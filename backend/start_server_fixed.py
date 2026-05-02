#!/usr/bin/env python3

import subprocess
import sys
import os

def main():
    print("🚀 CampusPulse Backend Sunucusu")
    print("=" * 50)
    
    # Önce Pydantic test et
    print("1️⃣ Pydantic V2 uyumluluğu test ediliyor...")
    try:
        from models.energy_data import EnergyDataRecord
        from datetime import date
        
        record = EnergyDataRecord(
            date=date(2023,11,15), 
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
        print("✅ Pydantic V2 uyumlu")
    except Exception as e:
        print(f"❌ Pydantic hatası: {e}")
        return
    
    # Sunucuyu başlat
    print("\n2️⃣ FastAPI sunucusu başlatılıyor...")
    print("📍 URL: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("⏹️ Durdurmak için: CTRL+C")
    print("-" * 50)
    
    # uvicorn komutu
    uvicorn_command = [
        sys.executable, "-m", "uvicorn", 
        "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
    ]
    
    try:
        subprocess.run(uvicorn_command, cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n⏹️ Sunucu durduruldu")
    except Exception as e:
        print(f"❌ Sunucu hatası: {e}")

if __name__ == "__main__":
    main()
