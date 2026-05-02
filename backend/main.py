from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from data_service import DataService

app = FastAPI(
    title="CampusPulse API",
    description="Energy Waste Detection System API",
    version="1.0.0"
)

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Service
data_service = DataService()

# Models
class RoomStatus(BaseModel):
    room_id: str
    room_name: str
    building: str
    floor: int
    current_power: float
    occupancy_status: int  # 0 = empty, 1 = occupied
    is_wasting_energy: bool
    waste_percentage: float
    detected_devices: List[str]
    coordinates: Dict[str, float]
    temperature: float
    active_devices: List[str]

class RoomStatusResponse(BaseModel):
    timestamp: str
    total_rooms: int
    wasting_rooms: int
    rooms: List[RoomStatus]

@app.get("/")
async def root():
    return {"message": "CampusPulse API is running"}

@app.get("/api/v1/rooms/status", response_model=RoomStatusResponse)
async def get_rooms_status():
    """
    Tüm odaların anlık enerji ve doluluk durumunu döndürür
    Muhammet'in frontend'i bu endpoint'i kullanacak
    """
    rooms_data = data_service.get_all_rooms_current_status()
    rooms = []
    wasting_count = 0
    
    for room_data in rooms_data:
        # AI Motoru - Anomali Tespiti (Senin görevin)
        is_wasting = room_data["occupancy_status"] == 0 and room_data["current_power"] > 50
        waste_percentage = (room_data["current_power"] / 1000) * 100 if is_wasting else 0
        
        # Cihaz Teşhisi (Senin görevin)
        detected_devices = []
        power = room_data["current_power"]
        
        if power > 200:
            detected_devices.append("Klima")
        if power > 1000:
            detected_devices.append("Projeksiyon")
        if power > 500:
            detected_devices.append("PC'ler")
        
        room_status = RoomStatus(
            room_id=room_data["room_id"],
            room_name=room_data["room_name"],
            building=room_data["building"],
            floor=room_data["floor"],
            current_power=room_data["current_power"],
            occupancy_status=room_data["occupancy_status"],
            is_wasting_energy=is_wasting,
            waste_percentage=waste_percentage,
            detected_devices=detected_devices,
            coordinates=room_data["coordinates"],
            temperature=room_data["temperature"],
            active_devices=room_data["active_devices"]
        )
        
        rooms.append(room_status)
        if is_wasting:
            wasting_count += 1
    
    response = RoomStatusResponse(
        timestamp=rooms_data[0]["timestamp"] if rooms_data else "2024-05-02T11:00:00Z",
        total_rooms=len(rooms),
        wasting_rooms=wasting_count,
        rooms=rooms
    )
    
    return response

@app.get("/api/v1/rooms/{room_id}")
async def get_room_detail(room_id: str):
    """Belirli bir odanın detaylı bilgisi"""
    room_data = data_service.get_current_room_data(room_id)
    if not room_data:
        return JSONResponse(
            status_code=404,
            content={"message": f"Room {room_id} not found"}
        )
    
    return room_data

@app.get("/api/v1/rooms/{room_id}/history")
async def get_room_history(room_id: str, hours: int = 24):
    """Belirli bir odanın geçmiş verisi"""
    history = data_service.get_room_history(room_id, hours)
    if not history:
        return JSONResponse(
            status_code=404,
            content={"message": f"Room {room_id} not found"}
        )
    
    return {
        "room_id": room_id,
        "hours": hours,
        "data": history
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
