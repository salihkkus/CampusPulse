# CampusPulse API Dokümantasyonu

## Genel Bakış

CampusPulse FastAPI backend'i enerji israfı tespiti ve teşhis sistemi için REST API endpoint'leri sunar.

**Base URL:** `http://localhost:8000`

## API Versiyonları

### v1 API - Orijinal Endpoint'ler
- Temel oda durumu ve veri yönetimi

### v2 API - Geliştirilmiş AI Endpoint'leri
- AI analizi, teşhis ve finansal hesaplamalar

---

## v2 AI Endpoint'leri

### 1. Model Bilgileri

**GET** `/api/v2/ai/model-info`

AI modeli hakkında bilgi döndürür.

**Response:**
```json
{
  "success": true,
  "data": {
    "model_type": "IsolationForest",
    "is_trained": true,
    "features": ["total_watt", "hour_of_day", "is_class_in_session", ...],
    "training_stats": {
      "total_samples": 56161,
      "detected_anomalies": 5616,
      "anomaly_rate": 0.1
    }
  }
}
```

---

### 2. Hızlı Teşhis

**GET** `/api/v2/ai/quick-diagnosis/{room_id}`

Belirli bir oda için hızlı teşhis döndürür.

**Response:**
```json
{
  "success": true,
  "data": {
    "room_id": "M1_Derslik_01",
    "diagnosis": "⚠️ Klima açık unutulmuş: klima",
    "timestamp": "2023-11-15T14:30:00Z"
  }
}
```

---

### 3. Kapsamlı Oda Analizi

**GET** `/api/v2/ai/analysis/{room_id}`

Belirli bir oda için detaylı analiz döndürür.

**Response:**
```json
{
  "success": true,
  "data": {
    "room_id": "M1_Derslik_01",
    "status": "CRITICAL",
    "urgency_level": "HIGH",
    "confidence": 0.85,
    "analysis": {
      "anomaly": {
        "is_anomaly": true,
        "anomaly_score": -0.15,
        "confidence": 0.85
      },
      "diagnosis": {
        "is_wasting": true,
        "primary_issue": "Klima açık unutulmuş",
        "detected_devices": ["klima"],
        "potential_savings": 3000.0
      },
      "financial": {
        "instant_loss_per_hour": 6.25,
        "daily_cost": 50.0,
        "monthly_cost": 1100.0,
        "wasted_cost_per_hour": 6.25,
        "potential_monthly_savings": 3000.0
      }
    },
    "current_data": {
      "power_consumption": 2500,
      "occupancy_status": 0,
      "detected_devices": ["klima"]
    },
    "recommendations": [
      {
        "type": "action",
        "title": "Klima açık unutulmuş",
        "description": "Oda boş iken klima çalışıyor. Hemen kapatın.",
        "action": "Klimayı kapat",
        "priority": "HIGH",
        "savings": "Ayda ~3000TL tasarruf"
      }
    ]
  }
}
```

---

### 4. Frontend Oda Durumu

**GET** `/api/v2/ai/room-status/{room_id}`

Muhammet'in frontend'i için optimize edilmiş oda durumu.

**Response:**
```json
{
  "success": true,
  "data": {
    "room_id": "M1_Derslik_01",
    "room_name": "M1 Derslik 01",
    "building": "M1",
    "floor": 1,
    "status": "CRITICAL",
    "is_wasting_energy": true,
    "is_anomaly": true,
    "urgency_level": "HIGH",
    "current_power": 2500,
    "occupancy_status": 0,
    "detected_devices": ["klima"],
    "instant_loss_tl_per_hour": 6.25,
    "daily_cost_tl": 50.0,
    "carbon_kg_per_hour": 1.125,
    "diagnostic_message": "Klima açık unutulmuş",
    "primary_device": "klima",
    "recommendations": [...],
    "confidence": 0.85,
    "timestamp": "2023-11-15T14:30:00Z"
  }
}
```

---

### 5. Toplu Analiz

**GET** `/api/v2/ai/batch-analysis`

