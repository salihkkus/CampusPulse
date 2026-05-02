#!/usr/bin/env python3

from data_analyzer import DataAnalyzer
import json

def main():
    """Eren'in veri setini analiz et"""
    
    print("🔍 Eren'in Veri Seti Analizi Başlatılıyor...")
    print("=" * 50)
    
    # Analyzer'ı başlat
    analyzer = DataAnalyzer("../kampus_1_aylik_enerji.csv")
    
    # Veriyi yükle ve analiz et
    results = analyzer.load_and_inspect_data()
    
    if "error" in results:
        print(f"❌ Hata: {results['error']}")
        return
    
    # Temel bilgiler
    basic = results["basic_info"]
    print(f"📊 Temel Bilgiler:")
    print(f"   Toplam Kayıt: {basic['total_rows']:,}")
    print(f"   Benzersiz Oda: {basic['unique_rooms']}")
    print(f"   Benzersiz Tarih: {basic['unique_dates']}")
    print(f"   Tarih Aralığı: {basic['date_range']['start_date']} - {basic['date_range']['end_date']}")
    print(f"   Dosya Boyutu: {basic['file_size_mb']} MB")
    print()
    
    # Veri kalitesi
    quality = results["quality_checks"]
    print(f"🔍 Veri Kalitesi:")
    print(f"   Toplam Watt Tutarlılığı: {'✅' if quality['total_watt_consistency'] else '❌'}")
    print(f"   Negatif Değerler: {'❌' if quality['negative_values'] else '✅'}")
    print(f"   Geçersiz Saatler: {'❌' if quality['invalid_hours'] else '✅'}")
    print(f"   Geçersiz Binary Değerler: {'❌' if quality['invalid_binary_values'] else '✅'}")
    print(f"   Duplicate Kayıtlar: {'❌' if quality['duplicate_records'] else '✅'}")
    print()
    
    # İstatistikler
    stats = results["statistics"]
    print(f"📈 İstatistiksel Özet:")
    for col, stat in stats.items():
        print(f"   {col}:")
        print(f"     Min: {stat['min']:.1f}W")
        print(f"     Max: {stat['max']:.1f}W") 
        print(f"     Ort: {stat['mean']:.1f}W")
        print(f"     Med: {stat['median']:.1f}W")
        print(f"     Std: {stat['std']:.1f}W")
        print(f"     Sıfır Değer: {stat['zeros']:,}")
        print()
    
    # Kategorik analiz
    categorical = results["categorical_analysis"]
    print(f"📚 Kategorik Analiz:")
    print(f"   Dersli Saat: {categorical['class_sessions']['with_classes']:,}")
    print(f"   Dersiz Saat: {categorical['class_sessions']['without_classes']:,}")
    print(f"   Ders Yüzdesi: {categorical['class_sessions']['class_percentage']:.1f}%")
    print(f"   Anormal Kayıt: {categorical['anomalies']['anomalous']:,}")
    print(f"   Anormali Yüzdesi: {categorical['anomalies']['anomaly_percentage']:.1f}%")
    print(f"   Hafta İçi: {categorical['day_types']['weekdays']:,}")
    print(f"   Hafta Sonu: {categorical['day_types']['weekends']:,}")
    print(f"   Tatil Günü: {categorical['day_types']['holidays']:,}")
    print()
    
    # Oda pattern'leri
    room_patterns = categorical['room_id']['room_pattern_analysis']
    print(f"🏢 Oda Pattern'leri:")
    print(f"   Benzersiz Bina: {room_patterns['total_buildings']}")
    print(f"   Binalar: {', '.join(room_patterns['unique_buildings'])}")
    print(f"   Oda Tipleri: {room_patterns['total_room_types']}")
    print(f"   Tipler: {', '.join(room_patterns['unique_room_types'])}")
    print()
    
    # Saat dağılımı (ilk 10 saat)
    hour_dist = categorical['hour_distribution']
    print(f"⏰ Saat Dağılımı (İlk 10 Saat):")
    for hour in range(10):
        count = hour_dist.get(hour, 0)
        print(f"   {hour:02d}:00 - {count:,} kayıt")
    print()
    
    # Örnek veri
    print(f"📋 Örnek Veri (İlk 3 Kayıt):")
    for i, record in enumerate(results["sample_data"][:3]):
        print(f"   Kayıt {i+1}:")
        print(f"     Tarih: {record['date']}")
        print(f"     Oda: {record['room_id']}")
        print(f"     Saat: {record['hour_of_day']}")
        print(f"     Ders: {'Evet' if record['is_class_in_session'] == 1 else 'Hayır'}")
        print(f"     Toplam Watt: {record['total_watt']:.1f}W")
        print(f"     İsraf Maliyeti: {record['wasted_cost_tl']:.2f}TL")
        print()
    
    # Sorunlar
    print(f"⚠️ Bulunan Sorunlar:")
    if quality['issues_found']:
        for issue in quality['issues_found']:
            print(f"   - {issue}")
    else:
        print("   ✅ Hiçbir sorun bulunamadı")
    print()
    
    # İsraf analizi
    print(f"💰 İsraf Analizi:")
    waste_analysis = analyzer.get_waste_analysis()
    if "error" not in waste_analysis:
        print(f"   İsraf Kaydı: {waste_analysis['total_waste_records']:,}")
        print(f"   Toplam İsraf: {waste_analysis['total_waste_cost']:.2f} TL")
        print(f"   Ortalama İsraf: {waste_analysis['avg_waste_per_incident']:.2f} TL")
        print(f"   En Çok İsraf Yapan Odalar: {', '.join(waste_analysis['top_wasting_rooms'][:3])}")
        print(f"   Pik İsraf Saatleri: {', '.join(map(str, waste_analysis['peak_waste_hours']))}")
    else:
        print(f"   Hata: {waste_analysis['error']}")
    print()
    
    # Enerji pattern'leri
    print(f"⚡ Enerji Pattern'leri:")
    energy_patterns = analyzer.get_energy_patterns()
    if "error" not in energy_patterns:
        print(f"   Pik Tüketim Saati: {energy_patterns['peak_consumption_hour']}:00")
        print(f"   Düşük Tüketim Saati: {energy_patterns['lowest_consumption_hour']}:00")
        
        # Oda tipi istatistikleri (ilk 5)
        room_stats = energy_patterns['room_type_statistics']
        print(f"   Oda Tipi İstatistikleri (İlk 5):")
        for room_type, stats in list(room_stats.items())[:5]:
            print(f"     {room_type}: Ort={stats['avg_consumption']:.1f}W, Max={stats['max_consumption']:.1f}W")
    else:
        print(f"   Hata: {energy_patterns['error']}")
    print()
    
    # Özet rapor
    print("=" * 50)
    print(analyzer.generate_summary_report())
    
    # Sonuçları JSON olarak kaydet
    with open('data_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n📁 Detaylı analiz sonuçları 'data_analysis_results.json' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
