print("🔍 DataService Debug")

from data_service import DataService

# DataService oluştur
data_service = DataService()

# Test odası
room_id = "ENG101"

print(f"📍 Oda: {room_id}")

# Mevcut durumu al
current_status = data_service.get_room_current_status(room_id)

if current_status:
    print("✅ Mevcut durum alındı:")
    print(f"   room_id: {current_status.get('room_id')}")
    print(f"   room_name: {current_status.get('room_name')}")
    print(f"   power_consumption: {current_status.get('power_consumption')}")
    print(f"   occupancy_status: {current_status.get('occupancy_status')}")
    print(f"   hour_of_day: {current_status.get('hour_of_day')}")
    print(f"   lighting_watt: {current_status.get('lighting_watt')}")
    print(f"   projector_watt: {current_status.get('projector_watt')}")
    print(f"   plug_load_watt: {current_status.get('plug_load_watt')}")
    print(f"   is_weekend: {current_status.get('is_weekend')}")
    print(f"   is_holiday: {current_status.get('is_holiday')}")
    print(f"   Veri tipi: {type(current_status)}")
    
    # Tüm anahtarları göster
    print(f"   Tüm anahtarlar: {list(current_status.keys())}")
else:
    print("❌ Mevcut durum alınamadı")

# Tüm odaları test et
print("\n🏢 Tüm Odalar:")
all_rooms = data_service.get_all_rooms_current_status()
print(f"   Toplam oda: {len(all_rooms)}")

for room in all_rooms:
    print(f"   - {room.get('room_id')}: {room.get('power_consumption')}W")

print("\n🎉 Debug tamamlandı!")
