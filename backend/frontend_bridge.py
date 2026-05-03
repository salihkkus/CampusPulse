from typing import Dict, List, Any
from datetime import datetime

class FrontendBridge:
    """
    Frontend Veri Köprüsü - JSON Sözleşmesi
    Muhammet'in frontend'i için optimize edilmiş veri formatı
    """
    
    def __init__(self):
        pass
    
    def format_room_for_frontend(self, ai_analysis: Dict) -> Dict:
        """
        Muhammet'e gönderilecek JSON formatı
        {
          "room_id": "LAB_204",
          "status": "CRITICAL",
          "is_anomaly": true,
          "detected_device": "Klima",
          "instant_loss_tl": 14.20,
          "recommendation": "Oda boş ancak klima aktif. Kapatılması önerilir."
        }
        """
        # Status seviyesini belirle
        urgency_level = ai_analysis.get("urgency_level", "low")
        status_map = {
            "critical": "CRITICAL",
            "high": "WARNING", 
            "medium": "ATTENTION",
            "low": "NORMAL"
        }
        status = status_map.get(urgency_level, "NORMAL")
        
        # Ana cihazı belirle
        detected_device = ai_analysis.get("primary_device", "Bilinmeyen")
        
        # Cihaz adını Türkçe'leştir
        device_names = {
            "klima": "Klima",
            "projeksiyon": "Projeksiyon",
            "pc": "PC",
            "pc_20_adet": "PC'ler",
            "aydınlatma": "Aydınlatma",
            "server": "Sunucu"
        }
        detected_device_tr = device_names.get(detected_device, detected_device)
        
        # Anlık kayıp
        instant_loss = ai_analysis.get("instant_loss_tl_per_hour", 0)
        
        # Öneri oluştur
        recommendation = self.generate_frontend_recommendation(ai_analysis)
        
        # Oda ID'sini formatla
        room_id = ai_analysis.get("room_id", "")
        if "ENG" in room_id:
            room_id = room_id.replace("ENG", "DERSLIK_")
        elif "LAB" in room_id:
            room_id = room_id.replace("LAB", "LAB_")
        elif "OFIS" in room_id:
            room_id = room_id.replace("OFIS", "OFIS_")
        
        return {
            "room_id": room_id,
            "status": status,
            "is_anomaly": ai_analysis.get("is_anomaly", False),
            "detected_device": detected_device_tr,
            "instant_loss_tl": round(instant_loss, 2),
            "recommendation": recommendation,
            
            # Ek bilgiler (isteğe bağlı)
            "current_power": ai_analysis.get("current_power_watts", 0),
            "occupancy_status": ai_analysis.get("occupancy_status", 0),
            "waste_percentage": ai_analysis.get("waste_percentage", 0),
            "carbon_kg_per_hour": ai_analysis.get("carbon_kg_per_hour", 0),
            "confidence": round(ai_analysis.get("analysis_confidence", 0) * 100, 1),
            "coordinates": ai_analysis.get("coordinates", {"x": 0, "y": 0, "z": 0}),
            "room_name": ai_analysis.get("room_name", ""),
            "building": ai_analysis.get("building", ""),
            "floor": ai_analysis.get("floor", 0)
        }
    
    def generate_frontend_recommendation(self, ai_analysis: Dict) -> str:
        """
        Frontend için öneri metni oluştur
        """
        is_wasting = ai_analysis.get("is_wasting_energy", False)
        is_anomaly = ai_analysis.get("is_anomaly", False)
        detected_device = ai_analysis.get("primary_device", "")
        occupancy = ai_analysis.get("occupancy_status", 1)
        
        device_names_tr = {
            "klima": "klima",
            "projeksiyon": "projeksiyon cihazı",
            "pc": "PC",
            "pc_20_adet": "PC'ler",
            "aydınlatma": "ışıklar",
            "server": "sunucu"
        }
        device_tr = device_names_tr.get(detected_device, "cihazlar")
        
        if is_wasting and occupancy == 0:
            # Boş oda israfı
            return f"Oda boş ancak {device_tr} aktif. Kapatılması önerilir."
        elif is_anomaly and not is_wasting:
            # Anormal tüketim
            return f"Anormal enerji tüketimi tespit edildi. Kontrol edilmesi önerilir."
        elif is_wasting and occupancy == 1:
            # Dolu oda ama yüksek tüketim
            return f"Yüksek enerji tüketimi tespit edildi. Tasarruf yapılabilir."
        else:
            # Normal durum
            return "Enerji tüketimi normal seviyede."
    
    def format_all_rooms_for_frontend(self, rooms_analyses: List[Dict]) -> Dict:
        """
        Tüm odaları frontend formatında döndür
        """
        formatted_rooms = []
        summary_stats = {
            "total_rooms": len(rooms_analyses),
            "critical_rooms": 0,
            "warning_rooms": 0,
            "normal_rooms": 0,
            "total_waste_tl": 0,
            "total_carbon_kg": 0,
            "total_power_watts": 0
        }
        
        for analysis in rooms_analyses:
            formatted_room = self.format_room_for_frontend(analysis)
            formatted_rooms.append(formatted_room)
            
            # İstatistikleri güncelle
            status = formatted_room["status"]
            if status == "CRITICAL":
                summary_stats["critical_rooms"] += 1
            elif status == "WARNING" or status == "ATTENTION":
                summary_stats["warning_rooms"] += 1
            else:
                summary_stats["normal_rooms"] += 1
            
            # Toplam israfı hesapla
            summary_stats["total_waste_tl"] += formatted_room.get("instant_loss_tl", 0)
            summary_stats["total_carbon_kg"] += formatted_room.get("carbon_kg_per_hour", 0)
                
            # Toplam tüketimi hesapla (kW)
            summary_stats["total_power_watts"] += formatted_room.get("current_power", 0)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": summary_stats,
            "rooms": formatted_rooms
        }
    
    def format_room_detail_for_frontend(self, ai_analysis: Dict) -> Dict:
        """
        Oda detayı için frontend formatı
        """
        basic_info = self.format_room_for_frontend(ai_analysis)
        
        # Detaylı bilgiler
        device_breakdown = ai_analysis.get("device_cost_breakdown", {})
        formatted_breakdown = {}
        
        for device, info in device_breakdown.items():
            device_names_tr = {
                "klima": "Klima",
                "projeksiyon": "Projeksiyon",
                "pc": "PC",
                "pc_20_adet": "PC'ler",
                "aydınlatma": "Aydınlatma",
                "server": "Sunucu"
            }
            
            formatted_breakdown[device_names_tr.get(device, device)] = {
                "power_watts": info.get("estimated_power_watts", 0),
                "hourly_cost_tl": round(info.get("hourly_cost_tl", 0), 2),
                "daily_cost_tl": round(info.get("daily_cost_tl", 0), 2),
                "carbon_kg_per_hour": round(info.get("carbon_kg_per_hour", 0), 3)
            }
        
        # Finansal projeksiyonlar
        financial_projections = {
            "hourly": round(ai_analysis.get("instant_loss_tl_per_hour", 0), 2),
            "daily": round(ai_analysis.get("daily_cost_tl", 0), 2),
            "weekly": round(ai_analysis.get("weekly_cost_tl", 0), 2),
            "monthly": round(ai_analysis.get("monthly_cost_tl", 0), 2),
            "annual": round(ai_analysis.get("annual_cost_tl", 0), 2)
        }
        
        # Karbon projeksiyonlar
        carbon_projections = {
            "hourly": round(ai_analysis.get("carbon_kg_per_hour", 0), 3),
            "daily": round(ai_analysis.get("carbon_kg_per_day", 0), 2),
            "weekly": round(ai_analysis.get("carbon_kg_per_week", 0), 2),
            "monthly": round(ai_analysis.get("carbon_kg_per_month", 0), 2),
            "annual": round(ai_analysis.get("carbon_kg_per_year", 0), 2)
        }
        
        return {
            **basic_info,
            "device_breakdown": formatted_breakdown,
            "financial_projections": financial_projections,
            "carbon_projections": carbon_projections,
            "analysis_methods": ai_analysis.get("analysis_methods", []),
            "diagnostic_message": ai_analysis.get("diagnostic_message", ""),
            "waste_percentage": ai_analysis.get("waste_percentage", 0),
            "anomaly_score": round(ai_analysis.get("anomaly_score", 0), 3)
        }
    
    def create_alert_payload(self, ai_analysis: Dict) -> Dict:
        """
        Frontend için alert/popup payload'ı
        """
        return {
            "type": "alert",
            "room_id": ai_analysis.get("room_id", ""),
            "severity": ai_analysis.get("urgency_level", "low"),
            "title": f"⚠️ {ai_analysis.get('room_name', '')}",
            "message": ai_analysis.get("diagnostic_message", ""),
            "instant_loss": round(ai_analysis.get("instant_loss_tl_per_hour", 0), 2),
            "action_required": ai_analysis.get("is_wasting_energy", False),
            "timestamp": datetime.now().isoformat()
        }
