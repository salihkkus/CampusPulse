# Manuel AI Model Eğitimi
# Bu dosyayı doğrudan çalıştırın: python manual_train.py

print("🤖 AI Model Eğitimi - Manuel Çalıştırma")

# Kütüphaneler
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import json
import os
from datetime import datetime

# 1. CSV oku
print("1️⃣ CSV okunuyor...")
df = pd.read_csv("../kampus_1_aylik_enerji.csv")
print(f"   ✅ {len(df)} kayıt okundu")

# 2. Feature'lar
print("2️⃣ Feature'lar hazırlanıyor...")
features = ['total_watt', 'hour_of_day', 'is_class_in_session']
X = df[features].copy()

# Ek feature'lar
X['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
X['is_weekend'] = (X['day_of_week'] >= 5).astype(int)
features.extend(['day_of_week', 'is_weekend'])

print(f"   ✅ {len(features)} feature hazır")

# 3. İstatistikler
print("3️⃣ İstatistikler...")
for f in features:
    print(f"   {f}: min={X[f].min()}, max={X[f].max()}")

# 4. Ölçeklendirme
print("4️⃣ Ölçeklendirme...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("   ✅ Ölçeklendirme tamam")

# 5. Model eğitimi
print("5️⃣ Model eğitimi...")
model = IsolationForest(contamination=0.1, random_state=42, n_estimators=100)
model.fit(X_scaled)
print("   ✅ Model eğitildi")

# 6. Tahminler
print("6️⃣ Tahminler...")
predictions = model.predict(X_scaled)
anomalies = (predictions == -1).sum()
print(f"   ✅ {anomalies} anomali tespit edildi ({anomalies/len(predictions)*100:.2f}%)")

# 7. Kaydet
print("7️⃣ Model kaydediliyor...")
os.makedirs("models", exist_ok=True)

with open("models/isolation_forest_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/feature_scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

config = {
    "features": features,
    "training_date": datetime.now().isoformat(),
    "total_samples": len(df),
    "anomalies_detected": int(anomalies)
}

with open("models/model_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("   ✅ Model kaydedildi")

# 8. Test
print("8️⃣ Test...")
test_data = pd.DataFrame([{
    'total_watt': 5000,
    'hour_of_day': 14,
    'is_class_in_session': 1,
    'day_of_week': 2,
    'is_weekend': 0
}])

test_scaled = scaler.transform(test_data[features])
test_pred = model.predict(test_scaled)[0]
print(f"   ✅ Test sonucu: {'Anomali' if test_pred == -1 else 'Normal'}")

print("\n🎉 AI MODEL EĞİTİMİ TAMAMLANDI!")
print("Model artık hazır! 🚀")
