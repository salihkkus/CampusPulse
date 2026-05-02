import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from datetime import datetime, date
import logging

class DataAnalyzer:
    """
    Eren'in gönderdiği CSV verisini analiz etmek için
    Veri kalitesi, eksik değerler, istatistikler ve anomali tespiti
    """
    
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.df = None
        self.analysis_results = {}
        
    def load_and_inspect_data(self) -> Dict[str, Any]:
        """
        Veriyi yükle ve temel analizleri yap
        """
        try:
            # CSV'i oku
            self.df = pd.read_csv(self.csv_file_path)
            
            # Temel bilgiler
            basic_info = {
                "total_rows": len(self.df),
                "total_columns": len(self.df.columns),
                "column_names": list(self.df.columns),
                "file_size_mb": self._get_file_size(),
                "date_range": self._get_date_range(),
                "unique_rooms": self.df['room_id'].nunique(),
                "unique_dates": self.df['date'].nunique()
            }
            
            # Veri tipleri
            data_types = self.df.dtypes.to_dict()
            data_types = {str(k): str(v) for k, v in data_types.items()}
            
            # Eksik veri analizi
            missing_data = self.df.isnull().sum().to_dict()
            missing_data = {str(k): int(v) for k, v in missing_data.items()}
            
            # İstatistiksel özet
            numeric_columns = ['lighting_watt', 'projector_watt', 'plug_load_watt', 'total_watt', 'wasted_cost_tl']
            stats_summary = {}
            
            for col in numeric_columns:
                if col in self.df.columns:
                    stats_summary[col] = {
                        "min": float(self.df[col].min()),
                        "max": float(self.df[col].max()),
                        "mean": float(self.df[col].mean()),
                        "median": float(self.df[col].median()),
                        "std": float(self.df[col].std()),
                        "zeros": int((self.df[col] == 0).sum()),
                        "negative_values": int((self.df[col] < 0).sum())
                    }
            
            # Kategorik veri analizi
            categorical_analysis = {}
            
            # room_id analizi
            room_counts = self.df['room_id'].value_counts().head(10)
            categorical_analysis['room_id'] = {
                "unique_count": int(self.df['room_id'].nunique()),
                "top_10_rooms": room_counts.to_dict(),
                "room_pattern_analysis": self._analyze_room_patterns()
            }
            
            # Saat dağılımı
            hour_distribution = self.df['hour_of_day'].value_counts().sort_index()
            categorical_analysis['hour_distribution'] = hour_distribution.to_dict()
            
            # Ders durumu analizi
            class_session_counts = self.df['is_class_in_session'].value_counts()
            categorical_analysis['class_sessions'] = {
                "with_classes": int(class_session_counts.get(1, 0)),
                "without_classes": int(class_session_counts.get(0, 0)),
                "class_percentage": float((class_session_counts.get(1, 0) / len(self.df)) * 100)
            }
            
            # Anomali analizi
            anomaly_counts = self.df['is_anomaly'].value_counts()
            categorical_analysis['anomalies'] = {
                "normal": int(anomaly_counts.get(0, 0)),
                "anomalous": int(anomaly_counts.get(1, 0)),
                "anomaly_percentage": float((anomaly_counts.get(1, 0) / len(self.df)) * 100) if len(self.df) > 0 else 0
            }
            
            # Hafta sonu/tatil analizi
            weekend_counts = self.df['is_weekend'].value_counts()
            holiday_counts = self.df['is_holiday'].value_counts()
            
            categorical_analysis['day_types'] = {
                "weekdays": int(weekend_counts.get(0, 0)),
                "weekends": int(weekend_counts.get(1, 0)),
                "holidays": int(holiday_counts.get(1, 0)),
                "weekday_percentage": float((weekend_counts.get(0, 0) / len(self.df)) * 100) if len(self.df) > 0 else 0
            }
            
            # Veri kalitesi kontrolü
            quality_checks = self._perform_quality_checks()
            
            # Örnek veri
            sample_data = self.df.head(5).to_dict('records')
            
            self.analysis_results = {
                "basic_info": basic_info,
                "data_types": data_types,
                "missing_data": missing_data,
                "statistics": stats_summary,
                "categorical_analysis": categorical_analysis,
                "quality_checks": quality_checks,
                "sample_data": sample_data,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return self.analysis_results
            
        except Exception as e:
            return {
                "error": f"Veri analizi hatası: {str(e)}",
                "analysis_timestamp": datetime.now().isoformat()
            }
    
    def _get_file_size(self) -> float:
        """Dosya boyutunu MB cinsinden döndür"""
        try:
            import os
            size_bytes = os.path.getsize(self.csv_file_path)
            return round(size_bytes / (1024 * 1024), 2)
        except:
            return 0.0
    
    def _get_date_range(self) -> Dict[str, str]:
        """Tarih aralığını döndür"""
        try:
            if 'date' in self.df.columns:
                min_date = self.df['date'].min()
                max_date = self.df['date'].max()
                return {
                    "start_date": str(min_date),
                    "end_date": str(max_date),
                    "total_days": str((pd.to_datetime(max_date) - pd.to_datetime(min_date)).days + 1)
                }
        except:
            pass
        return {"start_date": "N/A", "end_date": "N/A", "total_days": "0"}
    
    def _analyze_room_patterns(self) -> Dict[str, Any]:
        """Oda ID pattern'lerini analiz et"""
        try:
            room_ids = self.df['room_id'].unique()
            
            # Bina sayısı
            buildings = set()
            room_types = set()
            
            for room_id in room_ids:
                parts = room_id.split('_')
                if len(parts) >= 2:
                    buildings.add(parts[0])
                    room_types.add(parts[1])
            
            return {
                "unique_buildings": list(buildings),
                "unique_room_types": list(room_types),
                "total_buildings": len(buildings),
                "total_room_types": len(room_types)
            }
        except:
            return {"unique_buildings": [], "unique_room_types": [], "total_buildings": 0, "total_room_types": 0}
    
    def _perform_quality_checks(self) -> Dict[str, Any]:
        """Veri kalitesi kontrolleri yap"""
        checks = {
            "total_watt_consistency": True,
            "negative_values": False,
            "invalid_hours": False,
            "invalid_binary_values": False,
            "duplicate_records": False,
            "issues_found": []
        }
        
        try:
            # Toplam watt tutarlılığı kontrolü
            if all(col in self.df.columns for col in ['lighting_watt', 'projector_watt', 'plug_load_watt', 'total_watt']):
                calculated_total = self.df['lighting_watt'] + self.df['projector_watt'] + self.df['plug_load_watt']
                tolerance = calculated_total * 0.05  # %5 tolerans
                inconsistent = abs(self.df['total_watt'] - calculated_total) > tolerance
                
                if inconsistent.any():
                    checks["total_watt_consistency"] = False
                    checks["issues_found"].append(f"{inconsistent.sum()} kayıtta total_watt tutarsızlığı")
            
            # Negatif değer kontrolü
            numeric_cols = ['lighting_watt', 'projector_watt', 'plug_load_watt', 'total_watt', 'wasted_cost_tl']
            for col in numeric_cols:
                if col in self.df.columns:
                    negative_count = (self.df[col] < 0).sum()
                    if negative_count > 0:
                        checks["negative_values"] = True
                        checks["issues_found"].append(f"{col} kolonunda {negative_count} negatif değer")
            
            # Saat kontrolü
            if 'hour_of_day' in self.df.columns:
                invalid_hours = self.df[(self.df['hour_of_day'] < 0) | (self.df['hour_of_day'] > 23)]
                if len(invalid_hours) > 0:
                    checks["invalid_hours"] = True
                    checks["issues_found"].append(f"{len(invalid_hours)} geçersiz saat değeri")
            
            # Binary değer kontrolü
            binary_cols = ['is_class_in_session', 'is_anomaly', 'is_holiday', 'is_weekend']
            for col in binary_cols:
                if col in self.df.columns:
                    invalid_binary = self.df[~self.df[col].isin([0, 1])]
                    if len(invalid_binary) > 0:
                        checks["invalid_binary_values"] = True
                        checks["issues_found"].append(f"{col} kolonunda {len(invalid_binary)} geçersiz binary değer")
            
            # Duplicate kontrolü
            duplicates = self.df.duplicated().sum()
            if duplicates > 0:
                checks["duplicate_records"] = True
                checks["issues_found"].append(f"{duplicates} duplicate kayıt")
            
        except Exception as e:
            checks["issues_found"].append(f"Kalite kontrol hatası: {str(e)}")
        
        return checks
    
    def get_waste_analysis(self) -> Dict[str, Any]:
        """İsraf analizi yap"""
        if self.df is None:
            return {"error": "Veri yüklenmemiş"}
        
        try:
            # İsraf yapan kayıtlar
            waste_records = self.df[self.df['wasted_cost_tl'] > 0]
            
            # Oda bazında israf analizi
            room_waste = waste_records.groupby('room_id').agg({
                'wasted_cost_tl': ['sum', 'mean', 'count'],
                'total_watt': 'mean'
            }).round(2)
            
            room_waste.columns = ['total_wasted_cost', 'avg_wasted_cost', 'waste_incidents', 'avg_power']
            room_waste = room_waste.sort_values('total_wasted_cost', ascending=False)
            
            # Saat bazında israf analizi
            hour_waste = waste_records.groupby('hour_of_day').agg({
                'wasted_cost_tl': ['sum', 'count'],
                'total_watt': 'mean'
            }).round(2)
            
            hour_waste.columns = ['total_wasted_cost', 'waste_incidents', 'avg_power']
            
            # Gün bazında israf analizi
            daily_waste = waste_records.groupby('date').agg({
                'wasted_cost_tl': 'sum',
                'room_id': 'nunique'
            }).round(2)
            daily_waste.columns = ['daily_waste_cost', 'affected_rooms']
            
            return {
                "total_waste_records": len(waste_records),
                "total_waste_cost": float(waste_records['wasted_cost_tl'].sum()),
                "avg_waste_per_incident": float(waste_records['wasted_cost_tl'].mean()),
                "room_waste_analysis": room_waste.head(10).to_dict('index'),
                "hour_waste_analysis": hour_waste.to_dict('index'),
                "daily_waste_analysis": daily_waste.tail(7).to_dict('index'),  # Son 7 gün
                "top_wasting_rooms": room_waste.head(5).index.tolist(),
                "peak_waste_hours": hour_waste.sort_values('total_wasted_cost', ascending=False).head(3).index.tolist()
            }
            
        except Exception as e:
            return {"error": f"İsraf analizi hatası: {str(e)}"}
    
    def get_energy_patterns(self) -> Dict[str, Any]:
        """Enerji tüketim pattern'lerini analiz et"""
        if self.df is None:
            return {"error": "Veri yüklenmemiş"}
        
        try:
            # Günlük enerji tüketimi
            daily_energy = self.df.groupby(['date', 'room_id'])['total_watt'].sum().reset_index()
            daily_energy_avg = daily_energy.groupby('date')['total_watt'].mean()
            
            # Haftalık pattern
            self.df['datetime'] = pd.to_datetime(self.df['date'])
            self.df['day_of_week'] = self.df['datetime'].dt.day_name()
            
            weekly_pattern = self.df.groupby('day_of_week')['total_watt'].mean()
            
            # Saatlik pattern (ders vs ders dışı)
            hourly_pattern = self.df.groupby(['hour_of_day', 'is_class_in_session'])['total_watt'].mean().unstack()
            
            # Oda tipine göre ortalama tüketim
            room_type_energy = {}
            for room_id in self.df['room_id'].unique():
                room_type = '_'.join(room_id.split('_')[1:])  # Bina ID'sini kaldır
                if room_type not in room_type_energy:
                    room_type_energy[room_type] = []
                room_type_energy[room_type].extend(self.df[self.df['room_id'] == room_id]['total_watt'].tolist())
            
            room_type_stats = {}
            for room_type, values in room_type_energy.items():
                if values:
                    room_type_stats[room_type] = {
                        "avg_consumption": np.mean(values),
                        "max_consumption": np.max(values),
                        "min_consumption": np.min(values),
                        "sample_count": len(values)
                    }
            
            return {
                "daily_average_energy": daily_energy_avg.to_dict(),
                "weekly_pattern": weekly_pattern.to_dict(),
                "hourly_pattern": hourly_pattern.to_dict(),
                "room_type_statistics": room_type_stats,
                "peak_consumption_hour": int(self.df.groupby('hour_of_day')['total_watt'].mean().idxmax()),
                "lowest_consumption_hour": int(self.df.groupby('hour_of_day')['total_watt'].mean().idxmin())
            }
            
        except Exception as e:
            return {"error": f"Enerji pattern analizi hatası: {str(e)}"}
    
    def generate_summary_report(self) -> str:
        """Özet rapor oluştur"""
        if not self.analysis_results:
            return "Analiz sonuçları bulunamadı"
        
        basic = self.analysis_results.get("basic_info", {})
        quality = self.analysis_results.get("quality_checks", {})
        categorical = self.analysis_results.get("categorical_analysis", {})
        
        report = f"""
📊 VERİ ANALİZ RAPORU
==================

📈 Temel Bilgiler:
- Toplam Kayıt: {basic.get('total_rows', 'N/A'):,}
- Toplam Sütun: {basic.get('total_columns', 'N/A')}
- Benzersiz Oda: {basic.get('unique_rooms', 'N/A')}
- Tarih Aralığı: {basic.get('date_range', {}).get('start_date', 'N/A')} - {basic.get('date_range', {}).get('end_date', 'N/A')}
- Dosya Boyutu: {basic.get('file_size_mb', 'N/A')} MB

🔍 Veri Kalitesi:
- Toplam Watt Tutarlılığı: ✅ if quality.get('total_watt_consistency', False) else ❌
- Negatif Değerler: ❌ if quality.get('negative_values', False) else ✅
- Geçersiz Saatler: ❌ if quality.get('invalid_hours', False) else ✅
- Duplicate Kayıtlar: ❌ if quality.get('duplicate_records', False) else ✅

📚 Kategorik Analiz:
- Dersli Saat: {categorical.get('class_sessions', {}).get('with_classes', 'N/A'):,}
- Dersiz Saat: {categorical.get('class_sessions', {}).get('without_classes', 'N/A'):,}
- Anormal Kayıt: {categorical.get('anomalies', {}).get('anomalous', 'N/A'):,}
- Hafta İçi Günü: {categorical.get('day_types', {}).get('weekdays', 'N/A'):,}

⚠️ Bulunan Sorunlar:
"""
        
        if quality.get('issues_found'):
            for issue in quality['issues_found']:
                report += f"- {issue}\n"
        else:
            report += "- ✅ Hiçbir sorun bulunamadı\n"
        
        return report
