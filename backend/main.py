from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
from datetime import datetime, date
from data_service import DataService
from ai_engine import AIEngine
from frontend_bridge import FrontendBridge
from chart_data_service import ChartDataService
from enhanced_ai_engine import EnhancedAIEngine
from models.energy_data import EnergyDataRecord, EnergyDataBatch, EnergyDataValidationResponse

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

# Data Service, AI Engine, Frontend Bridge ve Chart Data Service
data_service = DataService()
ai_engine = AIEngine()
frontend_bridge = FrontendBridge()
chart_service = ChartDataService()

# Geliştirilmiş AI Motoru
enhanced_ai = EnhancedAIEngine()

# Eren'in veri seti için geçici depolama
eren_data_storage: List[EnergyDataRecord] = []

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

# Rapor Grafikleri Endpoint'leri
@app.get("/api/v1/charts/time-series/{room_id}")
async def get_time_series_chart(room_id: str, days: int = 7):
    """
    Belirli bir odanın zaman serisi grafiği
    Güç tüketimi, doluluk trendleri
    """
    chart_data = chart_service.prepare_time_series_data(room_id, days)
    return chart_data

@app.get("/api/v1/charts/waste-comparison")
async def get_waste_comparison_chart():
    """
    Odalar arası israf karşılaştırma grafiği
    Bar chart formatında
    """
    chart_data = chart_service.prepare_waste_comparison_chart()
    return chart_data

@app.get("/api/v1/charts/device-breakdown")
async def get_device_breakdown_chart(room_id: str = None):
    """
    Cihaz bazında enerji tüketim dağılımı
    Pie chart formatında
    """
    chart_data = chart_service.prepare_device_breakdown_chart(room_id)
    return chart_data

@app.get("/api/v1/charts/financial-trend")
async def get_financial_trend_chart(days: int = 30):
    """
    Finansal trend grafiği
    Günlük toplam maliyet ve karbon emisyonu
    """
    chart_data = chart_service.prepare_financial_trend_chart(days)
    return chart_data

@app.get("/api/v1/charts/occupancy-efficiency")
async def get_occupancy_efficiency_chart():
    """
    Doluluk vs Verimlilik grafiği
    Scatter plot formatında
    """
    chart_data = chart_service.prepare_occupancy_efficiency_chart()
    return chart_data

@app.get("/api/v1/charts/dashboard")
async def get_dashboard_charts():
    """
    Dashboard için tüm grafiklerin özeti
    Tek bir endpoint'den tüm grafik verileri
    """
    dashboard_data = chart_service.prepare_dashboard_summary()
    return dashboard_data

@app.get("/api/v1/reports/energy-audit")
async def get_energy_audit_report():
    """
    Kapsamlı enerji denetim raporu
    PDF export için veri hazırlığı
    """
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
    
    # Oda detaylarını ekle
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
    
    # Genel öneriler
    audit_data["recommendations"] = [
        "Otomatik klima kontrol sistemi kurulumu önerilir",
        "Boş odalardaki aydınlatma sensörleri takılmalı",
        "PC'ler için otomatik uyku modu konfigürasyonu yapılmalı",
        "Ders programına göre otomatik cihaz kontrolü sağlanmalı"
    ]
    
    return audit_data

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

# Eren'in Veri Seti Endpoint'leri
@app.post("/api/v1/data/upload", response_model=EnergyDataValidationResponse)
async def upload_energy_data(record: EnergyDataRecord):
    """
    Eren'den gelen tekil enerji verisi kaydını işle
    Veri doğrulama ve depolama
    """
    try:
        # Veriyi depola
        eren_data_storage.append(record)
        
        # AI motoru için format'a çevir
        ai_format = record.to_ai_format()
        
        return EnergyDataValidationResponse(
            is_valid=True,
            processed_records=1,
            warnings=[],
            errors=[]
        )
        
    except Exception as e:
        return EnergyDataValidationResponse(
            is_valid=False,
            processed_records=0,
            errors=[f"Veri işleme hatası: {str(e)}"]
        )

