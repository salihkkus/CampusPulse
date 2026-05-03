from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime
from dependencies import get_data_service, get_ai_engine, get_enhanced_ai

router = APIRouter(tags=["AI Analysis"])

# v1 routes
@router.post("/api/v1/ai/train/{room_id}")
async def train_ai_model(room_id: str, data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine)):
    history = data_service.get_room_history(room_id, 168)
    if len(history) < 20:
        return JSONResponse(status_code=400, content={"message": f"Insufficient data for training room {room_id}"})
    
    success = ai_engine.train_model_with_room_data(room_id, history)
    if success:
        return {
            "message": f"AI model trained successfully for room {room_id}",
            "training_data_size": len(history),
            "normal_profile": ai_engine.normal_consumption_profiles.get(room_id, {})
        }
    else:
        return JSONResponse(status_code=400, content={"message": f"Failed to train model for room {room_id}"})

@router.get("/api/v1/ai/analysis/{room_id}")
async def get_ai_analysis(room_id: str, data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine)):
    room_data = data_service.get_current_room_data(room_id)
    if not room_data:
        return JSONResponse(status_code=404, content={"message": f"Room {room_id} not found"})
    
    room_history = data_service.get_room_history(room_id, 24)
    ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
    
    waste_breakdown = ai_engine.get_device_waste_breakdown(
        ai_analysis["detected_devices"], 
        ai_analysis["waste_percentage"]
    )
    
    # recommendations
    recommendations = []
    if ai_analysis["is_wasting_energy"]: recommendations.append("Oda boş iken aktif cihazları kapatın")
    if ai_analysis["is_anomaly"]: recommendations.append("Anormal tüketim tespit edildi - kontrol edin")
    if ai_analysis["urgency_level"] == "critical": recommendations.append("Acil müdahale gerekiyor - yüksek israf seviyesi")
    devices = ai_analysis["detected_devices"]
    if "klima" in devices and ai_analysis["occupancy_status"] == 0: recommendations.append("Klima otomatik kapatma sistemi kurun")
    if "pc_20_adet" in devices and ai_analysis["occupancy_status"] == 0: recommendations.append("PC'ler için otomatik uyku modu ayarlayın")

    return {
        **ai_analysis,
        "device_waste_breakdown": waste_breakdown,
        "normal_profile": ai_engine.normal_consumption_profiles.get(room_id, {}),
        "recommendations": recommendations
    }

