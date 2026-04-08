import socket
import threading
from datetime import datetime

SERVER_IP = "127.0.0.1"
PORT = 12345


def client_task(id):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2)

    retries = 3
    success = False

    for attempt in range(retries):
        try:
            # send time
            t0 = datetime.now()

            client.sendto(b"time", (SERVER_IP, PORT))

            data, _ = client.recvfrom(1024)

            t1 = datetime.now()

            success = True
            break

        except socket.timeout:
            print(f"Client {id} packet lost... retrying")

    if not success:
        print(f"Client {id} failed to sync")
        client.close()
        return

    rtt = (t1 - t0).total_seconds()
    print(f"Client {id} RTT: {rtt:.6f} sec")

    client.close()


threads = []

# simulate 5 clients
for i in range(5):
    t = threading.Thread(target=client_task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Performance Test Completed")