@app.post("/api/v1/data/batch-upload", response_model=EnergyDataValidationResponse)
async def upload_energy_data_batch(batch: EnergyDataBatch):
    """
    Eren'den gelen toplu enerji verisini işle
    Batch doğrulama ve depolama
    """
    try:
        # Tüm kayıtları depola
        eren_data_storage.extend(batch.records)
        
        # Batch özeti al
        summary = batch.get_summary()
        
        return EnergyDataValidationResponse(
            is_valid=True,
            processed_records=len(batch.records),
            batch_summary=summary,
            warnings=[],
            errors=[]
        )
        
    except Exception as e:
        return EnergyDataValidationResponse(
            is_valid=False,
            processed_records=0,
            errors=[f"Batch işleme hatası: {str(e)}"]
        )

@app.get("/api/v1/data/records")
async def get_energy_records(
    room_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100
):
    """
    Depolanmış enerji verilerini listele
    Filtreleme ve sayfalama desteği
    """
    filtered_records = eren_data_storage.copy()
    
    # Oda ID'sine göre filtrele
    if room_id:
        filtered_records = [r for r in filtered_records if r.room_id == room_id]
    
    # Tarih aralığına göre filtrele
    if start_date:
        filtered_records = [r for r in filtered_records if r.date >= start_date]
    
    if end_date:
        filtered_records = [r for r in filtered_records if r.date <= end_date]
    
    # Limit uygula
    filtered_records = filtered_records[:limit]
    
    return {
        "total_records": len(eren_data_storage),
        "filtered_records": len(filtered_records),
        "records": [record.to_dict() for record in filtered_records]
    }

@app.get("/api/v1/data/rooms")
async def get_available_rooms():
    """
    Sistemdeki mevcut odaları listele
    """
    unique_rooms = list(set(record.room_id for record in eren_data_storage))
    
    room_stats = {}
    for room_id in unique_rooms:
        room_records = [r for r in eren_data_storage if r.room_id == room_id]
        
        total_watt = sum(r.total_watt for r in room_records)
        wasted_cost = sum(r.wasted_cost_tl for r in room_records)
        wasting_count = len([r for r in room_records if r.is_wasting_energy()])
        
        room_stats[room_id] = {
            "record_count": len(room_records),
            "total_watt": total_watt,
            "total_wasted_cost": wasted_cost,
            "wasting_percentage": (wasting_count / len(room_records)) * 100 if room_records else 0,
            "avg_watt": total_watt / len(room_records) if room_records else 0
        }
    
    return {
        "total_rooms": len(unique_rooms),
        "rooms": room_stats
    }

@app.delete("/api/v1/data/clear")
async def clear_energy_data():
    """
    Tüm enerji verilerini temizle
    Test ve development için
    """
    global eren_data_storage
    record_count = len(eren_data_storage)
    eren_data_storage = []
    
    return {
        "message": f"{record_count} kayıt başarıyla temizlendi",
        "cleared_at": datetime.now().isoformat()
    }

