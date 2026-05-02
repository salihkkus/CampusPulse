#!/usr/bin/env python3

from diagnosis_engine import DiagnosisEngine
import json

def test_diagnosis_engine():
    """Teşhis motorunu test et"""
    
    print("🔍 Teşhis Motoru Testi Başlatılıyor...")
    print("=" * 50)
    
    # Teşhis motorunu oluştur
    engine = DiagnosisEngine()
    
    # Test senaryoları
    test_cases = [
        {
            "name": "Boş oda + klima açık",
            "data": {
                "room_id": "M1_Derslik_01",
                "timestamp": "2023-11-15T14:00:00Z",
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
        },
        {
            "name": "Ders var + normal",
            "data": {
                "room_id": "M2_Derslik_02",
                "timestamp": "2023-11-15T10:00:00Z",
                "occupancy_status": 1,  # Ders var
                "hour_of_day": 10,
                "total_power": 5000,
                "lighting_watt": 400,
                "projector_watt": 300,
                "plug_load_watt": 4300,  # PC'ler
                "is_anomaly": 0,
                "is_weekend": 0,
                "is_holiday": 0
            }
        },
        {
            "name": "Gece + ışık açık",
            "data": {
                "room_id": "AKM_Derslik_03",
                "timestamp": "2023-11-15T23:00:00Z",
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
        },
        {
            "name": "Hafta sonu + PC'ler açık",
            "data": {
                "room_id": "M1_Derslik_04",
                "timestamp": "2023-11-18T15:00:00Z",
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
        },
        {
            "name": "Ders var + güç düşük (arıza)",
            "data": {
                "room_id": "M2_Derslik_05",
                "timestamp": "2023-11-15T11:00:00Z",
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
        }
    ]
    
    # Testleri çalıştır
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        # Teşhis yap
        diagnosis = engine.diagnose_energy_waste(test_case['data'])
        
        # Sonuçları yazdır
        print(f"📊 Sonuç:")
        print(f"   İsraf: {'Evet' if diagnosis['is_wasting'] else 'Hayır'}")
        print(f"   Tip: {diagnosis['diagnosis_type']}")
        print(f"   Öncelik: {diagnosis['urgency_level']}")
        print(f"   Güven: {diagnosis['confidence']:.0%}")
        
        if diagnosis['is_wasting']:
            print(f"   Ana Sorun: {diagnosis['primary_issue']}")
            print(f"   Cihazlar: {', '.join(diagnosis['detected_devices'])}")
            print(f"   Tasarruf: {diagnosis['potential_savings']:.0f}TL/ay")
            
            print(f"   Öneriler:")
            for j, rec in enumerate(diagnosis['recommendations'], 1):
                print(f"     {j}. {rec['short']} - {rec['action']}")
        
        # Hızlı teşhis
        quick = engine.get_quick_diagnosis(test_case['data'])
        print(f"   Hızlı: {quick}")
    
    # Toplu test
    print(f"\n📦 Toplu Teşhis Testi")
    print("-" * 30)
    
    all_data = [case['data'] for case in test_cases]
    batch_results = engine.batch_diagnose(all_data)
    
    summary = engine.get_diagnosis_summary(batch_results)
    
    print(f"Toplam analiz: {summary['total_analyzed']}")
    print(f"İsraf yapan: {summary['wasting_count']}")
    print(f"İsraf oranı: {summary['wasting_percentage']:.1f}%")
    print(f"Toplam tasarruf: {summary['total_potential_savings']:.0f}TL/ay")
    
    print(f"Cihaz frekansı:")
    for device, count in summary['device_frequency'].items():
        print(f"   {device}: {count}")
    
    print(f"Öncelik dağılımı:")
    for urgency, count in summary['urgency_distribution'].items():
        print(f"   {urgency}: {count}")
    
    # Detaylı rapor örneği
    print(f"\n📋 Detaylı Rapor Örneği")
    print("-" * 30)
    
    worst_case = max(batch_results, key=lambda x: x['potential_savings'])
    detailed_report = engine.generate_detailed_report(test_cases[0]['data'])
    
    print(detailed_report)
    
    print(f"\n🎉 Teşhis Motoru Testi Tamamlandı!")
    print("✅ Motor hazır ve çalışıyor!")

if __name__ == "__main__":
    test_diagnosis_engine()
