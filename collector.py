# Import library 
import time
import sqlite3
import requests
from datetime import datetime, timezone

DB_PATH = "flights.db"
API_URL = "https://opensky-network.org/api/states/all"

# Perak bounding box 
PARAMS = {
    "lamin": 3.6,
    "lamax": 6.8,
    "lomin": 100.0,
    "lomax": 102.6
}

POLL_SECONDS = 300 # 5 minutes

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS state_vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collected_at_utc TEXT NOT NULL,
        opensky_time INTEGER,
        icao24 TEXT,
        callsign TEXT,
        origin_country TEXT,
        longitude REAL,
        latitude REAL,
        baro_altitude REAL,
        on_ground INTEGER,
        velocity REAL,
        true_track REAL,
        vertical_rate REAL,
        geo_altitude REAL
        )
        """)
    
    conn.commit()
    conn.close()

def insert_rows(rows):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executemany("""
    INSERT INTO state_vectors (
        collected_at_utc,
        opensky_time,
        icao24,
        callsign,
        origin_country,
        longitude,
        latitude,
        baro_altitude,
        on_ground,
        velocity,
        true_track,
        vertical_rate,
        geo_altitude
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()

def fetch_states():
    response = requests.get(API_URL, params=PARAMS, timeout=30)

    if response.status_code == 429:
        print("Rate Limit reached (429). Waiting longer before next request...")
        return None
    response.raise_for_status()
    return response.json()
        
def main():
    init_db()
    print("Collected starter.... saving data to flights.db")

    while True:
        collected_at = datetime.now(timezone.utc).isoformat()

        try:
            data = fetch_states()

            if data is None:
                time.sleep(POLL_SECONDS)
                continue
            
            opensky_time = data.get("time")
            states = data.get("states", [])

            if not states:
                print(f"[{collected_at}] No aircraft data returned.")
                time.sleep(POLL_SECONDS)
                continue

            rows = []
            for s in states:
                rows.append((
                    collected_at,
                    opensky_time,
                    s[0],
                    s[1].strip() if s[1] else None,
                    s[2],
                    s[5],
                    s[6],
                    s[7],
                    int(s[8]) if s[8] is not None else None,
                    s[9],
                    s[10],
                    s[11],
                    s[13]
                ))

            insert_rows(rows)
            print(f"[{collected_at}] Saved {len(rows)} records.")

        except Exception as e:
            print(f"[{collected_at}] ERROR: {e}")

        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()