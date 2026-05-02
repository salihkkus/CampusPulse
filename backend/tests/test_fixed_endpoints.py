#!/usr/bin/env python3

import requests
import json

def test_fixed_endpoints():
    """Düzeltilmiş endpoint'leri test et"""
    
    base_url = "http://localhost:8000"
    
    print("🔧 Düzeltilmiş Endpoint Testleri")
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
        return
    
    # Test 2: Hızlı teşhis
    print("\n2️⃣ Hızlı Teşhis")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/quick-diagnosis/ENG101")
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
    
    # Test 3: Oda durumu
    print("\n3️⃣ Oda Durumu (Frontend)")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/room-status/ENG101")
        if response.status_code == 200:
            data = response.json()
            print("✅ Oda durumu başarılı")
            room = data['data']
            print(f"   Oda: {room['room_id']}")
            print(f"   Durum: {room['status']}")
            print(f"   Mesaj: {room['diagnostic_message']}")
            print(f"   Güç: {room['current_power']}W")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # Test 4: Dashboard
    print("\n4️⃣ Dashboard Özeti")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/v2/ai/dashboard-summary")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard başarılı")
            dashboard = data['data']
            summary = dashboard['summary']
            print(f"   Toplam oda: {summary['total_rooms']}")
            print(f"   İsraf yapan: {summary['wasting_rooms']}")
            print(f"   İsraf oranı: {summary['waste_percentage']:.1f}%")
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"   Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testler Tamamlandı!")
    print("✅ DataService method'ları eklendi")
    print("🚀 Muhammet frontend'e hazır!")

if __name__ == "__main__":
    test_fixed_endpoints()
