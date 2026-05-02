import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta
from financial_calculator import FinancialCalculator

class AIEngine:
    """
    Çift Katmanlı Analiz Motoru
    Katman A: Kural Bazlı (Hızlı Tepki)
    Katman B: ML - Anomali Tespit (Isolation Forest)
    """
    
    def __init__(self):
        self.device_power_signatures = {
            "klima": {"min_power": 800, "max_power": 2000, "typical": 1200},
            "projeksiyon": {"min_power": 200, "max_power": 500, "typical": 300},
            "pc": {"min_power": 100, "max_power": 300, "typical": 200},
            "pc_20_adet": {"min_power": 2000, "max_power": 4000, "typical": 3000},
            "aydınlatma": {"min_power": 50, "max_power": 200, "typical": 100},
            "server": {"min_power": 500, "max_power": 1500, "typical": 800}
        }
        
        # ML Model için scaler
        self.scaler = StandardScaler()
        self.isolation_model = IsolationForest(
            n_estimators=100,
            contamination=0.1,  # %10 anomalisi bekliyoruz
            random_state=42
        )
        self.model_trained = False
        
        # Normal tüketim profilleri
        self.normal_consumption_profiles = {}
        
        # Finansal hesaplayıcı
        self.financial_calculator = FinancialCalculator()
    
    def katman_a_kural_bazli_analiz(self, room_data: Dict) -> Dict:
        """
        Katman A: Kural Bazlı Analiz - Hızlı Tepki
        Doluluk = 0 ve Watt > 50 ise -> WASTE (İSRAF)
        """
        occupancy = room_data["occupancy_status"]
        current_power = room_data["current_power"]
        
        # Temel israf tespiti
        is_wasting = occupancy == 0 and current_power > 50
        
        # Cihaz tahmini (watt değerine göre)
        detected_devices = self.detect_devices_by_power(current_power)
        
        # İsraf yüzdesi
        waste_percentage = 0
        if is_wasting:
            waste_percentage = min((current_power / 1000) * 100, 100)
        
        return {
            "is_wasting": is_wasting,
            "waste_percentage": waste_percentage,
            "detected_devices": detected_devices,
            "analysis_type": "rule_based",
            "confidence": 0.95 if is_wasting else 0.8
        }
    
    def detect_devices_by_power(self, power: float) -> List[str]:
        """Watt değerine göre cihaz tahmini"""
        detected = []
        
        for device, signature in self.device_power_signatures.items():
            if signature["min_power"] <= power <= signature["max_power"]:
                detected.append(device)
        
        # Eğer tam eşleşme yoksa yaklaştırarak tahmin et
        if not detected:
            if power > 1500:
                detected.append("klima")
            elif power > 800:
                detected.append("pc_20_adet")
            elif power > 300:
                detected.append("pc")
            elif power > 150:
                detected.append("projeksiyon")
            else:
                detected.append("aydınlatma")
        
        return detected
    
    def katman_b_ml_anomali_tespiti(self, room_history: List[Dict]) -> Dict:
        """
        Katman B: ML - Anomali Tespit
        Isolation Forest ile normal dışı tüketimleri tespit et
        """
        if len(room_history) < 10:  # Yetersiz veri
            return {
                "is_anomaly": False,
                "anomaly_score": 0.0,
                "analysis_type": "ml_insufficient_data",
                "confidence": 0.0
            }
        
        # DataFrame'e çevir
        df = pd.DataFrame(room_history)
        
        # Özellikler: güç tüketimi, doluluk, saat, sıcaklık
        features = []
        for _, row in df.iterrows():
            timestamp = datetime.fromisoformat(row["timestamp"])
            hour = timestamp.hour
            
            feature_vector = [
                row["power_consumption"],
                row["occupancy_status"],
                hour,  # saat
                row.get("temperature", 22)
            ]
            features.append(feature_vector)
        
        features = np.array(features)
        
        # Modeli eğit (daha önce eğitilmemişse)
        if not self.model_trained:
            self.isolation_model.fit(features)
            self.model_trained = True
        
        # Anomali tespiti
        anomaly_scores = self.isolation_model.decision_function(features)
        predictions = self.isolation_model.predict(features)
        
        # En son değerin anomali durumu
        latest_prediction = predictions[-1]
        latest_score = anomaly_scores[-1]
        
        is_anomaly = bool(latest_prediction == -1)
        
        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": float(abs(latest_score)),
            "analysis_type": "ml_isolation_forest",
            "confidence": float(min(abs(latest_score) * 2, 1.0))
        }
    
    def train_model_with_room_data(self, room_id: str, historical_data: List[Dict]):
        """
        Belirli bir oda için modeli eğit
        Normal tüketim profillerini öğren
        """
        if len(historical_data) < 20:
            return False
        
        df = pd.DataFrame(historical_data)
        
        # Sadece normal durumlar (dolu ve boş ama normal tüketim)
        normal_data = []
        for _, row in df.iterrows():
            power = row["power_consumption"]
            occupancy = row["occupancy_status"]
            
            # Normal kabul ettiğimiz durumlar
            if occupancy == 1 and power < 2000:  # Dolu ve normal tüketim
                normal_data.append(row)
            elif occupancy == 0 and power < 100:  # Boş ve minimum tüketim
                normal_data.append(row)
        
        if len(normal_data) < 10:
            return False
        
        # Özellikleri çıkar
        features = []
        for row in normal_data:
            timestamp = datetime.fromisoformat(row["timestamp"])
            hour = timestamp.hour
            
            feature_vector = [
                row["power_consumption"],
                row["occupancy_status"],
                hour,
                row.get("temperature", 22)
            ]
            features.append(feature_vector)
        
        features = np.array(features)
        
        # Modeli eğit
        self.isolation_model.fit(features)
        self.model_trained = True
        
        # Normal profil kaydet
        self.normal_consumption_profiles[room_id] = {
            "avg_power": np.mean([row["power_consumption"] for row in normal_data]),
            "std_power": np.std([row["power_consumption"] for row in normal_data]),
            "training_size": len(normal_data)
        }
        
        return True
    
    def comprehensive_analysis(self, room_id: str, current_data: Dict, history: List[Dict]) -> Dict:
        """
        Çift katmanlı kapsamlı analiz
        Hem kural bazlı hem de ML analizini birleştir
        Finansal ve karbon çıktıları ekler
        """
        # Katman A: Kural Bazlı
        rule_result = self.katman_a_kural_bazli_analiz(current_data)
        
        # Katman B: ML Anomali Tespit
        ml_result = self.katman_b_ml_anomali_tespiti(history)
        
        # Sonuçları birleştir
        base_result = {
            "room_id": room_id,
            "timestamp": current_data.get("timestamp", datetime.now().isoformat()),
            "current_power": current_data["current_power"],
            "occupancy_status": current_data["occupancy_status"],
            
            # Kural bazlı sonuçlar
            "is_wasting_energy": rule_result["is_wasting"],
            "waste_percentage": rule_result["waste_percentage"],
            "detected_devices": rule_result["detected_devices"],
            
            # ML sonuçları
            "is_anomaly": ml_result["is_anomaly"],
            "anomaly_score": ml_result["anomaly_score"],
            
            # Kombine analiz
            "needs_attention": rule_result["is_wasting"] or ml_result["is_anomaly"],
            "urgency_level": self.calculate_urgency(rule_result, ml_result),
            
            # Meta bilgi
            "analysis_confidence": (rule_result["confidence"] + ml_result["confidence"]) / 2,
            "analysis_methods": [rule_result["analysis_type"], ml_result["analysis_type"]]
        }
        
        # Finansal ve karbon hesaplamaları ekle
        financial_result = self.financial_calculator.calculate_comprehensive_financials(current_data, base_result)
        
        # Birleştirilmiş sonuç
        final_result = {**base_result, **financial_result}
        
        return final_result
    
    def calculate_urgency(self, rule_result: Dict, ml_result: Dict) -> str:
        """Aciliyet seviyesini hesapla"""
        if rule_result["is_wasting"] and ml_result["is_anomaly"]:
            return "critical"
        elif rule_result["is_wasting"]:
            return "high"
        elif ml_result["is_anomaly"]:
            return "medium"
        else:
            return "low"
    
    def get_device_waste_breakdown(self, devices: List[str], waste_percentage: float) -> Dict:
        """Cihaz bazında israf dağılımı"""
        breakdown = {}
        
        for device in devices:
            if device in self.device_power_signatures:
                signature = self.device_power_signatures[device]
                device_waste = (signature["typical"] / 1000) * waste_percentage
                breakdown[device] = round(device_waste, 2)
        
        return breakdown
