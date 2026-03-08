import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ai.health_prediction import predict_health
import sqlite3
import time
from ping3 import ping
import speedtest

# connect database
conn = sqlite3.connect("database/network_data.db")
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS network_metrics (
    time TEXT,
    latency REAL,
    packet_loss REAL,
    download REAL,
    upload REAL,
    health TEXT
)
""")

conn.commit()


def check_latency():
    latency = ping("8.8.8.8")
    if latency:
        return round(latency * 1000, 2)
    return None


def check_packet_loss():
    lost = 0
    total = 5

    for i in range(total):
        if ping("8.8.8.8") is None:
            lost += 1

    return (lost / total) * 100


def check_speed():
    try:
        st = speedtest.Speedtest()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        return round(download,2), round(upload,2)
    except:
        return 0, 0


def health_status(latency, loss):

    if latency < 50 and loss < 1:
        return "Healthy"
    elif latency < 100 and loss < 5:
        return "Warning"
    else:
        return "Critical"


while True:

    latency = check_latency()
    packet_loss = check_packet_loss()
    download = 0
    upload = 0

    health = predict_health(latency, packet_loss)

    print("\n----- Network Report -----")
    print("Latency:", latency, "ms")
    print("Packet Loss:", packet_loss, "%")
    print("Download:", download, "Mbps")
    print("Upload:", upload, "Mbps")
    print("Health:", health)

    cursor.execute(
        "INSERT INTO network_metrics VALUES (datetime('now'),?,?,?,?,?)",
        (latency, packet_loss, download, upload, health)
    )

    conn.commit()

    time.sleep(15)