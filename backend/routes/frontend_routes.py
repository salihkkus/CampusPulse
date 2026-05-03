from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from dependencies import get_data_service, get_ai_engine, get_frontend_bridge

router = APIRouter(prefix="/api/v1/frontend", tags=["Frontend Bridge"])

@router.get("/timestamps")
async def get_available_timestamps(data_service=Depends(get_data_service)):
    return {"timestamps": data_service.get_available_timestamps()}

@router.get("/rooms")
async def get_frontend_rooms(timestamp: str = None, data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine), frontend_bridge=Depends(get_frontend_bridge)):
    rooms_data = data_service.get_all_rooms_current_status(timestamp)
    rooms_analyses = []
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24, timestamp)
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        rooms_analyses.append(ai_analysis)
    
    frontend_data = frontend_bridge.format_all_rooms_for_frontend(rooms_analyses)
    return frontend_data

@router.get("/rooms/{room_id}")
async def get_frontend_room_detail(room_id: str, timestamp: str = None, data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine), frontend_bridge=Depends(get_frontend_bridge)):
    room_data = data_service.get_current_room_data(room_id, timestamp)
    if not room_data:
        return JSONResponse(status_code=404, content={"message": f"Room {room_id} not found"})
    
    room_history = data_service.get_room_history(room_id, 24, timestamp)
    ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
    frontend_detail = frontend_bridge.format_room_detail_for_frontend(ai_analysis)
    return frontend_detail

@router.get("/alerts")
async def get_frontend_alerts(timestamp: str = None, data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine), frontend_bridge=Depends(get_frontend_bridge)):
    rooms_data = data_service.get_all_rooms_current_status(timestamp)
    alerts = []
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24, timestamp)
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        
        if ai_analysis.get("needs_attention", False):
            alert = frontend_bridge.create_alert_payload(ai_analysis)
            alerts.append(alert)
            
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    alerts.sort(key=lambda x: severity_order.get(x["severity"], 4))
    
    return {
        "timestamp": timestamp or datetime.now().isoformat(),
        "total_alerts": len(alerts),
        "alerts": alerts
    }

@router.get("/summary")
async def get_frontend_summary(timestamp: str = None, data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine), frontend_bridge=Depends(get_frontend_bridge)):
    frontend_rooms = await get_frontend_rooms(timestamp, data_service, ai_engine, frontend_bridge)
    summary = frontend_rooms["summary"]
    critical_rooms = [room for room in frontend_rooms["rooms"] if room["status"] == "CRITICAL"][:3]
    
    total_waste_per_hour = summary["total_waste_tl"]
    total_waste_per_day = total_waste_per_hour * 24
    total_waste_per_month = total_waste_per_day * 30
    
    return {
        "timestamp": timestamp or datetime.now().isoformat(),
        "overview": {
            "total_rooms": summary["total_rooms"],
            "critical_rooms": summary["critical_rooms"],
            "warning_rooms": summary["warning_rooms"],
            "normal_rooms": summary["normal_rooms"],
            "total_power_watts": summary["total_power_watts"],
            "total_waste_tl": summary["total_waste_tl"],
            "total_carbon_kg": summary["total_carbon_kg"]
        },
        "financial_impact": {
            "instant_loss_per_hour": round(total_waste_per_hour, 2),
            "projected_daily_loss": round(total_waste_per_day, 2),
            "projected_monthly_loss": round(total_waste_per_month, 2),
            "total_carbon_kg_per_hour": round(summary["total_carbon_kg"], 2)
        },
        "top_critical_rooms": critical_rooms,
        "alert_count": len([room for room in frontend_rooms["rooms"] if room["status"] in ["CRITICAL", "WARNING"]])
    }

@router.get("/range-report")
async def get_range_report(start_date: str, end_date: str, start_hour: int = 0, end_hour: int = 23, data_service=Depends(get_data_service)):
    return data_service.get_range_analysis(start_date, end_date, start_hour, end_hour)
