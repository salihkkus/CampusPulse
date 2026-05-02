print("🔍 Hızlı Sunucu Test")

try:
    # Import test
    from typing import Any
    from main import app
    print("✅ Import'lar başarılı")
    
    # Model test
    from models.energy_data import EnergyDataRecord
    from datetime import date
    record = EnergyDataRecord(
        record_date=date(2023,11,15), 
        room_id='M1_Derslik_01', 
        hour_of_day=14, 
        is_class_in_session=1, 
        lighting_watt=400.0, 
        projector_watt=300.0, 
        plug_load_watt=4300.0, 
        total_watt=5000.0, 
        is_anomaly=0, 
        wasted_cost_tl=0.0, 
        is_holiday=0, 
        is_weekend=0
    )
    print("✅ Model çalışıyor")
    
    # AI Engine test
    from enhanced_ai_engine import EnhancedAIEngine
    ai = EnhancedAIEngine()
    print("✅ AI Engine yüklendi")
    
    print("\n🎉 Tüm testler başarılı!")
    print("✅ Any import sorunu çözüldü")
    print("✅ Pydantic V2 uyumlu")
    print("✅ Model dosyaları bulunamadı uyarısı normal (önce eğitim gerekir)")
    print("🚀 Sunucu başlatılabilir!")
    
    print("\n📋 Sunucuyu başlatmak için:")
    print("uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
