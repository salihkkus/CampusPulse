import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
import logging

class AITrainer:
    """
    Eren'in veri seti ile Isolation Forest modeli eğit
    Anomali tespiti için enerji tüketim pattern'lerini öğren
    """
    
    def __init__(self, csv_file_path: str, model_save_path: str = "models/"):
        self.csv_file_path = csv_file_path
        self.model_save_path = model_save_path
        self.df = None
        self.model = None
        self.scaler = None
        self.feature_columns = ['total_watt', 'hour_of_day', 'is_class_in_session']
        self.training_results = {}
        
        # Model parametreleri
        self.contamination = 0.1  # %10 anomali beklentisi
        self.random_state = 42
        self.n_estimators = 100
        
    def load_and_prepare_data(self) -> Dict[str, Any]:
        """
        CSV'i yükle ve model için hazırla
        """
        try:
            # CSV'i oku
            self.df = pd.read_csv(self.csv_file_path)
            
            # Temel bilgiler
            basic_info = {
                "total_records": len(self.df),
                "training_features": self.feature_columns,
                "date_range": f"{self.df['date'].min()} - {self.df['date'].max()}",
                "unique_rooms": self.df['room_id'].nunique()
            }
            
            # Feature mühendisliği
            self._add_features()
            
            # Veri temizleme ve ön işleme
            self._preprocess_data()
            
            # Özellik istatistikleri
            feature_stats = {}
            for col in self.feature_columns:
                feature_stats[col] = {
                    "min": float(self.df[col].min()),
                    "max": float(self.df[col].max()),
                    "mean": float(self.df[col].mean()),
                    "std": float(self.df[col].std()),
                    "missing": int(self.df[col].isnull().sum())
                }
            
            return {
                "basic_info": basic_info,
                "feature_statistics": feature_stats,
                "data_quality": self._check_data_quality()
            }
            
        except Exception as e:
            return {"error": f"Veri yükleme hatası: {str(e)}"}
    
    def _add_features(self):
        """
        Model için ek özellikler ekle
        """
        # Zaman bazlı özellikler
        self.df['datetime'] = pd.to_datetime(self.df['date'])
        self.df['day_of_week'] = self.df['datetime'].dt.dayofweek  # 0=Monday, 6=Sunday
        self.df['is_weekend_feature'] = (self.df['day_of_week'] >= 5).astype(int)
        
        # Oda tipi özellikleri
        self.df['room_type'] = self.df['room_id'].apply(lambda x: x.split('_')[1])
        self.df['is_classroom'] = self.df['room_type'].isin(['Derslik']).astype(int)
        self.df['is_office'] = self.df['room_type'].isin(['HocaOdasi']).astype(int)
        
        # Güç tüketim özellikleri
        self.df['power_per_device'] = np.where(
            self.df['plug_load_watt'] > 0,
            self.df['total_watt'] / (self.df['plug_load_watt'] + 1),
            self.df['total_watt']
        )
        
        # Eğitim için özellik listesini güncelle
        self.feature_columns = [
            'total_watt', 'hour_of_day', 'is_class_in_session',
            'day_of_week', 'is_weekend_feature', 'is_classroom',
            'is_office', 'power_per_device'
        ]
        
    def _preprocess_data(self):
        """
        Veriyi ön işleme: temizleme, normalizasyon
        """
        # Eksik verileri doldur
        for col in self.feature_columns:
            if self.df[col].isnull().sum() > 0:
                if col in ['total_watt', 'power_per_device']:
                    self.df[col].fillna(0, inplace=True)
                else:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
        
        # Aykırı değerleri temizle (IQR method)
        for col in ['total_watt', 'power_per_device']:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Aykırı değerleri clip'le
            self.df[col] = self.df[col].clip(lower_bound, upper_bound)
    
    def _check_data_quality(self) -> Dict[str, Any]:
        """
        Veri kalitesini kontrol et
        """
        quality_checks = {
            "missing_values": self.df[self.feature_columns].isnull().sum().to_dict(),
            "zero_values": (self.df[self.feature_columns] == 0).sum().to_dict(),
            "negative_values": (self.df[self.feature_columns] < 0).sum().to_dict(),
            "data_types": self.df[self.feature_columns].dtypes.to_dict()
        }
        
        # Veri dağılımı
        quality_checks["distribution"] = {}
        for col in self.feature_columns:
            quality_checks["distribution"][col] = {
                "skewness": float(self.df[col].skew()),
                "kurtosis": float(self.df[col].kurtosis())
            }
        
        return quality_checks
    
    def train_isolation_forest(self) -> Dict[str, Any]:
        """
        Isolation Forest modelini eğit
        """
        try:
            # Eğitim verisi
            X = self.df[self.feature_columns].copy()
            
            # Veriyi ölçeklendir
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Model oluştur ve eğit
            self.model = IsolationForest(
                contamination=self.contamination,
                n_estimators=self.n_estimators,
                random_state=self.random_state,
                max_samples='auto',
                max_features=1.0
            )
            
            # Modeli eğit
            self.model.fit(X_scaled)
            
            # Tahminler
            y_pred = self.model.predict(X_scaled)  # -1 = anomaly, 1 = normal
            y_scores = self.model.decision_function(X_scaled)  # Anomaly scores
            
            # Sonuçları dataframe'e ekle
            self.df['predicted_anomaly'] = y_pred
            self.df['anomaly_score'] = y_scores
            self.df['predicted_anomaly_binary'] = (y_pred == -1).astype(int)
            
            # Model performansı
            actual_anomalies = self.df['is_anomaly']
            predicted_anomalies = self.df['predicted_anomaly_binary']
            
            # Confusion matrix
            tn, fp, fn, tp = confusion_matrix(actual_anomalies, predicted_anomalies).ravel()
            
            # Metrikler
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            accuracy = (tp + tn) / (tp + tn + fp + fn)
            
            # Feature importance (decision function'a göre)
            feature_importance = self._calculate_feature_importance(X_scaled, y_scores)
            
            training_results = {
                "model_info": {
                    "model_type": "IsolationForest",
                    "contamination": self.contamination,
                    "n_estimators": self.n_estimators,
                    "training_samples": len(X),
                    "features_used": self.feature_columns
                },
                "performance_metrics": {
                    "accuracy": float(accuracy),
                    "precision": float(precision),
                    "recall": float(recall),
                    "f1_score": float(f1_score),
                    "true_positives": int(tp),
                    "true_negatives": int(tn),
                    "false_positives": int(fp),
                    "false_negatives": int(fn)
                },
                "anomaly_analysis": {
                    "total_anomalies_detected": int(predicted_anomalies.sum()),
                    "actual_anomalies": int(actual_anomalies.sum()),
                    "anomaly_rate": float(predicted_anomalies.mean()),
                    "avg_anomaly_score": float(y_scores.mean()),
                    "anomaly_score_range": {
                        "min": float(y_scores.min()),
                        "max": float(y_scores.max())
                    }
                },
                "feature_importance": feature_importance,
                "training_timestamp": datetime.now().isoformat()
            }
            
            self.training_results = training_results
            return training_results
            
        except Exception as e:
            return {"error": f"Model eğitimi hatası: {str(e)}"}
    
    def _calculate_feature_importance(self, X_scaled: np.ndarray, y_scores: np.ndarray) -> Dict[str, float]:
        """
        Feature importance hesapla (correlation based)
        """
        feature_importance = {}
        
        for i, feature in enumerate(self.feature_columns):
            # Feature ile anomaly score arasındaki korelasyon
            correlation = np.corrcoef(X_scaled[:, i], y_scores)[0, 1]
            feature_importance[feature] = abs(float(correlation))
        
        # Sırala
        feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        return feature_importance
    
    def analyze_anomaly_patterns(self) -> Dict[str, Any]:
        """
        Tespit edilen anomalileri analiz et
        """
        if self.df is None or 'predicted_anomaly_binary' not in self.df.columns:
            return {"error": "Model eğitilmemiş veya tahmin yapılmamış"}
        
        anomalies = self.df[self.df['predicted_anomaly_binary'] == 1]
        normal_data = self.df[self.df['predicted_anomaly_binary'] == 0]
        
        # Zaman bazlı analiz
        time_analysis = {
            "anomaly_by_hour": anomalies['hour_of_day'].value_counts().to_dict(),
            "anomaly_by_day_of_week": anomalies['day_of_week'].value_counts().to_dict(),
            "anomaly_by_room_type": anomalies['room_type'].value_counts().to_dict()
        }
        
        # Özellik bazlı analiz
        feature_analysis = {}
        for feature in ['total_watt', 'hour_of_day', 'is_class_in_session']:
            feature_analysis[feature] = {
                "normal_mean": float(normal_data[feature].mean()),
                "normal_std": float(normal_data[feature].std()),
                "anomaly_mean": float(anomalies[feature].mean()),
                "anomaly_std": float(anomalies[feature].std())
            }
        
        # Oda bazlı analiz
        room_analysis = anomalies.groupby('room_id').agg({
            'predicted_anomaly_binary': 'count',
            'total_watt': 'mean',
            'anomaly_score': 'mean'
        }).round(2)
        
        room_analysis.columns = ['anomaly_count', 'avg_power', 'avg_anomaly_score']
        room_analysis = room_analysis.sort_values('anomaly_count', ascending=False)
        
        return {
            "time_patterns": time_analysis,
            "feature_patterns": feature_analysis,
            "room_analysis": room_analysis.head(10).to_dict('index'),
            "total_anomalies": len(anomalies),
            "anomaly_percentage": float(len(anomalies) / len(self.df) * 100)
        }
    
    def save_model(self) -> Dict[str, Any]:
        """
        Eğitilmiş modeli kaydet
        """
        try:
            import os
            os.makedirs(self.model_save_path, exist_ok=True)
            
            # Modeli kaydet
            model_file = f"{self.model_save_path}isolation_forest_model.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(self.model, f)
            
            # Scaler'ı kaydet
            scaler_file = f"{self.model_save_path}feature_scaler.pkl"
            with open(scaler_file, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            # Eğitim sonuçlarını kaydet
            results_file = f"{self.model_save_path}training_results.json"
            with open(results_file, 'w') as f:
                json.dump(self.training_results, f, indent=2, default=str)
            
            # Feature listesini kaydet
            config_file = f"{self.model_save_path}model_config.json"
            config = {
                "feature_columns": self.feature_columns,
                "model_params": {
                    "contamination": self.contamination,
                    "n_estimators": self.n_estimators,
                    "random_state": self.random_state
                },
                "training_date": datetime.now().isoformat()
            }
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return {
                "success": True,
                "model_file": model_file,
                "scaler_file": scaler_file,
                "results_file": results_file,
                "config_file": config_file,
                "message": "Model ve bileşenleri başarıyla kaydedildi"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Model kaydetme hatası: {str(e)}"}
    
    def load_model(self) -> Dict[str, Any]:
        """
        Kaydedilmiş modeli yükle
        """
        try:
            # Modeli yükle
            model_file = f"{self.model_save_path}isolation_forest_model.pkl"
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
            
            # Scaler'ı yükle
            scaler_file = f"{self.model_save_path}feature_scaler.pkl"
            with open(scaler_file, 'rb') as f:
                self.scaler = pickle.load(f)
            
            # Konfigürasyonu yükle
            config_file = f"{self.model_save_path}model_config.json"
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.feature_columns = config["feature_columns"]
            
            # Eğitim sonuçlarını yükle
            results_file = f"{self.model_save_path}training_results.json"
            with open(results_file, 'r') as f:
                self.training_results = json.load(f)
            
            return {
                "success": True,
                "message": "Model başarıyla yüklendi",
                "model_info": self.training_results.get("model_info", {}),
                "performance": self.training_results.get("performance_metrics", {})
            }
            
        except Exception as e:
            return {"success": False, "error": f"Model yükleme hatası: {str(e)}"}
    
    def predict_anomaly(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Yeni veri için anomali tahmini yap
        """
        if self.model is None or self.scaler is None:
            return {"error": "Model eğitilmemiş"}
        
        try:
            # Veriyi DataFrame'e çevir
            df_input = pd.DataFrame([data])
            
            # Feature'ları ekle
            df_input['datetime'] = pd.to_datetime(data['date'])
            df_input['day_of_week'] = df_input['datetime'].dt.dayofweek
            df_input['is_weekend_feature'] = (df_input['day_of_week'] >= 5).astype(int)
            df_input['room_type'] = data['room_id'].split('_')[1]
            df_input['is_classroom'] = int(df_input['room_type'].isin(['Derslik']))
            df_input['is_office'] = int(df_input['room_type'].isin(['HocaOdasi']))
            df_input['power_per_device'] = data['total_watt'] / (data.get('plug_load_watt', 0) + 1)
            
            # Feature'ları seç
            X = df_input[self.feature_columns]
            
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
            return {"error": f"Tahmin hatası: {str(e)}"}
    
    def generate_training_report(self) -> str:
        """
        Eğitim raporu oluştur
        """
        if not self.training_results:
            return "Eğitim sonuçları bulunamadı"
        
        model_info = self.training_results.get("model_info", {})
        performance = self.training_results.get("performance_metrics", {})
        anomaly = self.training_results.get("anomaly_analysis", {})
        
        report = f"""
🤖 AI MODEL EĞİTİM RAPORU
========================

📊 Model Bilgileri:
- Model Tipi: {model_info.get('model_type', 'N/A')}
- Eğitim Örnekleri: {model_info.get('training_samples', 'N/A'):,}
- Kullanılan Feature'lar: {', '.join(model_info.get('features_used', []))}
- Contamination: {model_info.get('contamination', 'N/A')}
- Estimators: {model_info.get('n_estimators', 'N/A')}

📈 Performans Metrikleri:
- Accuracy: {performance.get('accuracy', 0):.3f}
- Precision: {performance.get('precision', 0):.3f}
- Recall: {performance.get('recall', 0):.3f}
- F1 Score: {performance.get('f1_score', 0):.3f}
- True Positives: {performance.get('true_positives', 0):,}
- False Positives: {performance.get('false_positives', 0):,}

🔍 Anomali Analizi:
- Tespit Edilen Anomali: {anomaly.get('total_anomalies_detected', 0):,}
- Gerçek Anomali: {anomaly.get('actual_anomalies', 0):,}
- Anomali Oranı: {anomaly.get('anomaly_rate', 0):.3f}
- Ortalama Anomali Skoru: {anomaly.get('avg_anomaly_score', 0):.3f}

⏰ Eğitim Zamanı: {self.training_results.get('training_timestamp', 'N/A')}
"""
        
        return report
