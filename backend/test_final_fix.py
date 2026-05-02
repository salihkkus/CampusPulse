print("🔍 Final Pydantic V2 Test")

try:
    # Model'leri import et
    from models.energy_data import EnergyDataRecord, EnergyDataBatch
    from datetime import date
    
    print("✅ Import başarılı")
    
    # Test verisi oluştur (record_date kullanarak)
    test_data = {
        "record_date": date(2023, 11, 15),  # date yerine record_date
        "room_id": "M1_Derslik_01",
        "hour_of_day": 14,
        "is_class_in_session": 1,
        "lighting_watt": 400.0,
        "projector_watt": 300.0,
        "plug_load_watt": 4300.0,
        "total_watt": 5000.0,
        "is_anomaly": 0,
        "wasted_cost_tl": 0.0,
        "is_holiday": 0,
        "is_weekend": 0
    }
    
    # Kayıt oluştur
    record = EnergyDataRecord(**test_data)
    print("✅ EnergyDataRecord oluşturuldu")
    
    # Batch test
    batch_data = {
        "records": [record],
        "batch_id": "test_batch_001"
    }
    
    batch = EnergyDataBatch(**batch_data)
    print("✅ EnergyDataBatch oluşturuldu")
    
    # Test fonksiyonları
    print(f"   Cihaz dağılımı: {record.get_device_breakdown()}")
    print(f"   Ana cihaz: {record.get_primary_device()}")
    print(f"   İsraf var mı: {record.is_wasting_energy()}")
    print(f"   Gün tipi: {record.get_day_type().name}")
    print(f"   AI format: {record.to_ai_format()['timestamp']}")
    
    # Batch özet
    summary = batch.get_summary()
    print(f"   Batch özeti: {summary['total_records']} kayıt")
    print(f"   Tarih aralığı: {summary['date_range']['start']} - {summary['date_range']['end']}")
    
    print("\n🎉 Tüm testler başarılı!")
    print("✅ Pydantic V2 tam uyumlu")
    print("✅ Field name clash sorunu çözüldü")
    print("🚀 Sunucu başlatılabilir!")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
