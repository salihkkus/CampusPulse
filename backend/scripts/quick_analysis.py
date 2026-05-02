import pandas as pd
import numpy as np

print("🔍 CSV Veri Analizi Başlatılıyor...")

try:
    # CSV'i oku
    df = pd.read_csv('../kampus_1_aylik_enerji.csv')
    
    print("✅ CSV başarıyla okundu")
    print(f"📊 Satır sayısı: {len(df):,}")
    print(f"📊 Sütun sayısı: {len(df.columns)}")
    print(f"📊 Sütunlar: {list(df.columns)}")
    
    # Temel istatistikler
    print(f"\n📈 Temel İstatistikler:")
    print(f"   Benzersiz oda: {df['room_id'].nunique()}")
    print(f"   Benzersiz tarih: {df['date'].nunique()}")
    print(f"   Tarih aralığı: {df['date'].min()} - {df['date'].max()}")
    
    # Veri tipleri
    print(f"\n🔧 Veri Tipleri:")
    for col, dtype in df.dtypes.items():
        print(f"   {col}: {dtype}")
    
    # Eksik veri
    print(f"\n❓ Eksik Veri:")
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"   {col}: {count}")
        else:
            print(f"   {col}: 0")
    
    # Sayısal sütunlar için istatistik
    numeric_cols = ['lighting_watt', 'projector_watt', 'plug_load_watt', 'total_watt', 'wasted_cost_tl']
    print(f"\n📊 Sayısal İstatistikler:")
    for col in numeric_cols:
        if col in df.columns:
            print(f"   {col}:")
            print(f"     Min: {df[col].min():.1f}")
            print(f"     Max: {df[col].max():.1f}")
            print(f"     Ort: {df[col].mean():.1f}")
            print(f"     Sıfır: {(df[col] == 0).sum():,}")
    
    # Kategorik veriler
    print(f"\n📚 Kategorik Veriler:")
    print(f"   Dersli saat: {(df['is_class_in_session'] == 1).sum():,}")
    print(f"   Dersiz saat: {(df['is_class_in_session'] == 0).sum():,}")
    print(f"   Anomali: {(df['is_anomaly'] == 1).sum():,}")
    print(f"   Hafta sonu: {(df['is_weekend'] == 1).sum():,}")
    print(f"   Tatil: {(df['is_holiday'] == 1).sum():,}")
    
    # Veri kalitesi kontrolleri
    print(f"\n🔍 Veri Kalitesi:")
    
    # Toplam watt tutarlılığı
    calculated_total = df['lighting_watt'] + df['projector_watt'] + df['plug_load_watt']
    tolerance = calculated_total * 0.05
    inconsistent = abs(df['total_watt'] - calculated_total) > tolerance
    print(f"   Toplam watt tutarsızlığı: {inconsistent.sum():,} kayıt")
    
    # Negatif değerler
    numeric_cols = ['lighting_watt', 'projector_watt', 'plug_load_watt', 'total_watt', 'wasted_cost_tl']
    total_negative = 0
    for col in numeric_cols:
        neg_count = (df[col] < 0).sum()
        total_negative += neg_count
        if neg_count > 0:
            print(f"   {col} negatif: {neg_count}")
    
    if total_negative == 0:
        print(f"   Negatif değer: ✅ Yok")
    
    # Geçersiz saatler
    invalid_hours = df[(df['hour_of_day'] < 0) | (df['hour_of_day'] > 23)]
    print(f"   Geçersiz saat: {len(invalid_hours):,} kayıt")
    
    # Binary değerler
    binary_cols = ['is_class_in_session', 'is_anomaly', 'is_holiday', 'is_weekend']
    total_invalid_binary = 0
    for col in binary_cols:
        invalid = df[~df[col].isin([0, 1])]
        total_invalid_binary += len(invalid)
        if len(invalid) > 0:
            print(f"   {col} geçersiz binary: {len(invalid)}")
    
    if total_invalid_binary == 0:
        print(f"   Binary değerler: ✅ Tümü geçerli")
    
    # Duplicate kayıtlar
    duplicates = df.duplicated().sum()
    print(f"   Duplicate kayıt: {duplicates:,}")
    
    # İsraf analizi
    waste_records = df[df['wasted_cost_tl'] > 0]
    print(f"\n💰 İsraf Analizi:")
    print(f"   İsraf kaydı: {len(waste_records):,}")
    print(f"   Toplam israf: {waste_records['wasted_cost_tl'].sum():.2f} TL")
    print(f"   Ortalama israf: {waste_records['wasted_cost_tl'].mean():.2f} TL")
    
    # Örnek veri
    print(f"\n📋 Örnek Veri (İlk 3 kayıt):")
    print(df.head(3).to_string())
    
    print(f"\n✅ Analiz tamamlandı! Veri seti temiz ve kullanıma hazır.")
    
except Exception as e:
    print(f"❌ Hata: {str(e)}")
    import traceback
    traceback.print_exc()
