print("🔍 Basit Test")

try:
    import pandas as pd
    print("✅ Pandas yüklendi")
    
    df = pd.read_csv("../kampus_1_aylik_enerji.csv")
    print(f"✅ CSV okundu: {len(df)} satır")
    
    from sklearn.ensemble import IsolationForest
    print("✅ Sklearn yüklendi")
    
    # Basit model
    features = ['total_watt', 'hour_of_day', 'is_class_in_session']
    X = df[features]
    
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    
    predictions = model.predict(X)
    anomalies = (predictions == -1).sum()
    
    print(f"✅ Model eğitildi")
    print(f"   Anomali sayısı: {anomalies}")
    print(f"   Toplam kayıt: {len(df)}")
    print(f"   Anomali oranı: {anomalies/len(df)*100:.2f}%")
    
    print("🎉 Test başarılı!")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
