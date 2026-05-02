#!/usr/bin/env python3

from ai_trainer import AITrainer
import json

def main():
    """Eren'in veri seti ile AI modelini eğit"""
    
    print("🤖 AI Model Eğitimi Başlatılıyor...")
    print("=" * 50)
    
    # Trainer'ı oluştur
    trainer = AITrainer("../kampus_1_aylik_enerji.csv")
    
    # 1. Veriyi yükle ve hazırla
    print("📊 Veri yükleniyor ve hazırlanıyor...")
    data_prep = trainer.load_and_prepare_data()
    
    if "error" in data_prep:
        print(f"❌ Hata: {data_prep['error']}")
        return
    
    print("✅ Veri başarıyla yüklendi")
    basic_info = data_prep["basic_info"]
    print(f"   Toplam Kayıt: {basic_info['total_records']:,}")
    print(f"   Tarih Aralığı: {basic_info['date_range']}")
    print(f"   Benzersiz Oda: {basic_info['unique_rooms']}")
    print(f"   Feature'lar: {', '.join(basic_info['training_features'])}")
    print()
    
    # Feature istatistikleri
    print("📈 Feature İstatistikleri:")
    feature_stats = data_prep["feature_statistics"]
    for feature, stats in feature_stats.items():
        print(f"   {feature}:")
        print(f"     Min: {stats['min']:.1f}")
        print(f"     Max: {stats['max']:.1f}")
        print(f"     Ort: {stats['mean']:.1f}")
        print(f"     Std: {stats['std']:.1f}")
        print(f"     Eksik: {stats['missing']}")
    print()
    
    # Veri kalitesi
    print("🔍 Veri Kalitesi:")
    quality = data_prep["data_quality"]
    print(f"   Eksik Değer: {sum(quality['missing_values'].values())}")
    print(f"   Sıfır Değer: {sum(quality['zero_values'].values())}")
    print(f"   Negatif Değer: {sum(quality['negative_values'].values())}")
    print()
    
    # 2. Modeli eğit
    print("🧠 Isolation Forest modeli eğitiliyor...")
    training_results = trainer.train_isolation_forest()
    
    if "error" in training_results:
        print(f"❌ Hata: {training_results['error']}")
        return
    
    print("✅ Model başarıyla eğitildi")
    
    # Model bilgileri
    model_info = training_results["model_info"]
    print(f"   Model Tipi: {model_info['model_type']}")
    print(f"   Eğitim Örnekleri: {model_info['training_samples']:,}")
    print(f"   Contamination: {model_info['contamination']}")
    print(f"   Kullanılan Feature'lar: {len(model_info['features_used'])} adet")
    print()
    
    # Performans metrikleri
    print("📊 Performans Metrikleri:")
    performance = training_results["performance_metrics"]
    print(f"   Accuracy: {performance['accuracy']:.3f}")
    print(f"   Precision: {performance['precision']:.3f}")
    print(f"   Recall: {performance['recall']:.3f}")
    print(f"   F1 Score: {performance['f1_score']:.3f}")
    print(f"   True Positives: {performance['true_positives']:,}")
    print(f"   False Positives: {performance['false_positives']:,}")
    print(f"   True Negatives: {performance['true_negatives']:,}")
    print(f"   False Negatives: {performance['false_negatives']:,}")
    print()
    
    # Anomali analizi
    print("🔍 Anomali Analizi:")
    anomaly = training_results["anomaly_analysis"]
    print(f"   Tespit Edilen Anomali: {anomaly['total_anomalies_detected']:,}")
    print(f"   Gerçek Anomali: {anomaly['actual_anomalies']:,}")
    print(f"   Anomali Oranı: {anomaly['anomaly_rate']:.3f}")
    print(f"   Ortalama Anomali Skoru: {anomaly['avg_anomaly_score']:.3f}")
    print(f"   Skor Aralığı: {anomaly['anomaly_score_range']['min']:.3f} - {anomaly['anomaly_score_range']['max']:.3f}")
    print()
    
    # Feature importance
    print("🎯 Feature Importance:")
    feature_importance = training_results["feature_importance"]
    for i, (feature, importance) in enumerate(feature_importance.items(), 1):
        print(f"   {i}. {feature}: {importance:.3f}")
    print()
    
    # 3. Anomali pattern'lerini analiz et
    print("🔬 Anomali Pattern'leri analiz ediliyor...")
    pattern_analysis = trainer.analyze_anomaly_patterns()
    
    if "error" not in pattern_analysis:
        print("✅ Pattern analizi tamamlandı")
        
        # Zaman pattern'leri
        time_patterns = pattern_analysis["time_patterns"]
        print(f"   Anomali Saat Dağılımı (İlk 5):")
        hour_anomalies = dict(list(time_patterns["anomaly_by_hour"].items())[:5])
        for hour, count in hour_anomalies.items():
            print(f"     {hour:02d}:00 - {count} anomali")
        
        print(f"   Anomali Gün Dağılımı:")
        for day, count in time_patterns["anomaly_by_day_of_week"].items():
            day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
            print(f"     {day_names[day]} - {count} anomali")
        
        print(f"   Anomali Oda Tipi Dağılımı:")
        for room_type, count in time_patterns["anomaly_by_room_type"].items():
            print(f"     {room_type} - {count} anomali")
        print()
        
        # Feature pattern'leri
        print("📊 Feature Pattern'leri:")
        feature_patterns = pattern_analysis["feature_patterns"]
        for feature, stats in feature_patterns.items():
            print(f"   {feature}:")
            print(f"     Normal Ort: {stats['normal_mean']:.1f} ± {stats['normal_std']:.1f}")
            print(f"     Anomali Ort: {stats['anomaly_mean']:.1f} ± {stats['anomaly_std']:.1f}")
        print()
        
        # En çok anomali yapan odalar
        print("🏢 En Çok Anomali Yakan Odalar (İlk 5):")
        room_analysis = pattern_analysis["room_analysis"]
        for room_id, stats in list(room_analysis.items())[:5]:
            print(f"   {room_id}: {stats['anomaly_count']} anomali, Ort. Güç: {stats['avg_power']:.1f}W")
        print()
    
    # 4. Modeli kaydet
    print("💾 Model kaydediliyor...")
    save_results = trainer.save_model()
    
    if save_results["success"]:
        print("✅ Model başarıyla kaydedildi")
        print(f"   Model Dosyası: {save_results['model_file']}")
        print(f"   Scaler Dosyası: {save_results['scaler_file']}")
        print(f"   Sonuçlar: {save_results['results_file']}")
        print(f"   Konfigürasyon: {save_results['config_file']}")
    else:
        print(f"❌ Kaydetme hatası: {save_results['error']}")
    print()
    
    # 5. Test tahmini
    print("🧪 Test tahmini yapılıyor...")
    test_data = {
        "date": "2023-11-15",
        "room_id": "M1_Derslik_01",
        "hour_of_day": 14,
        "is_class_in_session": 1,
        "lighting_watt": 400.0,
        "projector_watt": 250.0,
        "plug_load_watt": 5000.0,
        "total_watt": 5650.0
    }
    
    prediction = trainer.predict_anomaly(test_data)
    
    if "error" not in prediction:
        print("✅ Test tahmini başarılı")
        print(f"   Anomali: {'Evet' if prediction['is_anomaly'] else 'Hayır'}")
        print(f"   Anomali Skoru: {prediction['anomaly_score']:.3f}")
        print(f"   Güven: {prediction['confidence']:.3f}")
    else:
        print(f"❌ Tahmin hatası: {prediction['error']}")
    print()
    
    # 6. Rapor
    print("=" * 50)
    print(trainer.generate_training_report())
    
    print(f"\n🎉 AI Model Eğitimi Tamamlandı!")
    print(f"Model artık anomali tespiti için hazır!")

if __name__ == "__main__":
    main()
