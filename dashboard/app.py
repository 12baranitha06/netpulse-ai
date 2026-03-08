import csv
from flask import send_file
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.health_prediction import predict_health
from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder=".")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "network_data.db")

def get_latest_data():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM network_metrics ORDER BY time DESC LIMIT 10")

    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    times = []
    latency = []
    loss = []

    for row in rows:
        times.append(row[0])
        latency.append(row[1])
        loss.append(row[2])

    return times, latency, loss


    for row in rows:
        times.append(row[0])
        latency.append(row[1])
        loss.append(row[2])

    return times, latency, loss


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():

    times, latency, loss = get_latest_data()

    if latency and loss:
        status = predict_health(latency[-1], loss[-1])
    else:
        status = "Unknown"

    return jsonify({
        "times": times,
        "latency": latency,
        "loss": loss,
        "status": status
    })

@app.route("/download")
def download():

    import sqlite3
    import csv
    import os

    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "network_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM network_metrics")
    rows = cursor.fetchall()

    file_path = os.path.join(os.path.dirname(__file__), "network_logs.csv")

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Latency", "Packet Loss"])
        writer.writerows(rows)

    conn.close()

    return send_file(file_path, as_attachment=True)  

if __name__ == "__main__":
    app.run(debug=True)