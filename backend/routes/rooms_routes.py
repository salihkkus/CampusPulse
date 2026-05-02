from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Any
from dependencies import get_data_service, get_ai_engine
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/rooms", tags=["Rooms"])

class RoomStatus(BaseModel):
    room_id: str
    room_name: str
    building: str
    floor: int
    current_power: float
    occupancy_status: int
    is_wasting_energy: bool
    waste_percentage: float
    detected_devices: List[str]
    coordinates: Dict[str, float]
    temperature: float
    active_devices: List[str]
    is_anomaly: bool
    anomaly_score: float
    urgency_level: str
    analysis_confidence: float
    instant_loss_tl_per_hour: float
    daily_cost_tl: float
    carbon_kg_per_hour: float
    diagnostic_message: str
    primary_device: str

class RoomStatusResponse(BaseModel):
    timestamp: str
    total_rooms: int
    wasting_rooms: int
    rooms: List[RoomStatus]

@router.get("/status", response_model=RoomStatusResponse)
async def get_rooms_status(data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine)):
    rooms_data = data_service.get_all_rooms_current_status()
    rooms = []
    wasting_count = 0
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24)
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        
        room_status = RoomStatus(
            room_id=room_data["room_id"],
            room_name=room_data["room_name"],
            building=room_data["building"],
            floor=room_data["floor"],
            current_power=room_data["current_power"],
            occupancy_status=room_data["occupancy_status"],
            is_wasting_energy=ai_analysis["is_wasting_energy"],
            waste_percentage=ai_analysis["waste_percentage"],
            detected_devices=ai_analysis["detected_devices"],
            coordinates=room_data["coordinates"],
            temperature=room_data["temperature"],
            active_devices=room_data["active_devices"],
            is_anomaly=ai_analysis["is_anomaly"],
            anomaly_score=ai_analysis["anomaly_score"],
            urgency_level=ai_analysis["urgency_level"],
            analysis_confidence=ai_analysis["analysis_confidence"],
            instant_loss_tl_per_hour=ai_analysis["instant_loss_tl_per_hour"],
            daily_cost_tl=ai_analysis["daily_cost_tl"],
            carbon_kg_per_hour=ai_analysis["carbon_kg_per_hour"],
            diagnostic_message=ai_analysis["diagnostic_message"],
            primary_device=ai_analysis["primary_device"]
        )
        rooms.append(room_status)
        if ai_analysis["is_wasting_energy"]:
            wasting_count += 1
            
    response = RoomStatusResponse(
        timestamp=rooms_data[0]["timestamp"] if rooms_data else "2024-05-02T11:00:00Z",
        total_rooms=len(rooms),
        wasting_rooms=wasting_count,
        rooms=rooms
    )
    return response

@router.get("/{room_id}")
async def get_room_detail(room_id: str, data_service=Depends(get_data_service)):
    room_data = data_service.get_current_room_data(room_id)
    if not room_data:
        return JSONResponse(status_code=404, content={"message": f"Room {room_id} not found"})
    return room_data

@router.get("/{room_id}/history")
async def get_room_history(room_id: str, hours: int = 24, data_service=Depends(get_data_service)):
    history = data_service.get_room_history(room_id, hours)
    if not history:
        return JSONResponse(status_code=404, content={"message": f"Room {room_id} not found"})
    return {"room_id": room_id, "hours": hours, "data": history}
