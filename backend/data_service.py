import pandas as pd
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
import os

class DataService:
    """
    Eren'in hazırladığı CSV veri dosyasını okuyan ve işleyen servis
    """
    
    def __init__(self, csv_file: str = None):
        if csv_file is None:
            # Determine absolute path to CSV file in the root directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(base_dir)
            self.csv_file = os.path.join(root_dir, "kampus_1_aylik_enerji.csv")
        else:
            self.csv_file = csv_file
            
        self.rooms_data = []
        self.load_csv_data()
    
    def load_csv_data(self):
        """CSV veri dosyasını pandas ile yükle"""
        try:
            if not os.path.exists(self.csv_file):
                print(f"[ERROR] Veri dosyasi bulunamadi: {self.csv_file}")
                print(f"[INFO] Mevcut dizin: {os.getcwd()}")
                self.generate_mock_data()
                return
                
            print(f"[INFO] {self.csv_file} yükleniyor...")
            df = pd.read_csv(self.csv_file)
            
            # Zaman damgasını oluştur
            df['timestamp_dt'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour_of_day'], unit='h')
            df['timestamp'] = df['timestamp_dt'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            df = df.sort_values('timestamp_dt')
            
            # Tüm benzersiz zaman damgalarını al
            self.all_timestamps = sorted(df['timestamp'].unique())
            
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
                        "timestamp": row['timestamp'],
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
                
            # '2023-12-01' tarihine sarkan (UTC+3 kaynaklı) veya direkt Aralık olan verileri temizle
            # 2023-11-30T21:00, 22:00 ve 23:00 UTC, Türkiye'de 01 Aralık 00, 01, 02'ye tekabül eder.
            exclude_ts = ['2023-11-30T21:00:00Z', '2023-11-30T22:00:00Z', '2023-11-30T23:00:00Z']
            self.all_timestamps = [ts for ts in self.all_timestamps if not ts.startswith('2023-12-01') and ts not in exclude_ts]
            for room in self.rooms_data:
                room["time_series"] = [d for d in room["time_series"] if not d["timestamp"].startswith('2023-12-01') and d["timestamp"] not in exclude_ts]
                
            print(f"[OK] CSV Veri yuklendi: {len(self.rooms_data)} oda, {len(self.all_timestamps)} zaman dilimi")
        except Exception as e:
            print(f"[ERROR] CSV yuklenirken hata: {e}")
            self.all_timestamps = []
            self.generate_mock_data()
    
    def generate_mock_data(self):
        """Mock veri oluşturmayı devredışı bırak"""
        self.rooms_data = []
        print("[INFO] Mock veri oluşturma devredışı bırakıldı.")
    
    def _generate_time_series(self, room_id: str, devices: List[str]) -> List[Dict]:
        time_series = []
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for hour in range(24):
            timestamp = (base_time + timedelta(hours=hour)).isoformat() + "Z"
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
                "timestamp": timestamp,
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
    
    def get_available_timestamps(self) -> List[str]:
        return self.all_timestamps
    
    def get_room_history(self, room_id: str, hours: int = 24, end_timestamp: str = None) -> List[Dict]:
        if not self.rooms_data: return []
        room = next((r for r in self.rooms_data if r["room_id"] == room_id), None)
        if not room: return []
        
        all_series = room.get("time_series", [])
        if not end_timestamp:
            return all_series[-hours:]
            
        # Find index of target timestamp
        idx = -1
        for i, data in enumerate(all_series):
            if data["timestamp"] == end_timestamp:
                idx = i
                break
        
        if idx == -1:
            return all_series[-hours:]
            
        start_idx = max(0, idx - hours + 1)
        return all_series[start_idx : idx + 1]
    
    def get_room_current_status(self, room_id: str, target_timestamp: str = None) -> Dict[str, Any]:
        if not self.rooms_data: return None
        room_data = next((room for room in self.rooms_data if room["room_id"] == room_id), None)
        if not room_data: return None
        
        time_series = room_data.get("time_series", [])
        if not time_series: return None
        
        target_data = None
        if target_timestamp:
            target_data = next((d for d in time_series if d["timestamp"] == target_timestamp), None)
            
        if not target_data:
            target_data = time_series[-1]
        
        return {
            "room_id": room_data["room_id"],
            "room_name": room_data["room_name"],
            "building": room_data["building"],
            "floor": room_data["floor"],
            "coordinates": room_data.get("coordinates", {"x": 0, "y": 0, "z": 0}),
            "devices": room_data.get("devices", []),
            "hour_of_day": datetime.fromisoformat(target_data["timestamp"].replace("Z", "+00:00")).hour,
            "power_consumption": target_data.get("power_consumption", 0),
            "current_power": target_data.get("power_consumption", 0),
            "occupancy_status": target_data.get("occupancy_status", 0),
            "temperature": target_data.get("temperature", 22),
            "active_devices": target_data.get("active_devices", []),
            "timestamp": target_data.get("timestamp", datetime.now().isoformat()),
            "lighting_watt": target_data.get("lighting_watt", 0),
            "projector_watt": target_data.get("projector_watt", 0),
            "plug_load_watt": target_data.get("plug_load_watt", 0),
            "is_anomaly": target_data.get("is_anomaly", 0),
            "is_weekend": target_data.get("is_weekend", 0),
            "is_holiday": target_data.get("is_holiday", 0),
        }
    
    def get_current_room_data(self, room_id: str, timestamp: str = None) -> Dict[str, Any]:
        return self.get_room_current_status(room_id, timestamp)
    
    def get_all_rooms_current_status(self, timestamp: str = None) -> List[Dict[str, Any]]:
        if not self.rooms_data: return []
        return [self.get_room_current_status(room["room_id"], timestamp) for room in self.rooms_data if self.get_room_current_status(room["room_id"], timestamp)]

    def get_range_analysis(self, start_date: str, end_date: str, start_hour: int = 0, end_hour: int = 23) -> Dict[str, Any]:
        """Belirli bir tarih ve saat aralığı için toplu analiz yap"""
        if not self.rooms_data: return None
        
        total_waste_tl = 0
        total_power_kwh = 0
        total_carbon_kg = 0
        room_stats = []
        
        # Tarih nesnelerine çevir
        try:
            sd = datetime.strptime(start_date, '%Y-%m-%d').date()
            ed = datetime.strptime(end_date, '%Y-%m-%d').date()
        except:
            return {"error": "Geçersiz tarih formatı. YYYY-MM-DD kullanın."}
        
        for room in self.rooms_data:
            room_waste = 0
            room_power = 0
            count = 0
            
            for d in room["time_series"]:
                dt = datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00"))
                local_dt = dt + timedelta(hours=3)
                curr_date = local_dt.date()
                
                # Tarih aralığında mı?
                if sd <= curr_date <= ed:
                    # Eğer aynı günse saat aralığına bak, farklı günlerdeyse (ara günler) tüm saatlere bak
                    # Veya kullanıcı her gün için aynı saat aralığını istiyor olabilir.
                    # Kullanıcının talebi "12-20 kasım arası" dediği için genellikle her günün o saatlerini kastedebilir.
                    # Ama şimdilik basitçe tüm saatleri alalım eğer tek gün değilse.
                    if sd == ed:
                        in_hour_range = (start_hour <= local_dt.hour <= end_hour)
                    else:
                        in_hour_range = True # Çoklu günde tüm saatleri al
                        
                    if in_hour_range:
                        room_waste += d.get("wasted_cost_tl", 0)
                        room_power += d.get("power_consumption", 0) / 1000.0 # kWh
                        count += 1
            
            if count > 0:
                total_waste_tl += room_waste
                total_power_kwh += room_power
                room_carbon = room_power * 0.5
                total_carbon_kg += room_carbon
                
                room_stats.append({
                    "room_id": room["room_id"],
                    "room_name": room["room_name"],
                    "building": room["building"],
                    "total_waste_tl": round(room_waste, 2),
                    "total_power_kwh": round(room_power, 2),
                    "total_carbon_kg": round(room_carbon, 2),
                    "avg_power_watt": round((room_power * 1000) / count, 2) if count > 0 else 0
                })
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "range_type": "Multi-Day" if sd != ed else "Single-Day",
            "summary": {
                "total_rooms": len(self.rooms_data),
                "analyzed_rooms": len(room_stats),
                "total_waste_tl": round(total_waste_tl, 2),
                "total_power_kwh": round(total_power_kwh, 2),
                "total_carbon_kg": round(total_carbon_kg, 2),
            },
            "rooms": sorted(room_stats, key=lambda x: x["total_waste_tl"], reverse=True)
        }

