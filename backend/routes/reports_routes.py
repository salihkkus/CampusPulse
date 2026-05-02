from fastapi import APIRouter, Depends
from datetime import datetime
from dependencies import get_data_service, get_ai_engine, get_chart_service

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.get("/energy-audit")
async def get_energy_audit_report(data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine), chart_service=Depends(get_chart_service)):
    rooms_data = data_service.get_all_rooms_current_status()
    audit_data = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "report_type": "Energy Audit Report",
            "period": "Last 24 Hours",
            "total_rooms": len(rooms_data)
        },
        "executive_summary": {
            "total_power_consumption": sum(r["current_power"] for r in rooms_data),
            "total_wasting_rooms": len([r for r in rooms_data if r["occupancy_status"] == 0 and r["current_power"] > 50]),
            "estimated_daily_loss": 0,
            "carbon_footprint": 0
        },
        "room_details": [],
        "recommendations": [],
        "charts": {
            "waste_comparison": chart_service.prepare_waste_comparison_chart(),
            "device_breakdown": chart_service.prepare_device_breakdown_chart(),
            "financial_trend": chart_service.prepare_financial_trend_chart(7)
        }
    }
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24)
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        
        audit_data["room_details"].append({
            "room_id": room_id,
            "room_name": room_data["room_name"],
            "current_power": room_data["current_power"],
            "occupancy_status": room_data["occupancy_status"],
            "is_wasting": ai_analysis.get("is_wasting_energy", False),
            "waste_percentage": ai_analysis.get("waste_percentage", 0),
            "instant_loss_tl": ai_analysis.get("instant_loss_tl_per_hour", 0),
            "detected_devices": ai_analysis.get("detected_devices", []),
            "recommendation": ai_analysis.get("diagnostic_message", "")
        })
        
        if ai_analysis.get("is_wasting_energy", False):
            audit_data["executive_summary"]["estimated_daily_loss"] += ai_analysis.get("daily_cost_tl", 0)
            audit_data["executive_summary"]["carbon_footprint"] += ai_analysis.get("carbon_kg_per_day", 0)
    
    audit_data["recommendations"] = [
        "Otomatik klima kontrol sistemi kurulumu önerilir",
        "Boş odalardaki aydınlatma sensörleri takılmalı",
        "PC'ler için otomatik uyku modu konfigürasyonu yapılmalı",
        "Ders programına göre otomatik cihaz kontrolü sağlanmalı"
    ]
    
    return audit_data
