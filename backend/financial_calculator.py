from typing import Dict, List, Any
from datetime import datetime, timedelta

class FinancialCalculator:
    """
    Finansal ve Karbon Hesaplamaları
    Teşhis konulan her israf için maliyet çıktıları üretir
    """
    
    def __init__(self):
        # Türkiye elektrik birim fiyatı (TL/kWh) - 2024 ortalaması
        self.electricity_price_per_kwh = 2.50  # TL/kWh
        
        # Karbon emisyon faktörü (kg CO2/kWh) - Türkiye ortalaması
        self.carbon_emission_factor = 0.45  # kg CO2/kWh
        
        # Cihaz bazında teşhis mesajları
        self.device_diagnostic_messages = {
            "klima": [
                "{room_number} nolu odada muhtemelen klima açık unutulmuş.",
                "{room_number} odasında klima boş iken çalışıyor.",
                "{room_number} nolu odada klima israfı tespit edildi."
            ],
            "projeksiyon": [
                "{room_number} nolu odada projeksiyon cihazı kapalı değil.",
                "{room_number} odasında projeksiyon boş iken aktif.",
                "{room_number} nolu odada projeksiyon israfı tespit edildi."
            ],
            "pc": [
                "{room_number} nolu odada PC'ler açık unutulmuş.",
                "{room_number} odasında bilgisayarlar boş iken çalışıyor.",
                "{room_number} nolu odada PC israfı tespit edildi."
            ],
            "pc_20_adet": [
                "{room_number} nolu lab'da 20 PC açık unutulmuş.",
                "{room_number} laboratuvarında PC'ler boş iken çalışıyor.",
                "{room_number} nolu lab'da PC israfı tespit edildi."
            ],
            "aydınlatma": [
                "{room_number} nolu odada ışıklar açık unutulmuş.",
                "{room_number} odasında aydınlatma boş iken aktif.",
                "{room_number} nolu odada aydınlatma israfı tespit edildi."
            ],
            "server": [
                "{room_number} nolu odada sunucu gereksiz yere çalışıyor.",
                "{room_number} odasında sunucu israfı tespit edildi."
            ]
        }
        
        # Genel teşhis mesajları
        self.general_diagnostic_messages = [
            "{room_number} nolu odada enerji israfı tespit edildi.",
            "{room_number} odasında boş iken aktif cihazlar var.",
            "{room_number} nolu odada acil müdahale gerekiyor."
        ]
    
    def calculate_instant_loss(self, power_watts: float) -> Dict[str, float]:
        """
        Anlık kayıp hesapla (TL)
        (Watt / 1000) * Birim Fiyat
        """
        power_kw = power_watts / 1000
        instant_cost_per_hour = power_kw * self.electricity_price_per_kwh
        
        # Günlük, haftalık, aylık tahminler
        daily_cost = instant_cost_per_hour * 24
        weekly_cost = daily_cost * 7
        monthly_cost = daily_cost * 30
        
        return {
            "instant_cost_per_hour": round(instant_cost_per_hour, 4),
            "daily_cost": round(daily_cost, 2),
            "weekly_cost": round(weekly_cost, 2),
            "monthly_cost": round(monthly_cost, 2)
        }
    
    def calculate_carbon_cost(self, power_watts: float) -> Dict[str, float]:
        """
        Karbon maliyeti hesapla (kg CO2)
        (Watt / 1000) * 0.45 (kg CO2)
        """
        power_kw = power_watts / 1000
        
        # Saatlik, günlük, haftalık karbon emisyonu
        carbon_per_hour = power_kw * self.carbon_emission_factor
        carbon_per_day = carbon_per_hour * 24
        carbon_per_week = carbon_per_day * 7
        carbon_per_month = carbon_per_day * 30
        
        return {
            "carbon_per_hour": round(carbon_per_hour, 3),
            "carbon_per_day": round(carbon_per_day, 2),
            "carbon_per_week": round(carbon_per_week, 2),
            "carbon_per_month": round(carbon_per_month, 2)
        }
    
    def generate_diagnostic_message(self, room_data: Dict, detected_devices: List[str]) -> str:
        """
        Teşhis mesajı oluştur
        "204 nolu odada muhtemelen Klima açık unutulmuş."
        """
        room_number = room_data.get("room_id", "Bilinmeyen")
        room_name = room_data.get("room_name", "")
        
        # Oda numarasını al (room_id'den)
        if "ENG" in room_number:
            room_number = room_number.replace("ENG", "")
        elif "LAB" in room_number:
            room_number = room_number.replace("LAB", "")
        elif "OFIS" in room_number:
            room_number = room_number.replace("OFIS", "")
        
        # En yüksek güç tüketen cihazı bul
        primary_device = self.get_primary_device(detected_devices)
        
        if primary_device and primary_device in self.device_diagnostic_messages:
            messages = self.device_diagnostic_messages[primary_device]
            message = messages[hash(room_number) % len(messages)]  # Rastgele mesaj seç
        else:
            messages = self.general_diagnostic_messages
            message = messages[hash(room_number) % len(messages)]
        
        return message.format(room_number=room_number)
    
    def get_primary_device(self, detected_devices: List[str]) -> str:
        """
        En yüksek güç tüketen cihazı belirle
        """
        device_power_ranking = {
            "pc_20_adet": 3000,
            "klima": 1200,
            "server": 800,
            "pc": 200,
            "projeksiyon": 300,
            "aydınlatma": 100
        }
        
        if not detected_devices:
            return None
        
        # En yüksek güçlü cihazı bul
        primary_device = None
        max_power = 0
        
        for device in detected_devices:
            if device in device_power_ranking:
                if device_power_ranking[device] > max_power:
                    max_power = device_power_ranking[device]
                    primary_device = device
        
        return primary_device
    
    def calculate_comprehensive_financials(self, room_data: Dict, analysis_result: Dict) -> Dict:
        """
        Kapsamlı finansal ve karbon hesaplaması
        """
        current_power = room_data["current_power"]
        detected_devices = analysis_result.get("detected_devices", [])
        
        # Finansal hesaplamalar
        financials = self.calculate_instant_loss(current_power)
        
        # Karbon hesaplamaları
        carbon = self.calculate_carbon_cost(current_power)
        
        # Teşhis mesajı
        diagnostic_message = self.generate_diagnostic_message(room_data, detected_devices)
        
        # Cihaz bazında maliyet dağılımı
        device_cost_breakdown = self.calculate_device_cost_breakdown(detected_devices, current_power)
        
        # Yıllık tahmin
        annual_cost = financials["daily_cost"] * 365
        annual_carbon = carbon["carbon_per_day"] * 365
        
        return {
            "room_id": room_data["room_id"],
            "room_name": room_data["room_name"],
            "current_power_watts": current_power,
            
            # Finansal çıktılar
            "instant_loss_tl_per_hour": financials["instant_cost_per_hour"],
            "daily_cost_tl": financials["daily_cost"],
            "weekly_cost_tl": financials["weekly_cost"],
            "monthly_cost_tl": financials["monthly_cost"],
            "annual_cost_tl": round(annual_cost, 2),
            
            # Karbon çıktıları
            "carbon_kg_per_hour": carbon["carbon_per_hour"],
            "carbon_kg_per_day": carbon["carbon_per_day"],
            "carbon_kg_per_week": carbon["carbon_per_week"],
            "carbon_kg_per_month": carbon["carbon_per_month"],
            "carbon_kg_per_year": round(annual_carbon, 2),
            
            # Teşhis
            "diagnostic_message": diagnostic_message,
            "primary_device": self.get_primary_device(detected_devices),
            "detected_devices": detected_devices,
            
            # Cihaz bazında maliyet
            "device_cost_breakdown": device_cost_breakdown,
            
            # Ek bilgiler
            "is_wasting_energy": analysis_result.get("is_wasting_energy", False),
            "waste_percentage": analysis_result.get("waste_percentage", 0),
            "urgency_level": analysis_result.get("urgency_level", "low"),
            
            # Fiyatlandırma bilgileri
            "electricity_price_per_kwh": self.electricity_price_per_kwh,
            "carbon_emission_factor": self.carbon_emission_factor,
            
            # Hesaplama zamanı
            "calculated_at": datetime.now().isoformat()
        }
    
    def calculate_device_cost_breakdown(self, detected_devices: List[str], total_power: float) -> Dict[str, Dict]:
        """
        Cihaz bazında maliyet dağılımı hesapla
        """
        device_power_signatures = {
            "klima": {"min_power": 800, "max_power": 2000, "typical": 1200},
            "projeksiyon": {"min_power": 200, "max_power": 500, "typical": 300},
            "pc": {"min_power": 100, "max_power": 300, "typical": 200},
            "pc_20_adet": {"min_power": 2000, "max_power": 4000, "typical": 3000},
            "aydınlatma": {"min_power": 50, "max_power": 200, "typical": 100},
            "server": {"min_power": 500, "max_power": 1500, "typical": 800}
        }
        
        breakdown = {}
        remaining_power = total_power
        
        for device in detected_devices:
            if device in device_power_signatures:
                signature = device_power_signatures[device]
                
                # Güç tüketimi tahmini
                device_power = min(signature["typical"], remaining_power)
                remaining_power -= device_power
                
                # Finansal hesaplamalar
                financials = self.calculate_instant_loss(device_power)
                carbon = self.calculate_carbon_cost(device_power)
                
                breakdown[device] = {
                    "estimated_power_watts": device_power,
                    "hourly_cost_tl": financials["instant_cost_per_hour"],
                    "daily_cost_tl": financials["daily_cost"],
                    "carbon_kg_per_hour": carbon["carbon_per_hour"],
                    "carbon_kg_per_day": carbon["carbon_per_day"]
                }
        
        return breakdown
    
    def calculate_building_summary(self, rooms_financials: List[Dict]) -> Dict:
        """
        Bina/genel özet hesaplamaları
        """
        total_power = sum(room["current_power_watts"] for room in rooms_financials)
        total_wasting_rooms = sum(1 for room in rooms_financials if room["is_wasting_energy"])
        
        # Toplam maliyetler
        total_hourly_cost = sum(room["instant_loss_tl_per_hour"] for room in rooms_financials)
        total_daily_cost = sum(room["daily_cost_tl"] for room in rooms_financials)
        total_monthly_cost = sum(room["monthly_cost_tl"] for room in rooms_financials)
        
        # Toplam karbon
        total_hourly_carbon = sum(room["carbon_kg_per_hour"] for room in rooms_financials)
        total_daily_carbon = sum(room["carbon_kg_per_day"] for room in rooms_financials)
        total_monthly_carbon = sum(room["carbon_kg_per_month"] for room in rooms_financials)
        
        # En çok israf yapan odalar
        top_wasting_rooms = sorted(
            [room for room in rooms_financials if room["is_wasting_energy"]],
            key=lambda x: x["instant_loss_tl_per_hour"],
            reverse=True
        )[:5]
        
        return {
            "summary": {
                "total_rooms": len(rooms_financials),
                "wasting_rooms": total_wasting_rooms,
                "waste_percentage": round((total_wasting_rooms / len(rooms_financials)) * 100, 1) if rooms_financials else 0,
                "total_power_watts": total_power,
                "total_hourly_cost_tl": round(total_hourly_cost, 2),
                "total_daily_cost_tl": round(total_daily_cost, 2),
                "total_monthly_cost_tl": round(total_monthly_cost, 2),
                "total_hourly_carbon_kg": round(total_hourly_carbon, 2),
                "total_daily_carbon_kg": round(total_daily_carbon, 2),
                "total_monthly_carbon_kg": round(total_monthly_carbon, 2)
            },
            "top_wasting_rooms": top_wasting_rooms,
            "calculated_at": datetime.now().isoformat()
        }
