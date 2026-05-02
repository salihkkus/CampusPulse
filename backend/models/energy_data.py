from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from enum import IntEnum

class DayType(IntEnum):
    """Gün tipi için enum"""
    WEEKDAY = 0
    WEEKEND = 1
    HOLIDAY = 2

class EnergyDataRecord(BaseModel):
    """
    Eren'in gönderdiği veri formatına uygun Pydantic modeli
    Veri doğrulama ve tip kontrolü için kullanılır
    """
    
    # Temel bilgiler
    record_date: date = Field(..., description="Veri tarihi (YYYY-MM-DD formatında)")
    room_id: str = Field(..., description="Oda ID'si (örn: M2_Derslik_13)")
    hour_of_day: int = Field(..., ge=0, le=23, description="Saat (0-23 arası)")
    
    # Ders durumu
    is_class_in_session: int = Field(..., ge=0, le=1, description="Ders var mı? (0=Hayır, 1=Evet)")
    
    # Cihaz bazında güç tüketimi (Watt)
    lighting_watt: float = Field(..., ge=0, description="Aydınlatma güç tüketimi (Watt)")
    projector_watt: float = Field(..., ge=0, description="Projeksiyon güç tüketimi (Watt)")
    plug_load_watt: float = Field(..., ge=0, description="Prize takılı cihazların güç tüketimi (Watt)")
    
    # Toplam güç tüketimi
    total_watt: float = Field(..., ge=0, description="Toplam güç tüketimi (Watt)")
    
    # Anomali ve maliyet bilgileri
    is_anomaly: int = Field(..., ge=0, le=1, description="Anomali mi? (0=Hayır, 1=Evet)")
    wasted_cost_tl: float = Field(..., ge=0, description="Israf edilen maliyet (TL)")
    
    # Gün tipi bilgileri
    is_holiday: int = Field(..., ge=0, le=1, description="Tatil günü mü? (0=Hayır, 1=Evet)")
    is_weekend: int = Field(..., ge=0, le=1, description="Hafta sonu mu? (0=Hayır, 1=Evet)")
    
    @field_validator('total_watt')
    @classmethod
    def validate_total_watt(cls, v, info):
        """Toplam watt değerinin bileşenlerin toplamına eşit olduğunu kontrol et"""
        values = info.data if hasattr(info, 'data') else {}
        if 'lighting_watt' in values and 'projector_watt' in values and 'plug_load_watt' in values:
            expected_total = values['lighting_watt'] + values['projector_watt'] + values['plug_load_watt']
            # %5 tolerans verelim
            tolerance = expected_total * 0.05
            if abs(v - expected_total) > tolerance:
                raise ValueError(f"Toplam watt ({v}) bileşenlerin toplamından ({expected_total}) çok farklı")
        return v
    
    @field_validator('room_id')
    @classmethod
    def validate_room_id(cls, v):
        """Oda ID formatını kontrol et"""
        if not v or len(v) < 3:
            raise ValueError("Oda ID'si en az 3 karakter olmalı")
        
        # Beklenen format: Bina_Kategori_Numara (örn: M2_Derslik_13)
        parts = v.split('_')
        if len(parts) < 3:
            raise ValueError("Oda ID formatı 'Bina_Kategori_Numara' olmalı (örn: M2_Derslik_13)")
        
        return v
    
    @field_validator('wasted_cost_tl')
    @classmethod
    def validate_wasted_cost(cls, v, info):
        """Israf maliyetinin mantıksal olduğunu kontrol et"""
        values = info.data if hasattr(info, 'data') else {}
        if 'is_class_in_session' in values and 'total_watt' in values:
            # Ders varsa ve güç tüketimi düşükse israf olmamalı
            if values['is_class_in_session'] == 1 and values['total_watt'] < 1000:
                if v > 0:
                    raise ValueError("Ders varken düşük tüketimde israf maliyeti olmamalı")
        return v
    
    @field_validator('is_weekend', 'is_holiday')
    @classmethod
    def validate_day_types(cls, v, info):
        """Gün tipi tutarlılığını kontrol et"""
        field_name = info.field_name if hasattr(info, 'field_name') else ''
        values = info.data if hasattr(info, 'data') else {}
        
        if field_name == 'is_weekend' and v == 1:
            if 'is_holiday' in values and values['is_holiday'] == 1:
                # Hem hafta sonu hem tatil olabilir (örn: tatil pazartesi)
                pass
        return v
    
    def get_device_breakdown(self) -> dict:
        """Cihaz bazında güç dağılımını döndür"""
        return {
            "lighting": self.lighting_watt,
            "projector": self.projector_watt,
            "plug_load": self.plug_load_watt
        }
    
    def get_primary_device(self) -> str:
        """En çok güç tüketen cihazı döndür"""
        devices = self.get_device_breakdown()
        return max(devices, key=devices.get)
    
    def is_wasting_energy(self) -> bool:
        """Enerji israfı olup olmadığını kontrol et"""
        # Ders yoksa ve güç tüketimi yüksekse israf var
        if self.is_class_in_session == 0 and self.total_watt > 500:
            return True
        # Ders varsa ama anomali tespit edildiyse
        if self.is_class_in_session == 1 and self.is_anomaly == 1:
            return True
        return False
    
    def get_day_type(self) -> DayType:
        """Gün tipini döndür"""
        if self.is_holiday == 1:
            return DayType.HOLIDAY
        elif self.is_weekend == 1:
            return DayType.WEEKEND
        else:
            return DayType.WEEKDAY
    
    def to_dict(self) -> dict:
        """Modeli dictionary'e çevir"""
        return self.model_dump()
    
    def to_ai_format(self) -> dict:
        """AI motoru için format'a çevir"""
        return {
            "room_id": self.room_id,
            "timestamp": f"{self.record_date}T{self.hour_of_day:02d}:00:00Z",
            "power_consumption": self.total_watt,
            "occupancy_status": self.is_class_in_session,
            "devices": list(self.get_device_breakdown().keys()),
            "device_breakdown": self.get_device_breakdown(),
            "is_wasting": self.is_wasting_energy(),
            "wasted_cost": self.wasted_cost_tl,
            "is_anomaly": bool(self.is_anomaly),
            "day_type": self.get_day_type().name
        }
    
    class Config:
        """Pydantic config"""
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "record_date": "2023-11-02",
                "room_id": "M2_Derslik_13",
                "hour_of_day": 8,
                "is_class_in_session": 1,
                "lighting_watt": 400.0,
                "projector_watt": 250.0,
                "plug_load_watt": 9150.0,
                "total_watt": 9800.0,
                "is_anomaly": 0,
                "wasted_cost_tl": 0.0,
                "is_holiday": 0,
                "is_weekend": 0
            }
        }

