import pandas as pd

df = pd.read_csv(r"c:\Users\Muhammet Canlı\Documents\GitHub\CampusPulse\kampus_1_aylik_enerji.csv")

# Son zaman damgasini bul (en son veri)
last_ts = df.sort_values(['date', 'hour_of_day']).iloc[-1]
last_date = last_ts['date']
last_hour = last_ts['hour_of_day']

print(f"Son tarih: {last_date}, Son saat: {last_hour}")

# O andaki kritik 3 oda
critical_rooms = ['AKM_Derslik_08', 'AKM_Derslik_03', 'M2_Derslik_14']
for rid in critical_rooms:
    row = df[(df['room_id'] == rid) & (df['date'] == last_date) & (df['hour_of_day'] == last_hour)]
    if not row.empty:
        r = row.iloc[0]
        print(f"\n{rid}:")
        print(f"  total_watt = {r['total_watt']}")
        print(f"  is_class_in_session = {r['is_class_in_session']}")
        print(f"  is_anomaly = {r['is_anomaly']}")
        print(f"  lighting = {r['lighting_watt']}, projector = {r['projector_watt']}, plug = {r['plug_load_watt']}")
        print(f"  wasted_cost_tl = {r['wasted_cost_tl']}")
    else:
        print(f"\n{rid}: veri bulunamadi")

# Bu odaların hep 650W mu oldugunu kontrol et
print("\n--- SON 5 SAAT ---")
for rid in critical_rooms:
    rows = df[(df['room_id'] == rid) & (df['date'] == last_date)].sort_values('hour_of_day').tail(5)
    print(f"\n{rid}:")
    for _, r in rows.iterrows():
        print(f"  saat={r['hour_of_day']}: total={r['total_watt']}W, occ={r['is_class_in_session']}, waste={r['wasted_cost_tl']}")