# Geliştirilmiş AI Endpoint'leri
@app.get("/api/v2/ai/analysis/{room_id}")
async def get_enhanced_room_analysis(room_id: str):
    """
    Geliştirilmiş oda analizi
    Anomali + Teşhis + Finansal analiz
    """
    try:
        # Mevcut veriyi al
        current_data = data_service.get_room_current_status(room_id)
        
        if not current_data:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        
        # Kapsamlı analiz yap
        analysis = enhanced_ai.comprehensive_analysis(room_id, current_data)
        
        return {
            "success": True,
            "data": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/api/v2/ai/batch-analysis")
async def get_batch_analysis():
    """
    Tüm odalar için toplu analiz
    """
    try:
        # Tüm odaların mevcut durumunu al
        all_rooms = data_service.get_all_rooms_current_status()
        
        if not all_rooms:
            return {
                "success": True,
                "data": {
                    "summary": {
                        "total_rooms": 0,
                        "wasting_rooms": 0,
                        "critical_rooms": 0,
                        "total_waste_cost": 0.0,
                        "total_potential_savings": 0.0
                    },
                    "rooms": [],
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        # Toplu analiz yap
        batch_result = enhanced_ai.batch_analyze_rooms(all_rooms)
        
        return {
            "success": True,
            "data": batch_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis error: {str(e)}")

@app.get("/api/v2/ai/quick-diagnosis/{room_id}")
async def get_quick_diagnosis(room_id: str):
    """
    Hızlı teşhis - tek satır sonuç
    """
    try:
        # Mevcut veriyi al
        current_data = data_service.get_room_current_status(room_id)
        
        if not current_data:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        
        # Veriyi format'a çevir
        diagnosis_data = {
            "room_id": room_id,
            "timestamp": datetime.now().isoformat(),
            "occupancy_status": current_data.get("occupancy_status", 0),
            "hour_of_day": current_data.get("hour_of_day", datetime.now().hour),
            "total_power": current_data.get("power_consumption", 0),  # Düzeltildi
            "lighting_watt": current_data.get("lighting_watt", 0),
            "projector_watt": current_data.get("projector_watt", 0),
            "plug_load_watt": current_data.get("plug_load_watt", 0),
            "is_weekend": current_data.get("is_weekend", 0),
            "is_holiday": current_data.get("is_holiday", 0)
        }
        
        # Hızlı teşhis
        quick_diagnosis = enhanced_ai.diagnosis_engine.get_quick_diagnosis(diagnosis_data)
        
        return {
            "success": True,
            "data": {
                "room_id": room_id,
                "diagnosis": quick_diagnosis,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick diagnosis error: {str(e)}")

@app.get("/api/v2/ai/model-info")
async def get_ai_model_info():
    """
    AI model bilgileri
    """
    try:
        model_info = enhanced_ai.get_model_info()
        
        return {
            "success": True,
            "data": model_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model info error: {str(e)}")

@app.post("/api/v2/ai/custom-analysis")
async def post_custom_analysis(data: Dict[str, Any]):
    """
    Özel veri için analiz
    Frontend'den gelen özel veriyi analiz eder
    """
    try:
        room_id = data.get("room_id", "unknown")
        
        # Analiz yap
        analysis = enhanced_ai.comprehensive_analysis(room_id, data)
        
        return {
            "success": True,
            "data": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom analysis error: {str(e)}")

@app.get("/api/v2/ai/room-status/{room_id}")
async def get_room_status_with_ai(room_id: str):
    """
    Oda durumu + AI analizi
    Muhammet'in frontend'i için optimize edilmiş
    """
    try:
        # Mevcut durumu al
        current_data = data_service.get_room_current_status(room_id)
        
        if not current_data:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        
        # AI analizi yap
        analysis = enhanced_ai.comprehensive_analysis(room_id, current_data)
        
        # Frontend format'ında hazırla
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
        
        return {
            "success": True,
            "data": response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Room status error: {str(e)}")

@app.get("/api/v2/ai/dashboard-summary")
async def get_dashboard_summary():
    """
    Dashboard özeti
    Tüm odaların durumu + istatistikler
    """
    try:
        # Toplu analiz yap
        batch_result = enhanced_ai.batch_analyze_rooms(data_service.get_all_rooms_current_status())
        
        # Dashboard verisi hazırla
        summary = batch_result["summary"]
        rooms = batch_result["rooms"]
        
        # En kritik odalar
        critical_rooms = [room for room in rooms if room["status"] == "CRITICAL"][:5]
        
        # En çok israf yapan odalar
        wasting_rooms = [room for room in rooms if room["analysis"]["diagnosis"]["is_wasting"]]
        wasting_rooms.sort(key=lambda x: x["analysis"]["financial"]["wasted_cost_per_hour"], reverse=True)
        top_wasters = wasting_rooms[:5]
        
        # Öneriler
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
                }
                for room in critical_rooms
            ],
            "top_wasters": [
                {
                    "room_id": room["room_id"],
                    "waste_per_hour": room["analysis"]["financial"]["wasted_cost_per_hour"],
                    "devices": room["current_data"]["detected_devices"],
                    "issue": room["analysis"]["diagnosis"].get("primary_issue", "Unknown")
                }
                for room in top_wasters
            ],
            "recommendations": all_recommendations[:10],  # İlk 10 öneri
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "data": dashboard_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