class EnergyDataBatch(BaseModel):
    """
    Toplu enerji verisi için model
    Eren'den gelen veri setlerini batch halinde işlemek için
    """
    records: List[EnergyDataRecord] = Field(..., description="Enerji verisi kayıtları")
    batch_id: Optional[str] = Field(None, description="Batch ID")
    uploaded_at: Optional[datetime] = Field(default_factory=datetime.now, description="Yükleme zamanı")
    
    @field_validator('records')
    @classmethod
    def validate_records_not_empty(cls, v):
        """Kayıt listesinin boş olmadığını kontrol et"""
        if not v:
            raise ValueError("En az bir enerji verisi kaydı gereklidir")
        return v
    
    def get_summary(self) -> dict:
        """Batch özetini döndür"""
        total_records = len(self.records)
        total_watt = sum(record.total_watt for record in self.records)
        total_wasted_cost = sum(record.wasted_cost_tl for record in self.records)
        wasting_records = [r for r in self.records if r.is_wasting_energy()]
        anomaly_records = [r for r in self.records if r.is_anomaly == 1]
        
        return {
            "batch_id": self.batch_id,
            "total_records": total_records,
            "total_watt": total_watt,
            "total_wasted_cost": total_wasted_cost,
            "wasting_records_count": len(wasting_records),
            "wasting_percentage": (len(wasting_records) / total_records) * 100 if total_records > 0 else 0,
            "anomaly_records_count": len(anomaly_records),
            "anomaly_percentage": (len(anomaly_records) / total_records) * 100 if total_records > 0 else 0,
            "unique_rooms": len(set(record.room_id for record in self.records)),
            "date_range": {
                "start": min(record.record_date for record in self.records).isoformat(),
                "end": max(record.record_date for record in self.records).isoformat()
            }
        }
    
    def filter_by_room(self, room_id: str) -> List[EnergyDataRecord]:
        """Belirli bir oda için kayıtları filtrele"""
        return [record for record in self.records if record.room_id == room_id]
    
    def filter_by_date_range(self, start_date: date, end_date: date) -> List[EnergyDataRecord]:
        """Tarih aralığına göre kayıtları filtrele"""
        return [record for record in self.records 
                if start_date <= record.record_date <= end_date]

class EnergyDataValidationResponse(BaseModel):
    """Veri doğrulama response modeli"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    processed_records: int = 0
    batch_summary: Optional[dict] = None
