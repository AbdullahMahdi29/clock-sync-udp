import socket
import tkinter as tk
from datetime import datetime
from datetime import date
import time
import random

SERVER_IP = "127.0.0.1"
PORT = 12345

def sync_time():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2)   # timeout for packet loss

    retries = 3
    success = False

    for attempt in range(retries):
        try:
            # Local time BEFORE sync
            t0 = datetime.now()

            # Simulated network delay
            delay = random.uniform(0.1, 1.0)
            time.sleep(delay)

            client.sendto(b"time", (SERVER_IP, PORT))
            data, _ = client.recvfrom(1024)

            t1 = datetime.now()
            success = True
            break

        except (socket.timeout, ConnectionResetError):
            print("Packet lost... retrying")

    if not success:
        local_label.config(text="Local Time: ---")
        server_label.config(text="Server Time: No Response")
        adjusted_label.config(text="Adjusted Time: ---")
        delay_label.config(text="Delay: ---")
        diff_label.config(text="Difference: Packet Lost")
        client.close()
        return

    server_time_parsed = datetime.strptime(data.decode(), "%H:%M:%S.%f")
    server_time = datetime.combine(date.today(), server_time_parsed.time())

    # Round Trip Delay
    rtt = (t1 - t0).total_seconds()

    # Adjusted time
    adjusted_time = server_time + (t1 - t0) / 2

    # Display
    local_label.config(text=f"Local Time: {t0.strftime('%H:%M:%S.%f')}")
    server_label.config(text=f"Server Time: {server_time}")
    adjusted_label.config(text=f"Adjusted Time: {adjusted_time}")
    delay_label.config(text=f"Simulated Delay: {delay:.3f}s")
    diff_label.config(text=f"Before Sync Diff: {rtt:.3f}s")

    client.close()

# GUI
root = tk.Tk()
root.title("Distributed Clock Sync (UDP)")
root.geometry("400x300")

tk.Label(root, text="Clock Synchronization", font=("Arial", 14)).pack(pady=10)

local_label = tk.Label(root, text="Local Time:")
local_label.pack()

server_label = tk.Label(root, text="Server Time:")
server_label.pack()

adjusted_label = tk.Label(root, text="Adjusted Time:")
adjusted_label.pack()

delay_label = tk.Label(root, text="Delay:")
delay_label.pack()

diff_label = tk.Label(root, text="Difference:")
diff_label.pack()

tk.Button(root, text="Sync Time", command=sync_time).pack(pady=10)

root.mainloop()