Tüm odalar için toplu analiz.

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_rooms": 50,
      "wasting_rooms": 12,
      "critical_rooms": 3,
      "total_waste_cost": 75.50,
      "total_potential_savings": 15000.0
    },
    "rooms": [...],
    "timestamp": "2023-11-15T14:30:00Z"
  }
}
```

---

### 6. Dashboard Özeti

**GET** `/api/v2/ai/dashboard-summary`

Dashboard için özet veriler.

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_rooms": 50,
      "wasting_rooms": 12,
      "critical_rooms": 3,
      "normal_rooms": 38,
      "total_waste_per_hour": 75.50,
      "total_potential_savings": 15000.0,
      "waste_percentage": 24.0
    },
    "critical_rooms": [
      {
        "room_id": "M1_Derslik_01",
        "status": "CRITICAL",
        "issue": "Klima açık unutulmuş",
        "urgency": "HIGH",
        "waste_per_hour": 6.25
      }
    ],
    "top_wasters": [
      {
        "room_id": "M2_Derslik_02",
        "waste_per_hour": 8.50,
        "devices": ["pc_20_adet", "klima"],
        "issue": "Bilgisayarlar açık kalmış"
      }
    ],
    "recommendations": [...],
    "timestamp": "2023-11-15T14:30:00Z"
  }
}
```

---

### 7. Özel Analiz

**POST** `/api/v2/ai/custom-analysis`

Özel veri için analiz.

**Request Body:**
```json
{
  "room_id": "Test_Derslik_01",
  "occupancy_status": 0,
  "hour_of_day": 14,
  "total_power": 2500,
  "lighting_watt": 400,
  "projector_watt": 0,
  "plug_load_watt": 2100,
  "is_weekend": 0,
  "is_holiday": 0
}
```

**Response:** Kapsamlı oda analizi ile aynı format.

---

## Hata Kodları

- **200**: Başarılı
- **404**: Oda bulunamadı
- **500**: Sunucu hatası

**Hata Response Format:**
```json
{
  "detail": "Room M1_Derslik_99 not found"
}
```

---

## Frontend Kullanım Örnekleri

### React/JavaScript

```javascript
// Oda durumu al
const response = await fetch('/api/v2/ai/room-status/M1_Derslik_01');
const roomData = await response.json();

if (roomData.success) {
  const room = roomData.data;
  console.log(`Durum: ${room.status}`);
  console.log(`Mesaj: ${room.diagnostic_message}`);
  console.log(`Maliyet: ${room.instant_loss_tl_per_hour}TL/saat`);
}
```

### Dashboard verisi

```javascript
// Dashboard özeti
const dashboardResponse = await fetch('/api/v2/ai/dashboard-summary');
const dashboardData = await dashboardResponse.json();

if (dashboardData.success) {
  const summary = dashboardData.data.summary;
  console.log(`İsraf oranı: ${summary.waste_percentage}%`);
  console.log(`Potansiyel tasarruf: ${summary.total_potential_savings}TL/ay`);
}
```

---

## Model Performansı

- **Accuracy**: ~85%
- **Processing Time**: <100ms per request
- **Confidence**: 70-95%
- **Features**: 8 adet (güç, zaman, doluluk, vb.)

---

## Güvenlik

- CORS ayarları: `http://localhost:3000`
- Rate limiting: Yok (development)
- Authentication: Yok (development)

---

## Development

### Sunucuyu Başlatma

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Test Etme

```bash
python test_endpoints.py
```

### Dokümantasyon

Swagger UI: `http://localhost:8000/docs`

---

## Muhammet İçin Notlar

1. **Ana Endpoint**: `/api/v2/ai/room-status/{room_id}`
2. **Dashboard**: `/api/v2/ai/dashboard-summary`
3. **Hızlı Mesaj**: `/api/v2/ai/quick-diagnosis/{room_id}`
4. **Format**: Tüm response'lar `{success: true, data: {...}}` formatında
5. **Hata**: `response.json().detail` üzerinden erişilebilir

**Önemli Alanlar:**
- `status`: NORMAL, ACTIVE, ATTENTION, WARNING, CRITICAL, ANOMALY
- `diagnostic_message`: "Klima açık unutulmuş"
- `instant_loss_tl_per_hour`: Anlık maliyet
- `recommendations`: Yapılacaklar listesi
