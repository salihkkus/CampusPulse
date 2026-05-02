from fastapi import APIRouter, Depends
from typing import Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import EnergyRecordDB
from models.energy_data import EnergyDataRecord, EnergyDataBatch, EnergyDataValidationResponse

router = APIRouter(prefix="/api/v1/data", tags=["Data Storage"])

@router.post("/upload", response_model=EnergyDataValidationResponse)
async def upload_energy_data(record: EnergyDataRecord, db: Session = Depends(get_db)):
    try:
        db_record = EnergyRecordDB(
            record_date=record.record_date,
            room_id=record.room_id,
            hour_of_day=record.hour_of_day,
            is_class_in_session=record.is_class_in_session,
            lighting_watt=record.lighting_watt,
            projector_watt=record.projector_watt,
            plug_load_watt=record.plug_load_watt,
            total_watt=record.total_watt,
            is_anomaly=record.is_anomaly,
            wasted_cost_tl=record.wasted_cost_tl,
            is_holiday=record.is_holiday,
            is_weekend=record.is_weekend,
            uploaded_at=datetime.now()
        )
        db.add(db_record)
        db.commit()
        return EnergyDataValidationResponse(
            is_valid=True,
            processed_records=1,
            warnings=[],
            errors=[]
        )
    except Exception as e:
        db.rollback()
        return EnergyDataValidationResponse(
            is_valid=False,
            processed_records=0,
            errors=[f"Veri işleme hatası: {str(e)}"]
        )

@router.post("/batch-upload", response_model=EnergyDataValidationResponse)
async def upload_energy_data_batch(batch: EnergyDataBatch, db: Session = Depends(get_db)):
    try:
        for record in batch.records:
            db_record = EnergyRecordDB(
                record_date=record.record_date,
                room_id=record.room_id,
                hour_of_day=record.hour_of_day,
                is_class_in_session=record.is_class_in_session,
                lighting_watt=record.lighting_watt,
                projector_watt=record.projector_watt,
                plug_load_watt=record.plug_load_watt,
                total_watt=record.total_watt,
                is_anomaly=record.is_anomaly,
                wasted_cost_tl=record.wasted_cost_tl,
                is_holiday=record.is_holiday,
                is_weekend=record.is_weekend,
                uploaded_at=datetime.now()
            )
            db.add(db_record)
        db.commit()
        summary = batch.get_summary()
        return EnergyDataValidationResponse(
            is_valid=True,
            processed_records=len(batch.records),
            batch_summary=summary,
            warnings=[],
            errors=[]
        )
    except Exception as e:
        db.rollback()
        return EnergyDataValidationResponse(
            is_valid=False,
            processed_records=0,
            errors=[f"Batch işleme hatası: {str(e)}"]
        )

@router.get("/records")
async def get_energy_records(
    room_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(EnergyRecordDB)
    if room_id: query = query.filter(EnergyRecordDB.room_id == room_id)
    if start_date: query = query.filter(EnergyRecordDB.record_date >= start_date)
    if end_date: query = query.filter(EnergyRecordDB.record_date <= end_date)
    
    records = query.limit(limit).all()
    total_count = db.query(EnergyRecordDB).count()
    
    return {
        "total_records": total_count,
        "filtered_records": len(records),
        "records": [
            {
                "record_date": str(r.record_date),
                "room_id": r.room_id,
                "hour_of_day": r.hour_of_day,
                "is_class_in_session": r.is_class_in_session,
                "lighting_watt": r.lighting_watt,
                "projector_watt": r.projector_watt,
                "plug_load_watt": r.plug_load_watt,
                "total_watt": r.total_watt,
                "is_anomaly": r.is_anomaly,
                "wasted_cost_tl": r.wasted_cost_tl,
                "is_holiday": r.is_holiday,
                "is_weekend": r.is_weekend
            } for r in records
        ]
    }

@router.get("/rooms")
async def get_available_rooms(db: Session = Depends(get_db)):
    records = db.query(EnergyRecordDB).all()
    unique_rooms = list(set(r.room_id for r in records))
    room_stats = {}
    
    for room_id in unique_rooms:
        room_records = [r for r in records if r.room_id == room_id]
        total_watt = sum(r.total_watt for r in room_records)
        wasted_cost = sum(r.wasted_cost_tl for r in room_records)
        
        wasting_count = sum(1 for r in room_records if (r.is_class_in_session == 0 and r.total_watt > 500) or (r.is_class_in_session == 1 and r.is_anomaly == 1))
        
        room_stats[room_id] = {
            "record_count": len(room_records),
            "total_watt": total_watt,
            "total_wasted_cost": wasted_cost,
            "wasting_percentage": (wasting_count / len(room_records)) * 100 if room_records else 0,
            "avg_watt": total_watt / len(room_records) if room_records else 0
        }
        
    return {"total_rooms": len(unique_rooms), "rooms": room_stats}

@router.delete("/clear")
async def clear_energy_data(db: Session = Depends(get_db)):
    record_count = db.query(EnergyRecordDB).delete()
    db.commit()
    return {
        "message": f"{record_count} kayıt başarıyla temizlendi",
        "cleared_at": datetime.now().isoformat()
    }