# v2 routes
@router.get("/api/v2/ai/analysis/{room_id}")
async def get_enhanced_room_analysis(room_id: str, data_service=Depends(get_data_service), enhanced_ai=Depends(get_enhanced_ai)):
    try:
        current_data = data_service.get_room_current_status(room_id)
        if not current_data:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        analysis = enhanced_ai.comprehensive_analysis(room_id, current_data)
        return {"success": True, "data": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.get("/api/v2/ai/batch-analysis")
async def get_batch_analysis(timestamp: str = None, data_service=Depends(get_data_service), enhanced_ai=Depends(get_enhanced_ai)):
    try:
        all_rooms = data_service.get_all_rooms_current_status(timestamp=timestamp)
        if not all_rooms:
            return {"success": True, "data": {"summary": {"total_rooms": 0, "wasting_rooms": 0, "critical_rooms": 0, "total_waste_cost": 0.0, "total_potential_savings": 0.0}, "rooms": [], "timestamp": datetime.now().isoformat()}}
        batch_result = enhanced_ai.batch_analyze_rooms(all_rooms)
        return {"success": True, "data": batch_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis error: {str(e)}")

@router.get("/api/v2/ai/quick-diagnosis/{room_id}")
async def get_quick_diagnosis(room_id: str, data_service=Depends(get_data_service), enhanced_ai=Depends(get_enhanced_ai)):
    try:
        current_data = data_service.get_room_current_status(room_id)
        if not current_data:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        
        diagnosis_data = {
            "room_id": room_id,
            "timestamp": datetime.now().isoformat(),
            "occupancy_status": current_data.get("occupancy_status", 0),
            "hour_of_day": current_data.get("hour_of_day", datetime.now().hour),
            "total_power": current_data.get("power_consumption", 0),
            "lighting_watt": current_data.get("lighting_watt", 0),
            "projector_watt": current_data.get("projector_watt", 0),
            "plug_load_watt": current_data.get("plug_load_watt", 0),
            "is_weekend": current_data.get("is_weekend", 0),
            "is_holiday": current_data.get("is_holiday", 0)
        }
        quick_diagnosis = enhanced_ai.diagnosis_engine.get_quick_diagnosis(diagnosis_data)
        return {"success": True, "data": {"room_id": room_id, "diagnosis": quick_diagnosis, "timestamp": datetime.now().isoformat()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick diagnosis error: {str(e)}")

@router.get("/api/v2/ai/model-info")
async def get_ai_model_info(enhanced_ai=Depends(get_enhanced_ai)):
    try:
        model_info = enhanced_ai.get_model_info()
        return {"success": True, "data": model_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model info error: {str(e)}")

@router.post("/api/v2/ai/custom-analysis")
async def post_custom_analysis(data: Dict[str, Any], enhanced_ai=Depends(get_enhanced_ai)):
    try:
        room_id = data.get("room_id", "unknown")
        analysis = enhanced_ai.comprehensive_analysis(room_id, data)
        return {"success": True, "data": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom analysis error: {str(e)}")

@router.get("/api/v2/ai/room-status/{room_id}")
async def get_room_status_with_ai(room_id: str, data_service=Depends(get_data_service), enhanced_ai=Depends(get_enhanced_ai)):
    try:
        current_data = data_service.get_room_current_status(room_id)
        if not current_data:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        analysis = enhanced_ai.comprehensive_analysis(room_id, current_data)
        
        response = {
            "room_id": room_id,
            "room_name": current_data.get("room_name", room_id),
            "building": current_data.get("building", "Unknown"),
            "floor": current_data.get("floor", 1),
            "status": analysis["status"],
            "is_wasting_energy": analysis["analysis"]["diagnosis"]["is_wasting"],
            "is_anomaly": analysis["analysis"]["anomaly"]["is_anomaly"],
            "urgency_level": analysis["urgency_level"],
            "current_power": analysis["current_data"]["power_consumption"],
            "occupancy_status": analysis["current_data"]["occupancy_status"],
            "detected_devices": analysis["current_data"]["detected_devices"],
            "instant_loss_tl_per_hour": analysis["analysis"]["financial"]["wasted_cost_per_hour"],
            "daily_cost_tl": analysis["analysis"]["financial"]["daily_cost"],
            "carbon_kg_per_hour": analysis["analysis"]["financial"]["wasted_carbon_per_hour"],
            "diagnostic_message": analysis["analysis"]["diagnosis"].get("primary_issue", "Normal"),
            "primary_device": analysis["current_data"]["detected_devices"][0] if analysis["current_data"]["detected_devices"] else "None",
            "recommendations": analysis["recommendations"],
            "confidence": analysis["confidence"],
            "timestamp": analysis["timestamp"]
        }
        return {"success": True, "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Room status error: {str(e)}")

@router.get("/api/v2/ai/dashboard-summary")
async def get_dashboard_summary(data_service=Depends(get_data_service), enhanced_ai=Depends(get_enhanced_ai)):
    try:
        batch_result = enhanced_ai.batch_analyze_rooms(data_service.get_all_rooms_current_status())
        summary = batch_result["summary"]
        rooms = batch_result["rooms"]
        
        critical_rooms = [room for room in rooms if room["status"] == "CRITICAL"][:5]
        wasting_rooms = [room for room in rooms if room["analysis"]["diagnosis"]["is_wasting"]]
        wasting_rooms.sort(key=lambda x: x["analysis"]["financial"]["wasted_cost_per_hour"], reverse=True)
        top_wasters = wasting_rooms[:5]
        
        all_recommendations = []
        for room in rooms:
            all_recommendations.extend(room["recommendations"])
            
        dashboard_data = {
            "summary": {
                "total_rooms": summary["total_rooms"],
                "wasting_rooms": summary["wasting_rooms"],
                "critical_rooms": summary["critical_rooms"],
                "normal_rooms": summary["total_rooms"] - summary["wasting_rooms"],
                "total_waste_per_hour": summary["total_waste_cost"],
                "total_potential_savings": summary["total_potential_savings"],
                "waste_percentage": (summary["wasting_rooms"] / summary["total_rooms"] * 100) if summary["total_rooms"] > 0 else 0
            },
            "critical_rooms": [
                {
                    "room_id": room["room_id"],
                    "status": room["status"],
                    "issue": room["analysis"]["diagnosis"].get("primary_issue", "Unknown"),
                    "urgency": room["urgency_level"],
                    "waste_per_hour": room["analysis"]["financial"]["wasted_cost_per_hour"]
                } for room in critical_rooms
            ],
            "top_wasters": [
                {
                    "room_id": room["room_id"],
                    "waste_per_hour": room["analysis"]["financial"]["wasted_cost_per_hour"],
                    "devices": room["current_data"]["detected_devices"],
                    "issue": room["analysis"]["diagnosis"].get("primary_issue", "Unknown")
                } for room in top_wasters
            ],
            "recommendations": all_recommendations[:10],
            "timestamp": datetime.now().isoformat()
        }
        return {"success": True, "data": dashboard_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")
