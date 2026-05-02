import pandas as pd
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
import os

class DataService:
    """
    Eren'in hazırladığı CSV veri dosyasını okuyan ve işleyen servis
    """
    
    def __init__(self, csv_file: str = "../kampus_1_aylik_enerji.csv"):
        self.csv_file = csv_file
        self.rooms_data = []
        self.load_csv_data()
    
    def load_csv_data(self):
        """CSV veri dosyasını pandas ile yükle"""
        try:
            if not os.path.exists(self.csv_file):
                print(f"[WARN] Veri dosyasi bulunamadi: {self.csv_file}")
                self.generate_mock_data()
                return
                
            print(f"[INFO] {self.csv_file} yükleniyor...")
            df = pd.read_csv(self.csv_file)
            
            # Zaman damgasını oluştur
            df['timestamp'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour_of_day'], unit='h')
            df = df.sort_values('timestamp')
            
            # Odalara göre grupla
            unique_rooms = df['room_id'].unique()
            self.rooms_data = []
            
            for room_id in unique_rooms:
                room_df = df[df['room_id'] == room_id].copy()
                
                # Bina ve oda tipini isminden çıkar (Örn: M1_Derslik_01)
                parts = str(room_id).split('_')
                building = parts[0] if len(parts) > 0 else "Unknown"
                room_type = parts[1] if len(parts) > 1 else "Room"
                room_num = parts[2] if len(parts) > 2 else "01"
                
                devices = ["klima", "aydınlatma", "projeksiyon"]
                if room_type.lower() == "lab":
                    devices.append("pc_20_adet")
                elif room_type.lower() == "ofis":
                    devices.append("pc")
                    
                time_series = []
                for _, row in room_df.iterrows():
                    active = []
                    if row['lighting_watt'] > 0: active.append("aydınlatma")
                    if row['projector_watt'] > 0: active.append("projeksiyon")
                    if row['plug_load_watt'] > 0: 
                        if room_type.lower() == "lab": active.append("pc_20_adet")
                        else: active.append("pc")
                    # Klima simülasyonu
                    if row['total_watt'] > (row['lighting_watt'] + row['projector_watt'] + row['plug_load_watt'] + 500):
                        active.append("klima")
                        
                    time_series.append({
                        "timestamp": row['timestamp'].isoformat() + "Z",
                        "power_consumption": float(row['total_watt']),
                        "occupancy_status": int(row['is_class_in_session']),
                        "temperature": 22.0, 
                        "active_devices": active,
                        "lighting_watt": float(row['lighting_watt']),
                        "projector_watt": float(row['projector_watt']),
                        "plug_load_watt": float(row['plug_load_watt']),
                        "is_anomaly": int(row['is_anomaly']),
                        "wasted_cost_tl": float(row['wasted_cost_tl']),
                        "is_weekend": int(row['is_weekend']),
                        "is_holiday": int(row['is_holiday'])
                    })
                
                self.rooms_data.append({
                    "room_id": str(room_id),
                    "room_name": f"{building} {room_type} {room_num}",
                    "building": building,
                    "floor": 1,
                    "coordinates": {"x": 0, "y": 0, "z": 0},
                    "devices": devices,
                    "time_series": time_series
                })
                
            print(f"[OK] CSV Veri yuklendi: {len(self.rooms_data)} oda")
        except Exception as e:
            print(f"[ERROR] CSV yuklenirken hata: {e}")
            self.generate_mock_data()
    
    def generate_mock_data(self):
        """Mock veri oluştur (Önceki metod)"""
        self.rooms_data = []
        room_defs = [
            {"room_id": "ENG101", "room_name": "Derslik 101", "building": "Mühendislik Fakültesi", "floor": 1, "coordinates": {"x": 100, "y": 150, "z": 0}, "devices": ["klima", "projeksiyon", "aydınlatma"]},
            {"room_id": "LAB201", "room_name": "Bilgisayar Lab 201", "building": "Mühendislik Fakültesi", "floor": 2, "coordinates": {"x": 200, "y": 250, "z": 1}, "devices": ["klima", "pc_20_adet", "projeksiyon", "aydınlatma"]},
            {"room_id": "OFIS301", "room_name": "Akademisyen Ofisi 301", "building": "Mühendislik Fakültesi", "floor": 3, "coordinates": {"x": 150, "y": 350, "z": 2}, "devices": ["klima", "pc", "aydınlatma"]}
        ]
        
        for room_def in room_defs:
            room_def["time_series"] = self._generate_time_series(room_def["room_id"], room_def["devices"])
            self.rooms_data.append(room_def)
    
    def _generate_time_series(self, room_id: str, devices: List[str]) -> List[Dict]:
        time_series = []
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for hour in range(24):
            timestamp = base_time + timedelta(hours=hour)
            if 8 <= hour <= 12 or 14 <= hour <= 17: occupancy = 1
            elif 18 <= hour <= 22: occupancy = 0.5 if "LAB" in room_id else 0
            else: occupancy = 0
            
            if occupancy == 0: power = 50 + (hour % 3) * 30
            else: power = 200 + occupancy * 300 + (hour % 5) * 50
            
            active = []
            if occupancy == 0:
                if "klima" in devices and 6 <= hour <= 18: active.append("klima")
                if "pc" in devices or "pc_20_adet" in devices: active.append("pc")
            else:
                active.extend(devices)
            
            time_series.append({
                "timestamp": timestamp.isoformat(),
                "power_consumption": round(power, 2),
                "occupancy_status": int(occupancy),
                "temperature": 22 + (hour % 4) - 2,
                "active_devices": active,
                "lighting_watt": 0,
                "projector_watt": 0,
                "plug_load_watt": 0,
                "is_anomaly": 0,
                "wasted_cost_tl": 0,
                "is_weekend": 0,
                "is_holiday": 0
            })
        return time_series
    
    def get_room_history(self, room_id: str, hours: int = 24) -> List[Dict]:
        if not self.rooms_data: return []
        room = next((r for r in self.rooms_data if r["room_id"] == room_id), None)
        if not room: return []
        return room.get("time_series", [])[-hours:]
    
    def get_room_current_status(self, room_id: str) -> Dict[str, Any]:
        if not self.rooms_data: return None
        room_data = next((room for room in self.rooms_data if room["room_id"] == room_id), None)
        if not room_data: return None
        
        time_series = room_data.get("time_series", [])
        latest_data = time_series[-1] if time_series else {
            "timestamp": datetime.now().isoformat(), "power_consumption": 0, "occupancy_status": 0, "temperature": 22, "active_devices": [],
            "lighting_watt": 0, "projector_watt": 0, "plug_load_watt": 0, "is_anomaly": 0, "wasted_cost_tl": 0, "is_weekend": 0, "is_holiday": 0
        }
        
        return {
            "room_id": room_data["room_id"],
            "room_name": room_data["room_name"],
            "building": room_data["building"],
            "floor": room_data["floor"],
            "coordinates": room_data.get("coordinates", {"x": 0, "y": 0, "z": 0}),
            "devices": room_data.get("devices", []),
            "hour_of_day": datetime.fromisoformat(latest_data["timestamp"].replace("Z", "+00:00")).hour if "Z" in latest_data["timestamp"] else datetime.now().hour,
            "power_consumption": latest_data.get("power_consumption", 0),
            "current_power": latest_data.get("power_consumption", 0),
            "occupancy_status": latest_data.get("occupancy_status", 0),
            "temperature": latest_data.get("temperature", 22),
            "active_devices": latest_data.get("active_devices", []),
            "timestamp": latest_data.get("timestamp", datetime.now().isoformat()),
            "lighting_watt": latest_data.get("lighting_watt", 0),
            "projector_watt": latest_data.get("projector_watt", 0),
            "plug_load_watt": latest_data.get("plug_load_watt", 0),
            "is_anomaly": latest_data.get("is_anomaly", 0),
            "is_weekend": latest_data.get("is_weekend", 0),
            "is_holiday": latest_data.get("is_holiday", 0),
        }
    
    def get_current_room_data(self, room_id: str) -> Dict[str, Any]:
        return self.get_room_current_status(room_id)
    
    def get_all_rooms_current_status(self) -> List[Dict[str, Any]]:
        if not self.rooms_data: return []
        return [self.get_room_current_status(room["room_id"]) for room in self.rooms_data if self.get_room_current_status(room["room_id"])]

