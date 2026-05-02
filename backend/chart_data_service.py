import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta
from data_service import DataService
from ai_engine import AIEngine

class ChartDataService:
    """
    Rapor Grafikleri İçin Veri Servisi
    Frontend'de Chart.js, Recharts gibi kütüphanelerle uyumlu veri formatları
    """
    
    def __init__(self, data_service=None, ai_engine=None):
        self.data_service = data_service if data_service else DataService()
        self.ai_engine = ai_engine if ai_engine else AIEngine()
    
    def prepare_time_series_data(self, room_id: str, days: int = 7) -> Dict:
        """
        Zaman serisi grafiği için veri hazırla
        Güç tüketimi, doluluk, israf trendleri
        """
        # Geçmiş veriyi al
        history = self.data_service.get_room_history(room_id, days * 24)
        
        if not history:
            return {"error": f"No data found for room {room_id}"}
        
        # DataFrame'e çevir
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Saatlik verileri günlük olarak grupla
        df['date'] = df['timestamp'].dt.date
        daily_data = df.groupby('date').agg({
            'power_consumption': ['mean', 'max', 'min'],
            'occupancy_status': 'mean',
            'temperature': 'mean'
        }).round(2)
        
        # Sütunları düzleştir
        daily_data.columns = ['avg_power', 'max_power', 'min_power', 'avg_occupancy', 'avg_temp']
        daily_data = daily_data.reset_index()
        
        # Tarih formatını ayarla
        daily_data['date'] = daily_data['date'].astype(str)
        
        return {
            "chart_type": "time_series",
            "room_id": room_id,
            "period": f"{days} days",
            "data": {
                "labels": daily_data['date'].tolist(),
                "datasets": [
                    {
                        "label": "Ortalama Güç (W)",
                        "data": daily_data['avg_power'].tolist(),
                        "borderColor": "rgb(75, 192, 192)",
                        "backgroundColor": "rgba(75, 192, 192, 0.2)",
                        "yAxisID": "y"
                    },
                    {
                        "label": "Maksimum Güç (W)",
                        "data": daily_data['max_power'].tolist(),
                        "borderColor": "rgb(255, 99, 132)",
                        "backgroundColor": "rgba(255, 99, 132, 0.2)",
                        "yAxisID": "y"
                    },
                    {
                        "label": "Doluluk Oranı (%)",
                        "data": (daily_data['avg_occupancy'] * 100).tolist(),
                        "borderColor": "rgb(54, 162, 235)",
                        "backgroundColor": "rgba(54, 162, 235, 0.2)",
                        "yAxisID": "y1"
                    }
                ]
            }
        }
    
    def prepare_waste_comparison_chart(self) -> Dict:
        """
        Odalar arası israf karşılaştırma grafiği
        Bar chart formatında
        """
        rooms_data = self.data_service.get_all_rooms_current_status()
        waste_data = []
        
        for room_data in rooms_data:
            room_id = room_data["room_id"]
            room_history = self.data_service.get_room_history(room_id, 24)
            
            # AI analizini al
            ai_analysis = self.ai_engine.comprehensive_analysis(room_id, room_data, room_history)
            
            if ai_analysis.get("is_wasting_energy", False):
                waste_data.append({
                    "room_id": room_id,
                    "room_name": room_data["room_name"],
                    "waste_percentage": ai_analysis.get("waste_percentage", 0),
                    "instant_loss_tl": ai_analysis.get("instant_loss_tl_per_hour", 0),
                    "current_power": room_data["current_power"]
                })
        
        # İsraf yüzdesine göre sırala
        waste_data.sort(key=lambda x: x["waste_percentage"], reverse=True)
        
        return {
            "chart_type": "bar_chart",
            "title": "Odalar Arası Enerji İsrafı Karşılaştırması",
            "data": {
                "labels": [item["room_name"] for item in waste_data],
                "datasets": [
                    {
                        "label": "İsraf Yüzdesi (%)",
                        "data": [item["waste_percentage"] for item in waste_data],
                        "backgroundColor": "rgba(255, 99, 132, 0.8)",
                        "borderColor": "rgba(255, 99, 132, 1)",
                        "borderWidth": 1,
                        "yAxisID": "y"
                    },
                    {
                        "label": "Saatlik Kayıp (TL)",
                        "data": [item["instant_loss_tl"] for item in waste_data],
                        "backgroundColor": "rgba(54, 162, 235, 0.8)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "borderWidth": 1,
                        "yAxisID": "y1"
                    }
                ]
            }
        }
    
    def prepare_device_breakdown_chart(self, room_id: str = None) -> Dict:
        """
        Cihaz bazında enerji tüketim dağılımı
        Pie chart formatında
        """
        if room_id:
            # Tek oda için cihaz dağılımı
            room_data = self.data_service.get_current_room_data(room_id)
            if not room_data:
                return {"error": f"Room {room_id} not found"}
            
            room_history = self.data_service.get_room_history(room_id, 24)
            ai_analysis = self.ai_engine.comprehensive_analysis(room_id, room_data, room_history)
            
            device_breakdown = ai_analysis.get("device_cost_breakdown", {})
            
            labels = []
            data = []
            colors = []
            
            color_map = {
                "klima": "rgba(255, 99, 132, 0.8)",
                "projeksiyon": "rgba(54, 162, 235, 0.8)",
                "pc": "rgba(255, 206, 86, 0.8)",
                "pc_20_adet": "rgba(75, 192, 192, 0.8)",
                "aydınlatma": "rgba(153, 102, 255, 0.8)",
                "server": "rgba(255, 159, 64, 0.8)"
            }
            
            device_names = {
                "klima": "Klima",
                "projeksiyon": "Projeksiyon",
                "pc": "PC",
                "pc_20_adet": "PC'ler (20 Adet)",
                "aydınlatma": "Aydınlatma",
                "server": "Sunucu"
            }
            
            for device, info in device_breakdown.items():
                labels.append(device_names.get(device, device))
                data.append(info.get("estimated_power_watts", 0))
                colors.append(color_map.get(device, "rgba(201, 203, 207, 0.8)"))
            
            title = f"{room_data['room_name']} - Cihaz Enerji Dağılımı"
        else:
            # Tüm bina için cihaz dağılımı
            rooms_data = self.data_service.get_all_rooms_current_status()
            all_devices = {}
            
            for room_data in rooms_data:
                room_id = room_data["room_id"]
                room_history = self.data_service.get_room_history(room_id, 24)
                ai_analysis = self.ai_engine.comprehensive_analysis(room_id, room_data, room_history)
                
                device_breakdown = ai_analysis.get("device_cost_breakdown", {})
                for device, info in device_breakdown.items():
                    if device not in all_devices:
                        all_devices[device] = 0
                    all_devices[device] += info.get("estimated_power_watts", 0)
            
            labels = []
            data = []
            colors = []
            
            color_map = {
                "klima": "rgba(255, 99, 132, 0.8)",
                "projeksiyon": "rgba(54, 162, 235, 0.8)",
                "pc": "rgba(255, 206, 86, 0.8)",
                "pc_20_adet": "rgba(75, 192, 192, 0.8)",
                "aydınlatma": "rgba(153, 102, 255, 0.8)",
                "server": "rgba(255, 159, 64, 0.8)"
            }
            
            device_names = {
                "klima": "Klima",
                "projeksiyon": "Projeksiyon",
                "pc": "PC",
                "pc_20_adet": "PC'ler",
                "aydınlatma": "Aydınlatma",
                "server": "Sunucu"
            }
            
            for device, power in all_devices.items():
                labels.append(device_names.get(device, device))
                data.append(power)
                colors.append(color_map.get(device, "rgba(201, 203, 207, 0.8)"))
            
            title = "Tüm Bina - Cihaz Enerji Dağılımı"
        
        return {
            "chart_type": "pie_chart",
            "title": title,
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "data": data,
                        "backgroundColor": colors,
                        "borderColor": "rgba(255, 255, 255, 1)",
                        "borderWidth": 2
                    }
                ]
            }
        }
    
    def prepare_financial_trend_chart(self, days: int = 30) -> Dict:
        """
        Finansal trend grafiği
        Günlük toplam maliyet ve karbon emisyonu
        """
        rooms_data = self.data_service.get_all_rooms_current_status()
        
        # Son günler için sentetik veri oluştur (gerçek veri gelince değişecek)
        dates = []
        daily_costs = []
        daily_carbon = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            dates.append(date.strftime("%Y-%m-%d"))
            
            # Rastgele ama trend içeren veriler
            base_cost = 50 + (i * 0.5)  # Artan trend
            base_carbon = 10 + (i * 0.1)
            
            daily_cost = base_cost + np.random.normal(0, 10)
            daily_carbon_value = base_carbon + np.random.normal(0, 2)
            
            daily_costs.append(max(0, daily_cost))
            daily_carbon.append(max(0, daily_carbon_value))
        
        return {
            "chart_type": "financial_trend",
            "title": f"Son {days} Günlük Finansal Trend",
            "data": {
                "labels": dates,
                "datasets": [
                    {
                        "label": "Günlük Toplam Maliyet (TL)",
                        "data": [round(cost, 2) for cost in daily_costs],
                        "borderColor": "rgb(255, 99, 132)",
                        "backgroundColor": "rgba(255, 99, 132, 0.2)",
                        "yAxisID": "y",
                        "type": "line"
                    },
                    {
                        "label": "Günlük Karbon Emisyonu (kg CO2)",
                        "data": [round(carbon, 2) for carbon in daily_carbon],
                        "borderColor": "rgb(75, 192, 192)",
                        "backgroundColor": "rgba(75, 192, 192, 0.2)",
                        "yAxisID": "y1",
                        "type": "bar"
                    }
                ]
            }
        }
    
    def prepare_occupancy_efficiency_chart(self) -> Dict:
        """
        Doluluk vs Verimlilik grafiği
        Scatter plot formatında
        """
        rooms_data = self.data_service.get_all_rooms_current_status()
        
        scatter_data = []
        
        for room_data in rooms_data:
            room_id = room_data["room_id"]
            room_history = self.data_service.get_room_history(room_id, 24)
            
            # AI analizini al
            ai_analysis = self.ai_engine.comprehensive_analysis(room_id, room_data, room_history)
            
            # Doluluk ve verimlilik hesapla
            avg_occupancy = 0
            if room_history:
                avg_occupancy = sum(item["occupancy_status"] for item in room_history) / len(room_history) * 100
            
            efficiency = 100 - ai_analysis.get("waste_percentage", 0)
            
            scatter_data.append({
                "x": avg_occupancy,
                "y": efficiency,
                "room_id": room_id,
                "room_name": room_data["room_name"],
                "current_power": room_data["current_power"]
            })
        
        return {
            "chart_type": "scatter_plot",
            "title": "Doluluk vs Enerji Verimliliği",
            "data": {
                "datasets": [
                    {
                        "label": "Odalar",
                        "data": scatter_data,
                        "backgroundColor": "rgba(54, 162, 235, 0.6)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "pointRadius": 8,
                        "pointHoverRadius": 10
                    }
                ]
            },
            "options": {
                "scales": {
                    "x": {
                        "title": {
                            "display": True,
                            "text": "Doluluk Oranı (%)"
                        },
                        "min": 0,
                        "max": 100
                    },
                    "y": {
                        "title": {
                            "display": True,
                            "text": "Enerji Verimliliği (%)"
                        },
                        "min": 0,
                        "max": 100
                    }
                }
            }
        }
    
    def prepare_dashboard_summary(self) -> Dict:
        """
        Dashboard için tüm grafiklerin özeti
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "charts": {
                "waste_comparison": self.prepare_waste_comparison_chart(),
                "device_breakdown": self.prepare_device_breakdown_chart(),
                "financial_trend": self.prepare_financial_trend_chart(7),
                "occupancy_efficiency": self.prepare_occupancy_efficiency_chart()
            },
            "summary_stats": {
                "total_rooms": len(self.data_service.get_all_rooms_current_status()),
                "wasting_rooms": len([r for r in self.data_service.get_all_rooms_current_status() 
                                    if r["current_power"] > 50 and r["occupancy_status"] == 0]),
                "total_power": sum(r["current_power"] for r in self.data_service.get_all_rooms_current_status()),
                "avg_occupancy": np.mean([r["occupancy_status"] for r in self.data_service.get_all_rooms_current_status()]) * 100
            }
        }
