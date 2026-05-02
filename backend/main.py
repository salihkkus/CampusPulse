from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
from data_service import DataService
from ai_engine import AIEngine
from frontend_bridge import FrontendBridge

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

# Data Service, AI Engine ve Frontend Bridge
data_service = DataService()
ai_engine = AIEngine()
frontend_bridge = FrontendBridge()

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
    # AI Analiz sonuçları
    is_anomaly: bool
    anomaly_score: float
    urgency_level: str
    analysis_confidence: float
    # Finansal çıktılar
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

@app.get("/")
async def root():
    return {"message": "CampusPulse API is running"}

@app.get("/api/v1/rooms/status", response_model=RoomStatusResponse)
async def get_rooms_status():
    """
    Tüm odaların anlık enerji ve doluluk durumunu döndürür
    AI motoru ile çift katmanlı analiz yapılır
    Muhammet'in frontend'i bu endpoint'i kullanacak
    """
    rooms_data = data_service.get_all_rooms_current_status()
    rooms = []
    wasting_count = 0
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        
        # Geçmiş veriyi al (ML analizi için)
        room_history = data_service.get_room_history(room_id, 24)
        
        # AI Motoru - Çift Katmanlı Analiz
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
            # AI Analiz sonuçları
            is_anomaly=ai_analysis["is_anomaly"],
            anomaly_score=ai_analysis["anomaly_score"],
            urgency_level=ai_analysis["urgency_level"],
            analysis_confidence=ai_analysis["analysis_confidence"],
            # Finansal çıktılar
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

@app.post("/api/v1/ai/train/{room_id}")
async def train_ai_model(room_id: str):
    """
    AI modelini belirli bir oda için eğit
    Eren'den gelen geçmiş verilerle normal tüketim profillerini öğren
    """
    history = data_service.get_room_history(room_id, 168)  # 1 haftalık veri
    
    if len(history) < 20:
        return JSONResponse(
            status_code=400,
            content={"message": f"Insufficient data for training room {room_id}"}
        )
    
    success = ai_engine.train_model_with_room_data(room_id, history)
    
    if success:
        return {
            "message": f"AI model trained successfully for room {room_id}",
            "training_data_size": len(history),
            "normal_profile": ai_engine.normal_consumption_profiles.get(room_id, {})
        }
    else:
        return JSONResponse(
            status_code=400,
            content={"message": f"Failed to train model for room {room_id}"}
        )

@app.get("/api/v1/ai/analysis/{room_id}")
async def get_ai_analysis(room_id: str):
    """Belirli bir odanın detaylı AI analizini döndür"""
    room_data = data_service.get_current_room_data(room_id)
    if not room_data:
        return JSONResponse(
            status_code=404,
            content={"message": f"Room {room_id} not found"}
        )
    
    room_history = data_service.get_room_history(room_id, 24)
    ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
    
    # Cihaz bazında israf dağılımı
    waste_breakdown = ai_engine.get_device_waste_breakdown(
        ai_analysis["detected_devices"], 
        ai_analysis["waste_percentage"]
    )
    
    return {
        **ai_analysis,
        "device_waste_breakdown": waste_breakdown,
        "normal_profile": ai_engine.normal_consumption_profiles.get(room_id, {}),
        "recommendations": generate_recommendations(ai_analysis)
    }

@app.get("/api/v1/financial/summary")
async def get_financial_summary():
    """
    Tüm binaların finansal özetini döndür
    Toplam maliyet, karbon emisyonu ve israf istatistikleri
    """
    rooms_data = data_service.get_all_rooms_current_status()
    rooms_financials = []
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24)
        
        # AI analizini al
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        
        # Sadece finansal bilgileri çıkar
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
    
    # Bina özeti hesapla
    building_summary = ai_engine.financial_calculator.calculate_building_summary(rooms_financials)
    
    return building_summary

@app.get("/api/v1/financial/top-wasters")
async def get_top_wasters(limit: int = 10):
    """
    En çok israf yapan odaları listeler
    """
    financial_summary = await get_financial_summary()
    top_wasters = financial_summary["top_wasting_rooms"][:limit]
    
    return {
        "top_wasting_rooms": top_wasters,
        "total_wasting_rooms": financial_summary["summary"]["wasting_rooms"],
        "queried_at": datetime.now().isoformat()
    }

