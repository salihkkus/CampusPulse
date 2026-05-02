import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import json
from datetime import datetime

print("🤖 AI Model Eğitimi - Basit Test")

try:
    # CSV'i oku
    df = pd.read_csv('../kampus_1_aylik_enerji.csv')
    print(f"✅ CSV okundu: {len(df)} kayıt")
    
    # Feature'lar
    features = ['total_watt', 'hour_of_day', 'is_class_in_session']
    X = df[features].copy()
    
    print(f"📊 Feature'lar: {features}")
    print(f"   total_watt: {X['total_watt'].min():.1f} - {X['total_watt'].max():.1f}")
    print(f"   hour_of_day: {X['hour_of_day'].min()} - {X['hour_of_day'].max()}")
    print(f"   is_class_in_session: {X['is_class_in_session'].unique()}")
    
    # Özellik mühendisliği
    X['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
    X['is_weekend'] = (X['day_of_week'] >= 5).astype(int)
    features.extend(['day_of_week', 'is_weekend'])
    
    print(f"🔧 Ek feature'lar eklendi: {len(features)} toplam")
    
    # Veriyi ölçeklendir
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Model eğitimi
    print("🧠 Isolation Forest eğitiliyor...")
    model = IsolationForest(
        contamination=0.1,  # %10 anomali beklentisi
        random_state=42,
        n_estimators=100
    )
    
    model.fit(X_scaled)
    print("✅ Model eğitildi")
    
    # Tahminler
    predictions = model.predict(X_scaled)  # -1 = anomaly, 1 = normal
    scores = model.decision_function(X_scaled)
    
    # Sonuçları analiz et
    anomalies = (predictions == -1).sum()
    total = len(predictions)
    anomaly_rate = anomalies / total * 100
    
    print(f"🔍 Sonuçlar:")
    print(f"   Toplam kayıt: {total:,}")
    print(f"   Tespit edilen anomali: {anomalies:,}")
    print(f"   Anomali oranı: {anomaly_rate:.2f}%")
    print(f"   Ortalama anomali skoru: {scores.mean():.3f}")
    
    # Gerçek anomalilerle karşılaştır
    actual_anomalies = df['is_anomaly'].sum()
    print(f"   Gerçek anomali: {actual_anomalies:,}")
    
    # Modeli kaydet
    print("💾 Model kaydediliyor...")
    
    # Model
    with open('models/isolation_forest_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Scaler
    with open('models/feature_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Konfigürasyon
    config = {
        "features": features,
        "model_params": {
            "contamination": 0.1,
            "n_estimators": 100,
            "random_state": 42
        },
        "training_stats": {
            "total_samples": total,
            "detected_anomalies": int(anomalies),
            "anomaly_rate": float(anomaly_rate),
            "training_date": datetime.now().isoformat()
        }
    }
    
    with open('models/model_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Model kaydedildi")
    
    # Test tahmini
    print("\n🧪 Test tahmini:")
    test_data = {
        'total_watt': 5000,
        'hour_of_day': 14,
        'is_class_in_session': 1,
        'day_of_week': 2,
        'is_weekend': 0
    }
    
    test_df = pd.DataFrame([test_data])
    test_scaled = scaler.transform(test_df[features])
    test_pred = model.predict(test_scaled)[0]
    test_score = model.decision_function(test_scaled)[0]
    
    print(f"   Test verisi: {test_data}")
    print(f"   Tahmin: {'Anomali' if test_pred == -1 else 'Normal'}")
    print(f"   Skor: {test_score:.3f}")
    
    print("\n🎉 AI Model Eğitimi Başarılı!")
    print("Model artık anomali tespiti için hazır!")
    
except Exception as e:
    print(f"❌ Hata: {str(e)}")
    import traceback
    traceback.print_exc()
