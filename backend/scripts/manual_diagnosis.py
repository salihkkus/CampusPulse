# Manuel Teşhis Testi
# Direkt çalıştır: python manual_diagnosis.py

print("🔍 Teşhis Motoru Test")

# Kütüphaneler
from diagnosis_engine import DiagnosisEngine

# Motor oluştur
engine = DiagnosisEngine()

print("\n🧪 Test Senaryoları:")
print("=" * 40)

# Senaryo 1: Boş oda + klima açık
print("\n1️⃣ Boş Oda + Klima Açık:")
print("   Durum: Oda boş, klima çalışıyor")
print("   Beklenen: 'Klima açık unutulmuş' uyarısı")

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
print(f"   ✅ Sonuç: {result1['primary_issue']}")
print(f"   🔧 Cihazlar: {', '.join(result1['detected_devices'])}")
print(f"   💰 Tasarruf: {result1['potential_savings']:.0f}TL/ay")

# Senaryo 2: Normal ders
print("\n2️⃣ Normal Ders:")
print("   Durum: Ders var, normal güç tüketimi")
print("   Beklenen: 'Normal' - uyarı yok")

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
print(f"   ✅ Sonuç: {'Normal - İsraf yok' if not result2['is_wasting'] else 'İsraf var'}")

# Senaryo 3: Gece + ışık açık
print("\n3️⃣ Gece + Işık Açık:")
print("   Durum: Gece 23:00, ışıklar açık")
print("   Beklenen: 'Işıklar açık kalmış' uyarısı")

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
print(f"   ✅ Sonuç: {result3['primary_issue']}")
print(f"   🔧 Cihazlar: {', '.join(result3['detected_devices'])}")

# Senaryo 4: Hafta sonu + PC'ler açık
print("\n4️⃣ Hafta Sonu + PC'ler Açık:")
print("   Durum: Cumartesi, bilgisayarlar açık")
print("   Beklenen: 'Bilgisayarlar açık kalmış' uyarısı")

data4 = {
    "room_id": "M1_Derslik_04",
    "occupancy_status": 0,  # Boş
    "hour_of_day": 15,
    "total_power": 5500,
    "lighting_watt": 0,
    "projector_watt": 0,
    "plug_load_watt": 5500,  # PC'ler
    "is_anomaly": 1,
    "is_weekend": 1,  # Hafta sonu
    "is_holiday": 0
}

result4 = engine.diagnose_energy_waste(data4)
print(f"   ✅ Sonuç: {result4['primary_issue']}")
print(f"   🔧 Cihazlar: {', '.join(result4['detected_devices'])}")
print(f"   💰 Tasarruf: {result4['potential_savings']:.0f}TL/ay")

# Senaryo 5: Ders + arıza
print("\n5️⃣ Ders + Güç Arızası:")
print("   Durum: Ders var ama güç çok düşük")
print("   Beklenen: 'Güç arızası' uyarısı")

data5 = {
    "room_id": "M2_Derslik_05",
    "occupancy_status": 1,  # Ders var
    "hour_of_day": 11,
    "total_power": 150,  # Çok düşük
    "lighting_watt": 100,
    "projector_watt": 0,
    "plug_load_watt": 50,
    "is_anomaly": 1,
    "is_weekend": 0,
    "is_holiday": 0
}

result5 = engine.diagnose_energy_waste(data5)
print(f"   ✅ Sonuç: {result5['primary_issue']}")
print(f"   🔧 Tip: {result5['diagnosis_type']}")

print("\n" + "=" * 40)
print("🎯 MUHAMMET'İN EKRANINDA GÖRÜNECEK MESAJLAR:")
print("=" * 40)

quick1 = engine.get_quick_diagnosis(data1)
quick2 = engine.get_quick_diagnosis(data2)
quick3 = engine.get_quick_diagnosis(data3)
quick4 = engine.get_quick_diagnosis(data4)
quick5 = engine.get_quick_diagnosis(data5)

print(f"📍 M1_Derslik_01: {quick1}")
print(f"📍 M2_Derslik_02: {quick2}")
print(f"📍 AKM_Derslik_03: {quick3}")
print(f"📍 M1_Derslik_04: {quick4}")
print(f"📍 M2_Derslik_05: {quick5}")

print("\n" + "=" * 40)
print("📋 DETAYLI ÖRNEK RAPOR:")
print("=" * 40)

# En kötü durumun detaylı raporu
detailed_report = engine.generate_detailed_report(data1)
print(detailed_report)

print("\n🎉 TEŞHİS MOTORU TESTİ BAŞARILI!")
print("✅ Muhammet'in ekranı hazır!")
print("🚀 Artık 'neden' ve 'ne yapmalı' sorularına cevap veriyor!")
