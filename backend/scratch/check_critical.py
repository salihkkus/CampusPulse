import urllib.request
import json

r = urllib.request.urlopen('http://localhost:8000/api/v2/ai/batch-analysis')
d = json.loads(r.read())
rooms = d['data']['rooms']
critical = [x for x in rooms if x['status'] == 'CRITICAL']
print(f"Toplam oda: {len(rooms)}, Kritik: {len(critical)}")
print()
for rm in critical[:5]:
    fin = rm['analysis']['financial']
    cur = rm['current_data']
    print(f"  {rm['room_id']}:")
    print(f"    power = {cur['power_consumption']}W")
    print(f"    wasted_cost_per_hour = {fin['wasted_cost_per_hour']}")
    print(f"    daily_cost = {fin['daily_cost']}")
    print(f"    instant_carbon_per_hour = {fin['instant_carbon_per_hour']}")
    print(f"    occupancy = {cur['occupancy_status']}")
    print(f"    devices = {cur['detected_devices']}")
    print()
