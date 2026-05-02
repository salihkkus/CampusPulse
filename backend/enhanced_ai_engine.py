import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class EnhancedAIEngine:
    """
    Geliştirilmiş AI Motoru
    Isolation Forest + Teşhis Sistemi entegre
    """
    
    def __init__(self, model_path: str = "models/"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_columns = []
        self.model_config = {}
        self.is_trained = False
        
        # Teşhis motorunu yükle
        from diagnosis_engine import DiagnosisEngine
        self.diagnosis_engine = DiagnosisEngine()
        
        # Modeli yükle
        self.load_model()
    
    def load_model(self) -> bool:
        """
        Eğitilmiş modeli yükle
        """
        try:
            # Model dosyalarını kontrol et
            model_file = os.path.join(self.model_path, "isolation_forest_model.pkl")
            scaler_file = os.path.join(self.model_path, "feature_scaler.pkl")
            config_file = os.path.join(self.model_path, "model_config.json")
            
            if not all(os.path.exists(f) for f in [model_file, scaler_file, config_file]):
                print("[WARN] Model dosyalari bulunamadi")
                return False
            
            # Modeli yükle
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
            
            # Scaler'ı yükle
            with open(scaler_file, 'rb') as f:
                self.scaler = pickle.load(f)
            
            # Konfigürasyonu yükle
            with open(config_file, 'r') as f:
                self.model_config = json.load(f)
                self.feature_columns = self.model_config["features"]
            
            self.is_trained = True
            print("[OK] AI Modeli basariyla yuklendi")
            return True
            
        except Exception as e:
            print(f"[ERROR] Model yukleme hatasi: {str(e)}")
            return False
    
    def prepare_features(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Veriyi model için hazırla
        """
        df = pd.DataFrame([data])
        
        # Gerekli feature'ları ekle
        if 'datetime' in data:
            df['datetime'] = pd.to_datetime(data['datetime'])
        else:
            df['datetime'] = pd.to_datetime(data['date'])
        
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Oda tipi özellikleri
        df['room_type'] = data['room_id'].split('_')[1]
        df['is_classroom'] = df['room_type'].isin(['Derslik']).astype(int)
        df['is_office'] = df['room_type'].isin(['HocaOdasi']).astype(int)
        
        # Güç per device
        df['power_per_device'] = data['total_power'] / (data.get('plug_load_watt', 0) + 1)
        
        return df
    
    def predict_anomaly(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anomali tahmini yap
        """
        if not self.is_trained:
            return {
                "error": "Model eğitilmemiş",
                "is_anomaly": False,
                "anomaly_score": 0.0,
                "confidence": 0.0
            }
        
        try:
            # Feature'ları hazırla
            df = self.prepare_features(data)
            
            # Feature'ları seç
            X = df[self.feature_columns]
            
            # Ölçeklendir
            X_scaled = self.scaler.transform(X)
            
            # Tahmin yap
            prediction = self.model.predict(X_scaled)[0]
            score = self.model.decision_function(X_scaled)[0]
            
            return {
                "is_anomaly": bool(prediction == -1),
                "anomaly_score": float(score),
                "confidence": float(abs(score)),
                "prediction": int(prediction),
                "features_used": self.feature_columns
            }
            
        except Exception as e:
            return {
                "error": f"Tahmin hatası: {str(e)}",
                "is_anomaly": False,
                "anomaly_score": 0.0,
                "confidence": 0.0
            }
    
    def comprehensive_analysis(self, room_id: str, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Kapsamlı analiz: Anomali + Teşhis + Finansal
        """
        # Veriyi standard format'a çevir
        analysis_data = {
            "room_id": room_id,
            "timestamp": current_data.get("timestamp", datetime.now().isoformat()),
            "occupancy_status": current_data.get("occupancy_status", 0),
            "hour_of_day": current_data.get("hour_of_day", datetime.now().hour),
            "total_power": current_data.get("power_consumption", 0),  # Düzeltildi
            "lighting_watt": current_data.get("lighting_watt", 0),
            "projector_watt": current_data.get("projector_watt", 0),
            "plug_load_watt": current_data.get("plug_load_watt", 0),
            "is_weekend": current_data.get("is_weekend", 0),
            "is_holiday": current_data.get("is_holiday", 0)
        }
        
        # 1. Anomali tahmini
        anomaly_result = self.predict_anomaly(analysis_data)
        
        # 2. Teşhis analizi
        diagnosis_result = self.diagnosis_engine.diagnose_energy_waste(analysis_data)
        
        # 3. Finansal hesaplama
        financial_result = self._calculate_financial_impact(analysis_data, diagnosis_result)
        
        # 4. Durum belirleme
        status = self._determine_room_status(analysis_data, anomaly_result, diagnosis_result)
        
        # 5. Öneriler
        recommendations = self._generate_recommendations(diagnosis_result, financial_result)
        
        return {
            "room_id": room_id,
            "timestamp": analysis_data["timestamp"],
            "status": status,
            "analysis": {
                "anomaly": anomaly_result,
                "diagnosis": diagnosis_result,
                "financial": financial_result
            },
            "current_data": {
                "power_consumption": analysis_data["total_power"],
                "occupancy_status": analysis_data["occupancy_status"],
                "hour_of_day": analysis_data["hour_of_day"],
                "detected_devices": diagnosis_result.get("detected_devices", [])
            },
            "recommendations": recommendations,
            "urgency_level": diagnosis_result.get("urgency_level", "LOW"),
            "confidence": diagnosis_result.get("confidence", 0.0)
        }
    
    def _calculate_financial_impact(self, data: Dict[str, Any], diagnosis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finansal etkiyi hesapla
        """
        electricity_price = 2.50  # TL/kWh
        carbon_factor = 0.45  # kg CO2/kWh
        
        total_power = data["total_power"]
        
        # Anlık maliyet
        instant_cost_per_hour = (total_power / 1000) * electricity_price
        instant_carbon_per_hour = (total_power / 1000) * carbon_factor
        
        # Günlük tahmin (8 saat)
        daily_cost = instant_cost_per_hour * 8
        daily_carbon = instant_carbon_per_hour * 8
        
        # Aylık tahmin (22 gün)
        monthly_cost = daily_cost * 22
        monthly_carbon = daily_carbon * 22
        
        # İsraf maliyeti
        wasted_cost_per_hour = 0
        wasted_carbon_per_hour = 0
        
        if diagnosis.get("is_wasting", False):
            wasted_cost_per_hour = instant_cost_per_hour
            wasted_carbon_per_hour = instant_carbon_per_hour
        
        return {
            "instant_loss_per_hour": instant_cost_per_hour,
            "daily_cost": daily_cost,
            "monthly_cost": monthly_cost,
            "instant_carbon_per_hour": instant_carbon_per_hour,
            "daily_carbon": daily_carbon,
            "monthly_carbon": monthly_carbon,
            "wasted_cost_per_hour": wasted_cost_per_hour,
            "wasted_carbon_per_hour": wasted_carbon_per_hour,
            "potential_monthly_savings": diagnosis.get("potential_savings", 0.0)
        }
    
    def _determine_room_status(self, data: Dict[str, Any], anomaly: Dict[str, Any], diagnosis: Dict[str, Any]) -> str:
        """
        Oda durumunu belirle
        """
        if diagnosis.get("is_wasting", False):
            urgency = diagnosis.get("urgency_level", "LOW")
            if urgency == "HIGH":
                return "CRITICAL"
            elif urgency == "MEDIUM":
                return "WARNING"
            else:
                return "ATTENTION"
        elif anomaly.get("is_anomaly", False):
            return "ANOMALY"
        elif data["occupancy_status"] == 1:
            return "ACTIVE"
        else:
            return "NORMAL"
    
    def _generate_recommendations(self, diagnosis: Dict[str, Any], financial: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Öneriler oluştur
        """
        recommendations = []
        
        if diagnosis.get("recommendations"):
            for rec in diagnosis["recommendations"]:
                recommendations.append({
                    "type": "action",
                    "title": rec["short"],
                    "description": rec["detailed"],
                    "action": rec["action"],
                    "priority": rec["priority"],
                    "savings": rec["savings"]
                })
        
        # Ek öneriler
        if financial["wasted_cost_per_hour"] > 5.0:
            recommendations.append({
                "type": "system",
                "title": "Otomasyon öner",
                "description": "Bu oda için otomatik kapatma sistemi kurun",
                "action": "Otomasyon sistemi kur",
                "priority": "MEDIUM",
                "savings": f"Ayda ~{financial['potential_monthly_savings']:.0f}TL"
            })
        
        return recommendations
    
    def batch_analyze_rooms(self, rooms_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Toplu oda analizi
        """
        results = []
        summary = {
            "total_rooms": len(rooms_data),
            "wasting_rooms": 0,
            "critical_rooms": 0,
            "total_waste_cost": 0.0,
            "total_potential_savings": 0.0
        }
        
        for room_data in rooms_data:
            room_id = room_data["room_id"]
            analysis = self.comprehensive_analysis(room_id, room_data)
            results.append(analysis)
            
            # Özet güncelle
            if analysis["analysis"]["diagnosis"]["is_wasting"]:
                summary["wasting_rooms"] += 1
                summary["total_waste_cost"] += analysis["analysis"]["financial"]["wasted_cost_per_hour"]
                summary["total_potential_savings"] += analysis["analysis"]["financial"]["potential_monthly_savings"]
            
            if analysis["status"] == "CRITICAL":
                summary["critical_rooms"] += 1
        
        return {
            "summary": summary,
            "rooms": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Model bilgilerini döndür
        """
        if not self.is_trained:
            return {"error": "Model eğitilmemiş"}
        
        return {
            "model_type": "IsolationForest",
            "is_trained": self.is_trained,
            "features": self.feature_columns,
            "training_stats": self.model_config.get("training_stats", {}),
            "model_params": self.model_config.get("model_params", {}),
            "load_timestamp": datetime.now().isoformat()
        }
