import urllib.request
import json

# Saat 10:00 UTC = 13:00 TR (ders saati)
ts = "2023-11-15T10:00:00Z"
url = f"http://localhost:8000/api/v2/ai/batch-analysis?timestamp={ts}"
r = urllib.request.urlopen(url)
d = json.loads(r.read())
rooms = d['data']['rooms']

# Doluluk durumlarini say
occ_full = sum(1 for rm in rooms if rm['current_data']['occupancy_status'] == 1)
occ_empty = sum(1 for rm in rooms if rm['current_data']['occupancy_status'] == 0)
critical = [x for x in rooms if x['status'] == 'CRITICAL']

print(f"Timestamp: {ts}")
print(f"Toplam oda: {len(rooms)}")
print(f"  Dolu: {occ_full}, Bos: {occ_empty}")
print(f"  Kritik: {len(critical)}")
print()

# Ilk 5 odanin durumunu goster
for rm in rooms[:5]:
    cur = rm['current_data']
    print(f"  {rm['room_id']}: {rm['status']}, power={cur['power_consumption']}W, occ={'Dolu' if cur['occupancy_status'] else 'Bos'}")
