#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """FastAPI endpoint'lerini test et"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 FastAPI Endpoint Testleri")
    print("=" * 50)
    
    # Test 1: Model bilgileri
    print("\n1️⃣ Model Bilgileri")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/model-info")
        if response.status_code == 200:
            data = response.json()
            print("✅ Model bilgileri alındı")
            print(f"   Model: {data['data'].get('model_type', 'Unknown')}")
            print(f"   Eğitim: {data['data'].get('is_trained', False)}")
            print(f"   Feature'lar: {len(data['data'].get('features', []))}")
        else:
            print(f"❌ Hata: {response.status_code}")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        print("💡 Sunucu çalışmıyor olabilir: uvicorn main:app --reload")
        return
    
    # Test 2: Hızlı teşhis
    print("\n2️⃣ Hızlı Teşhis")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/quick-diagnosis/M1_Derslik_01")
        if response.status_code == 200:
            data = response.json()
            print("✅ Hızlı teşhis başarılı")
            print(f"   Oda: {data['data']['room_id']}")
            print(f"   Teşhis: {data['data']['diagnosis']}")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # Test 3: Oda analizi
    print("\n3️⃣ Oda Analizi")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/analysis/M1_Derslik_01")
        if response.status_code == 200:
            data = response.json()
            print("✅ Oda analizi başarılı")
            analysis = data['data']
            print(f"   Durum: {analysis['status']}")
            print(f"   İsraf: {analysis['analysis']['diagnosis']['is_wasting']}")
            print(f"   Anomali: {analysis['analysis']['anomaly']['is_anomaly']}")
            print(f"   Cihazlar: {analysis['current_data']['detected_devices']}")
            print(f"   Güven: {analysis['confidence']:.0%}")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # Test 4: Frontend odası durumu
    print("\n4️⃣ Frontend Oda Durumu")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/room-status/M1_Derslik_01")
        if response.status_code == 200:
            data = response.json()
            print("✅ Frontend odası durumu başarılı")
            room_data = data['data']
            print(f"   Oda: {room_data['room_id']}")
            print(f"   Durum: {room_data['status']}")
            print(f"   Mesaj: {room_data['diagnostic_message']}")
            print(f"   Cihazlar: {room_data['detected_devices']}")
            print(f"   Maliyet: {room_data['instant_loss_tl_per_hour']:.2f}TL/saat")
            print(f"   Karbon: {room_data['carbon_kg_per_hour']:.2f}kg CO2/saat")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # Test 5: Toplu analiz
    print("\n5️⃣ Toplu Analiz")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/batch-analysis")
        if response.status_code == 200:
            data = response.json()
            print("✅ Toplu analiz başarılı")
            batch = data['data']
            summary = batch['summary']
            print(f"   Toplam oda: {summary['total_rooms']}")
            print(f"   İsraf yapan: {summary['wasting_rooms']}")
            print(f"   Kritik: {summary['critical_rooms']}")
            print(f"   Toplam israf: {summary['total_waste_cost']:.2f}TL/saat")
            print(f"   Potansiyel tasarruf: {summary['total_potential_savings']:.0f}TL/ay")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # Test 6: Dashboard özeti
    print("\n6️⃣ Dashboard Özeti")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/dashboard-summary")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard özeti başarılı")
            dashboard = data['data']
            summary = dashboard['summary']
            print(f"   Toplam oda: {summary['total_rooms']}")
            print(f"   İsraf oranı: {summary['waste_percentage']:.1f}%")
            print(f"   Kritik oda: {summary['critical_rooms']}")
            print(f"   Normal oda: {summary['normal_rooms']}")
            print(f"   Öneri sayısı: {len(dashboard['recommendations'])}")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # Test 7: Özel analiz
    print("\n7️⃣ Özel Analiz")
    print("-" * 30)
    
    try:
        custom_data = {
            "room_id": "Test_Derslik_01",
            "occupancy_status": 0,  # Boş
            "hour_of_day": 14,
            "total_power": 2500,
            "lighting_watt": 400,
            "projector_watt": 0,
            "plug_load_watt": 2100,  # Klima
            "is_weekend": 0,
            "is_holiday": 0
        }
        
        response = requests.post(
            f"{base_url}/api/v2/ai/custom-analysis",
            json=custom_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Özel analiz başarılı")
            analysis = data['data']
            print(f"   Oda: {analysis['room_id']}")
            print(f"   Durum: {analysis['status']}")
            print(f"   İsraf: {analysis['analysis']['diagnosis']['is_wasting']}")
            print(f"   Mesaj: {analysis['analysis']['diagnosis'].get('primary_issue', 'Normal')}")
            print(f"   Cihazlar: {analysis['current_data']['detected_devices']}")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Endpoint Testleri Tamamlandı!")
    print("✅ FastAPI hazır ve Muhammet'in frontend'i bekliyor!")

if __name__ == "__main__":
    test_api_endpoints()