# Frontend Bridge Endpoint'leri
@app.get("/api/v1/frontend/rooms")
async def get_frontend_rooms():
    """
    Muhammet'in frontend'i için optimize edilmiş oda verileri
    JSON Sözleşmesi formatında veri döndürür
    """
    rooms_data = data_service.get_all_rooms_current_status()
    rooms_analyses = []
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24)
        
        # AI analizini al
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        rooms_analyses.append(ai_analysis)
    
    # Frontend formatına çevir
    frontend_data = frontend_bridge.format_all_rooms_for_frontend(rooms_analyses)
    
    return frontend_data

@app.get("/api/v1/frontend/rooms/{room_id}")
async def get_frontend_room_detail(room_id: str):
    """
    Belirli bir odanın frontend detayı
    """
    room_data = data_service.get_current_room_data(room_id)
    if not room_data:
        return JSONResponse(
            status_code=404,
            content={"message": f"Room {room_id} not found"}
        )
    
    room_history = data_service.get_room_history(room_id, 24)
    ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
    
    # Frontend detay formatı
    frontend_detail = frontend_bridge.format_room_detail_for_frontend(ai_analysis)
    
    return frontend_detail

@app.get("/api/v1/frontend/alerts")
async def get_frontend_alerts():
    """
    Frontend için alert/popup verileri
    Sadece israf yapan veya anomali tespit edilen odalar
    """
    rooms_data = data_service.get_all_rooms_current_status()
    alerts = []
    
    for room_data in rooms_data:
        room_id = room_data["room_id"]
        room_history = data_service.get_room_history(room_id, 24)
        
        ai_analysis = ai_engine.comprehensive_analysis(room_id, room_data, room_history)
        
        # Sadece dikkat gerektiren durumlar
        if ai_analysis.get("needs_attention", False):
            alert = frontend_bridge.create_alert_payload(ai_analysis)
            alerts.append(alert)
    
    # Önem sırasına göre sırala
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    alerts.sort(key=lambda x: severity_order.get(x["severity"], 4))
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_alerts": len(alerts),
        "alerts": alerts
    }

@app.get("/api/v1/frontend/summary")
async def get_frontend_summary():
    """
    Frontend için dashboard özeti
    """
    frontend_rooms = await get_frontend_rooms()
    
    # Özet istatistikler
    summary = frontend_rooms["summary"]
    
    # En kritik 3 oda
    critical_rooms = [room for room in frontend_rooms["rooms"] if room["status"] == "CRITICAL"][:3]
    
    # Toplam maliyet bilgisi
    total_waste_per_hour = summary["total_waste_tl"]
    total_waste_per_day = total_waste_per_hour * 24
    total_waste_per_month = total_waste_per_day * 30
    
    return {
        "timestamp": datetime.now().isoformat(),
        "overview": {
            "total_rooms": summary["total_rooms"],
            "critical_rooms": summary["critical_rooms"],
            "warning_rooms": summary["warning_rooms"],
            "normal_rooms": summary["normal_rooms"]
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

def generate_recommendations(analysis: Dict) -> List[str]:
    """AI analizine göre öneriler oluştur"""
    recommendations = []
    
    if analysis["is_wasting_energy"]:
        recommendations.append("Oda boş iken aktif cihazları kapatın")
        
    if analysis["is_anomaly"]:
        recommendations.append("Anormal tüketim tespit edildi - kontrol edin")
        
    if analysis["urgency_level"] == "critical":
        recommendations.append("Acil müdahale gerekiyor - yüksek israf seviyesi")
    
    devices = analysis["detected_devices"]
    if "klima" in devices and analysis["occupancy_status"] == 0:
        recommendations.append("Klima otomatik kapatma sistemi kurun")
    
    if "pc_20_adet" in devices and analysis["occupancy_status"] == 0:
        recommendations.append("PC'ler için otomatik uyku modu ayarlayın")
    
    return recommendations

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
