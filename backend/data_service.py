import pandas as pd
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta

class DataService:
    """
    Eren'in hazırladığı veri dosyalarını okuyan ve işleyen servis
    JSON formatında zaman serisi verisi bekliyoruz
    """
    
    def __init__(self, data_file: str = "data/mock_rooms.json"):
        self.data_file = data_file
        self.rooms_data = None
        self.load_data()
    
    def load_data(self):
        """JSON veri dosyasını yükle"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # JSON yapısını kontrol et: { "rooms": [...] } veya doğrudan [...]
            if isinstance(raw_data, dict) and "rooms" in raw_data:
                self.rooms_data = raw_data["rooms"]
            elif isinstance(raw_data, list):
                self.rooms_data = raw_data
            else:
                print("[WARN] Beklenmeyen JSON yapisi, mock data kullaniliyor...")
                self.generate_mock_data()
                return
            
            print(f"[OK] Veri yuklendi: {len(self.rooms_data)} oda")
        except FileNotFoundError:
            print(f"[WARN] Veri dosyasi bulunamadi: {self.data_file}")
            print("[INFO] Mock data kullaniliyor...")
            self.generate_mock_data()
    
    def generate_mock_data(self):
        """Eren'in verisi gelene kadar örnek veri oluştur"""
        # Önce boş rooms_data oluştur (generate_time_series içinde kullanılıyor)
        self.rooms_data = []
        
        room_defs = [
            {
                "room_id": "ENG101",
                "room_name": "Derslik 101",
                "building": "Mühendislik Fakültesi",
                "floor": 1,
                "coordinates": {"x": 100, "y": 150, "z": 0},
                "devices": ["klima", "projeksiyon", "aydınlatma"],
            },
            {
                "room_id": "LAB201", 
                "room_name": "Bilgisayar Lab 201",
                "building": "Mühendislik Fakültesi",
                "floor": 2,
                "coordinates": {"x": 200, "y": 250, "z": 1},
                "devices": ["klima", "pc_20_adet", "projeksiyon", "aydınlatma"],
            },
            {
                "room_id": "OFIS301",
                "room_name": "Akademisyen Ofisi 301", 
                "building": "Mühendislik Fakültesi",
                "floor": 3,
                "coordinates": {"x": 150, "y": 350, "z": 2},
                "devices": ["klima", "pc", "aydınlatma"],
            }
        ]
        
        # Odaları oluştur ve time_series ekle
        self.rooms_data = []
        for room_def in room_defs:
            room_def["time_series"] = self._generate_time_series(room_def["room_id"], room_def["devices"])
            self.rooms_data.append(room_def)
    
    def _generate_time_series(self, room_id: str, devices: List[str]) -> List[Dict]:
        """Saatlik bazda 24 saatlik örnek veri oluştur"""
        time_series = []
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for hour in range(24):
            timestamp = base_time + timedelta(hours=hour)
            
            # Doluluk durumu (saatlere göre)
            if 8 <= hour <= 12 or 14 <= hour <= 17:  # Ders saatleri
                occupancy = 1
            elif 18 <= hour <= 22:  # Akşam kullanımı
                occupancy = 0.5 if "LAB" in room_id else 0
            else:  # Gece
                occupancy = 0
            
            # Güç tüketimi (doluluk ve cihazlara göre)
            if occupancy == 0:
                # Boş zaman - hayalet yük
                power = 50 + (hour % 3) * 30  # 50-140W arası
            else:
                # Dolu zaman - normal kullanım
                power = 200 + occupancy * 300 + (hour % 5) * 50  # 200-750W arası
            
            # Aktif cihazlar
            active = []
            if occupancy == 0:
                if "klima" in devices and 6 <= hour <= 18:
                    active.append("klima")
                if "pc" in devices or "pc_20_adet" in devices:
                    active.append("pc")
            else:
                active.extend(devices)
            
            time_series.append({
                "timestamp": timestamp.isoformat(),
                "power_consumption": round(power, 2),
                "occupancy_status": int(occupancy),
                "temperature": 22 + (hour % 4) - 2,  # 20-25°C
                "active_devices": active
            })
        
        return time_series
    
    def get_room_history(self, room_id: str, hours: int = 24) -> List[Dict]:
        """Belirli bir odanın geçmiş verisini getir"""
        if not self.rooms_data:
            return []
        
        room = next((r for r in self.rooms_data if r["room_id"] == room_id), None)
        if not room:
            return []
        
        time_series = room.get("time_series", [])
        
        # Son 'hours' kadar veriyi döndür
        return time_series[-hours:]
    
    def get_room_current_status(self, room_id: str) -> Dict[str, Any]:
        """Belirli bir odanın mevcut durumunu döndür"""
        if not self.rooms_data:
            return None
        
        room_data = next((room for room in self.rooms_data if room["room_id"] == room_id), None)
        if not room_data:
            return None
        
        # En son veriyi al
        time_series = room_data.get("time_series", [])
        if time_series:
            latest_data = time_series[-1]
        else:
            # Varsayılan veri
            latest_data = {
                "timestamp": datetime.now().isoformat(),
                "power_consumption": 0,
                "occupancy_status": 0,
                "temperature": 22,
                "active_devices": []
            }
        
        # Oda bilgileri ile birleştir
        current_status = {
            "room_id": room_data["room_id"],
            "room_name": room_data["room_name"],
            "building": room_data["building"],
            "floor": room_data["floor"],
            "coordinates": room_data.get("coordinates", {"x": 0, "y": 0, "z": 0}),
            "devices": room_data.get("devices", []),
            "hour_of_day": datetime.now().hour,
            # Alanları hem orijinal hem de normalize edilmiş isimlerle sağla
            "power_consumption": latest_data.get("power_consumption", 0),
            "current_power": latest_data.get("power_consumption", 0),  # ai_engine uyumluluğu
            "occupancy_status": latest_data.get("occupancy_status", 0),
            "temperature": latest_data.get("temperature", 22),
            "active_devices": latest_data.get("active_devices", []),
            "timestamp": latest_data.get("timestamp", datetime.now().isoformat()),
            # Enhanced AI için ek alanlar
            "lighting_watt": latest_data.get("lighting_watt", 0),
            "projector_watt": latest_data.get("projector_watt", 0),
            "plug_load_watt": latest_data.get("plug_load_watt", 0),
            "is_anomaly": latest_data.get("is_anomaly", 0),
            "is_weekend": latest_data.get("is_weekend", 0),
            "is_holiday": latest_data.get("is_holiday", 0),
        }
        
        return current_status
    
    def get_current_room_data(self, room_id: str) -> Dict[str, Any]:
        """
        Belirli bir odanın mevcut verisini döndür.
        get_room_current_status ile aynı, main.py uyumluluğu için alias.
        """
        return self.get_room_current_status(room_id)
    
    def get_all_rooms_current_status(self) -> List[Dict[str, Any]]:
        """Tüm odaların mevcut durumunu döndür"""
        if not self.rooms_data:
            return []
        
        all_rooms = []
        for room in self.rooms_data:
            status = self.get_room_current_status(room["room_id"])
            if status:
                all_rooms.append(status)
        
        return all_rooms
