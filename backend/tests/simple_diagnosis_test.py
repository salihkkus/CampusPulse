print("🔍 Teşhis Motoru Test")

from diagnosis_engine import DiagnosisEngine

# Motor oluştur
engine = DiagnosisEngine()

# Test 1: Boş oda + klima
print("\n🧪 Test 1: Boş oda + klima açık")
data1 = {
    "room_id": "M1_Derslik_01",
    "occupancy_status": 0,  # Boş
    "hour_of_day": 14,
    "total_power": 2500,
    "lighting_watt": 400,
    "projector_watt": 0,
    "plug_load_watt": 2100,  # Klima
    "is_anomaly": 1,
    "is_weekend": 0,
    "is_holiday": 0
}

result1 = engine.diagnose_energy_waste(data1)
print(f"   İsraf: {result1['is_wasting']}")
print(f"   Ana sorun: {result1['primary_issue']}")
print(f"   Cihazlar: {result1['detected_devices']}")
print(f"   Öneri: {result1['recommendations'][0]['short'] if result1['recommendations'] else 'Yok'}")

# Test 2: Normal ders
print("\n🧪 Test 2: Normal ders")
data2 = {
    "room_id": "M2_Derslik_02",
    "occupancy_status": 1,  # Ders var
    "hour_of_day": 10,
    "total_power": 5000,
    "lighting_watt": 400,
    "projector_watt": 300,
    "plug_load_watt": 4300,
    "is_anomaly": 0,
    "is_weekend": 0,
    "is_holiday": 0
}

result2 = engine.diagnose_energy_waste(data2)
print(f"   İsraf: {result2['is_wasting']}")
print(f"   Durum: Normal")

# Test 3: Gece + ışık
print("\n🧪 Test 3: Gece + ışık açık")
data3 = {
    "room_id": "AKM_Derslik_03",
    "occupancy_status": 0,  # Boş
    "hour_of_day": 23,
    "total_power": 450,
    "lighting_watt": 450,  # Işıklar açık
    "projector_watt": 0,
    "plug_load_watt": 0,
    "is_anomaly": 1,
    "is_weekend": 0,
    "is_holiday": 0
}

result3 = engine.diagnose_energy_waste(data3)
print(f"   İsraf: {result3['is_wasting']}")
print(f"   Ana sorun: {result3['primary_issue']}")
print(f"   Cihazlar: {result3['detected_devices']}")

print("\n✅ Teşhis motoru testi tamamlandı!")
print("🎯 Muhammet'in ekranında görünecek mesajlar:")
print(f"   - {engine.get_quick_diagnosis(data1)}")
print(f"   - {engine.get_quick_diagnosis(data2)}")
print(f"   - {engine.get_quick_diagnosis(data3)}")
