from fastapi import APIRouter, Depends
from datetime import datetime
from dependencies import get_data_service, get_ai_engine

router = APIRouter(prefix="/api/v1/financial", tags=["Financial"])

@router.get("/summary")
async def get_financial_summary(data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine)):
    rooms_data = data_service.get_all_rooms_current_status()
    rooms_financials = []
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24)
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        
        financial_info = {
            "room_id": ai_analysis["room_id"],
            "room_name": ai_analysis["room_name"],
            "current_power_watts": ai_analysis["current_power_watts"],
            "is_wasting_energy": ai_analysis["is_wasting_energy"],
            "instant_loss_tl_per_hour": ai_analysis["instant_loss_tl_per_hour"],
            "daily_cost_tl": ai_analysis["daily_cost_tl"],
            "carbon_kg_per_hour": ai_analysis["carbon_kg_per_hour"],
            "diagnostic_message": ai_analysis["diagnostic_message"],
            "urgency_level": ai_analysis["urgency_level"]
        }
        rooms_financials.append(financial_info)
    
    building_summary = ai_engine.financial_calculator.calculate_building_summary(rooms_financials)
    return building_summary

@router.get("/top-wasters")
async def get_top_wasters(limit: int = 10, data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine)):
    financial_summary = await get_financial_summary(data_service, ai_engine)
    top_wasters = financial_summary["top_wasting_rooms"][:limit]
    
    return {
        "top_wasting_rooms": top_wasters,
        "total_wasting_rooms": financial_summary["summary"]["wasting_rooms"],
        "queried_at": datetime.now().isoformat()
    }
