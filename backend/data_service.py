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
        """JSON veri dosyasını pandas DataFrame'e yükle"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.rooms_data = json.load(f)
            print(f"✅ Veri yüklendi: {len(self.rooms_data)} oda")
        except FileNotFoundError:
            print(f"⚠️ Veri dosyası bulunamadı: {self.data_file}")
            print("🔄 Mock data kullanılıyor...")
            self.generate_mock_data()
    
    def generate_mock_data(self):
        """Eren'in verisi gelene kadar örnek veri oluştur"""
        self.rooms_data = [
            {
                "room_id": "ENG101",
                "room_name": "Derslik 101",
                "building": "Mühendislik Fakültesi",
                "floor": 1,
                "coordinates": {"x": 100, "y": 150, "z": 0},
                "devices": ["klima", "projeksiyon", "aydınlatma"],
                "time_series": self.generate_time_series("ENG101")
            },
            {
                "room_id": "LAB201", 
                "room_name": "Bilgisayar Lab 201",
                "building": "Mühendislik Fakültesi",
                "floor": 2,
                "coordinates": {"x": 200, "y": 250, "z": 1},
                "devices": ["klima", "pc_20_adet", "projeksiyon", "aydınlatma"],
                "time_series": self.generate_time_series("LAB201")
            },
            {
                "room_id": "OFIS301",
                "room_name": "Akademisyen Ofisi 301", 
                "building": "Mühendislik Fakültesi",
                "floor": 3,
                "coordinates": {"x": 150, "y": 350, "z": 2},
                "devices": ["klima", "pc", "aydınlatma"],
                "time_series": self.generate_time_series("OFIS301")
            }
        ]
    
    def generate_time_series(self, room_id: str) -> List[Dict]:
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
            
            time_series.append({
                "timestamp": timestamp.isoformat(),
                "power_consumption": round(power, 2),
                "occupancy_status": int(occupancy),
                "temperature": 22 + (hour % 4) - 2,  # 20-25°C
                "active_devices": self.get_active_devices(room_id, occupancy)
            })
        
        return time_series
    
    def get_active_devices(self, room_id: str, occupancy: float) -> List[str]:
        """Oda tipine ve doluluğa göre aktif cihazları belirle"""
        room = next((r for r in self.rooms_data if r["room_id"] == room_id), None)
        if not room:
            return []
        
        devices = room["devices"]
        active = []
        
        if occupancy == 0:
            # Boş odada kalan cihazlar (hayalet yük)
            if "klima" in devices and 6 <= datetime.now().hour <= 18:
                active.append("klima")
            if "pc" in devices or "pc_20_adet" in devices:
                active.append("pc")
        else:
            # Dolu odadaki normal cihazlar
            active.extend(devices)
        
        return active
    
    def get_current_room_data(self, room_id: str) -> Dict[str, Any]:
        """Belirli bir odanın güncel verisini getir"""
        room = next((r for r in self.rooms_data if r["room_id"] == room_id), None)
        if not room:
            return None
        
        # En son zaman serisi verisini al
        current_data = room["time_series"][-1]
        
        return {
            "room_id": room["room_id"],
            "room_name": room["room_name"],
            "building": room["building"],
            "floor": room["floor"],
            "coordinates": room["coordinates"],
            "devices": room["devices"],
            "current_power": current_data["power_consumption"],
            "occupancy_status": current_data["occupancy_status"],
            "temperature": current_data["temperature"],
            "active_devices": current_data["active_devices"],
            "timestamp": current_data["timestamp"]
        }
    
    def get_all_rooms_current_status(self) -> List[Dict[str, Any]]:
        """Tüm odaların güncel durumunu listele"""
        return [self.get_current_room_data(room["room_id"]) for room in self.rooms_data]
    
    def get_room_history(self, room_id: str, hours: int = 24) -> List[Dict]:
        """Belirli bir odanın geçmiş verisini getir"""
        room = next((r for r in self.rooms_data if r["room_id"] == room_id), None)
        if not room:
            return []
        
        return room["time_series"][-hours:]
