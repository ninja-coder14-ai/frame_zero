import os
import time
import random
import requests
from dotenv import load_dotenv

load_dotenv()

LOKI_URL = os.getenv("LOKI_URL")
LOKI_USER = os.getenv("LOKI_USER")
LOKI_TOKEN = os.getenv("LOKI_TOKEN")

COUNTRIES = ["US", "UK", "DE", "PK", "IN", "BR"]
SUSPICIOUS_COUNTRIES = ["RU", "KP", "XX"]

def push_log(stream_labels, message):
    timestamp_ns = str(int(time.time() * 1_000_000_000))
    payload = {
        "streams": [
            {
                "stream": stream_labels,
                "values": [[timestamp_ns, message]],
            }
        ]
    }
    resp = requests.post(
        LOKI_URL,
        json=payload,
        auth=(LOKI_USER, LOKI_TOKEN),
        headers={"Content-Type": "application/json"},
    )
    if resp.status_code not in (200, 204):
        print(f"FAILED ({resp.status_code}): {resp.text}")
    else:
        print(f"Sent: {message}")

def generate_normal_event():
    country = random.choice(COUNTRIES)
    asset_id = f"asset-{random.randint(1000,9999)}"
    push_log(
        {"service": "drm-auth", "level": "info"},
        f"DRM auth SUCCESS asset={asset_id} country={country} user=crew_{random.randint(1,20)}",
    )

def generate_anomaly_event():
    country = random.choice(SUSPICIOUS_COUNTRIES)
    asset_id = f"asset-{random.randint(1000,9999)}"
    push_log(
        {"service": "drm-auth", "level": "warning"},
        f"DRM auth FAILED asset={asset_id} country={country} attempts=7 reason=invalid_token",
    )

if __name__ == "__main__":
    print("Pushing synthetic pipeline data to Loki... Ctrl+C to stop.")
    while True:
        if random.random() < 0.15:
            generate_anomaly_event()
        else:
            generate_normal_event()
        time.sleep(2)
