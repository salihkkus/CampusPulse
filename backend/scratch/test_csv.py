import pandas as pd
import os

csv_file = "../kampus_1_aylik_enerji.csv"
print(f"Checking {csv_file}")
print(f"Exists: {os.path.exists(csv_file)}")

try:
    df = pd.read_csv(csv_file)
    print(f"Loaded successfully. Rows: {len(df)}")
    print(df.head())
    
    df['timestamp'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour_of_day'], unit='h')
    print("Timestamp conversion successful")
    
    unique_rooms = df['room_id'].unique()
    print(f"Unique rooms: {unique_rooms}")
except Exception as e:
    print(f"Error: {e}")
