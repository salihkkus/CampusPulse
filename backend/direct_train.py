import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import json
import os
from datetime import datetime

print("🤖 AI Model Eğitimi - Direkt Çalıştırma")

# CSV dosya yolu
csv_path = "../kampus_1_aylik_enerji.csv"
models_path = "models"

# Models klasörünü oluştur
os.makedirs(models_path, exist_ok=True)

try:
    # 1. Veriyi yükle
    print("📊 Veri yükleniyor...")
    df = pd.read_csv(csv_path)
    print(f"✅ {len(df):,} kayıt yüklendi")
    
    # 2. Feature'ları hazırla
    print("🔧 Feature'lar hazırlanıyor...")
    features = ['total_watt', 'hour_of_day', 'is_class_in_session']
    X = df[features].copy()
    
    # Ek feature'lar
    X['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
    X['is_weekend'] = (X['day_of_week'] >= 5).astype(int)
    features.extend(['day_of_week', 'is_weekend'])
    
    print(f"✅ {len(features)} feature hazırlandı")
    
    # 3. Veri istatistikleri
    print("📈 Veri istatistikleri:")
    for feature in features:
        print(f"   {feature}: {X[feature].min():.1f} - {X[feature].max():.1f}")
    
    # 4. Veriyi ölçeklendir
    print("⚖️ Veri ölçekleniyor...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("✅ Veri ölçeklendi")
    
    # 5. Model eğitimi
    print("🧠 Isolation Forest eğitiliyor...")
    model = IsolationForest(
        contamination=0.1,
        random_state=42,
        n_estimators=100
    )
    
    model.fit(X_scaled)
    print("✅ Model eğitildi")
    
    # 6. Tahminler
    predictions = model.predict(X_scaled)
    scores = model.decision_function(X_scaled)
    
    anomalies = (predictions == -1).sum()
    total = len(predictions)
    anomaly_rate = anomalies / total * 100
    
    print("🔍 Sonuçlar:")
    print(f"   Toplam kayıt: {total:,}")
    print(f"   Anomali: {anomalies:,}")
    print(f"   Anomali oranı: {anomaly_rate:.2f}%")
    print(f"   Ortalama skor: {scores.mean():.3f}")
    
    # 7. Modeli kaydet
    print("💾 Model kaydediliyor...")
    
    # Model
    with open(os.path.join(models_path, 'isolation_forest_model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    # Scaler
    with open(os.path.join(models_path, 'feature_scaler.pkl'), 'wb') as f:
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
            "total_samples": int(total),
            "detected_anomalies": int(anomalies),
            "anomaly_rate": float(anomaly_rate),
            "avg_score": float(scores.mean()),
            "training_date": datetime.now().isoformat()
        }
    }
    
    with open(os.path.join(models_path, 'model_config.json'), 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Model kaydedildi")
    
    # 8. Test
    print("🧪 Test yapılıyor...")
    test_data = pd.DataFrame([{
        'total_watt': 5000,
        'hour_of_day': 14,
        'is_class_in_session': 1,
        'day_of_week': 2,
        'is_weekend': 0
    }])
    
    test_scaled = scaler.transform(test_data[features])
    test_pred = model.predict(test_scaled)[0]
    test_score = model.decision_function(test_scaled)[0]
    
    print(f"   Test sonucu: {'Anomali' if test_pred == -1 else 'Normal'}")
    print(f"   Test skoru: {test_score:.3f}")
    
    print("\n🎉 AI Model Eğitimi Başarılı!")
    print("Model anomali tespiti için hazır!")
    
    # 9. Özet rapor
    print("\n📋 Eğitim Özeti:")
    print(f"   Veri seti: {len(df):,} kayıt")
    print(f"   Feature'lar: {len(features)} adet")
    print(f"   Model: Isolation Forest")
    print(f"   Anomali oranı: {anomaly_rate:.2f}%")
    print(f"   Eğitim süresi: {datetime.now().strftime('%H:%M:%S')}")
    
except FileNotFoundError:
    print(f"❌ CSV dosyası bulunamadı: {csv_path}")
except Exception as e:
    print(f"❌ Hata: {str(e)}")
    import traceback
    traceback.print_exc()
