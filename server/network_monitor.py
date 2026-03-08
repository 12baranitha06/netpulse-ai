from ping3 import ping
import speedtest
import time

def check_latency():
    latency = ping("8.8.8.8")
    if latency:
        return round(latency * 1000, 2)
    else:
        return None

def check_speed():
    st = speedtest.Speedtest()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    return round(download,2), round(upload,2)

while True:
    latency = check_latency()
    download, upload = check_speed()

    print("----- Network Status -----")
    print(f"Latency: {latency} ms")
    print(f"Download Speed: {download} Mbps")
    print(f"Upload Speed: {upload} Mbps")

    time.sleep(10)