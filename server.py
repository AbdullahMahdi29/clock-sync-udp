import socket
import datetime

HOST = "127.0.0.1"
PORT = 12345

# Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket to address
server.bind((HOST, PORT))

print("UDP Time Server Started...")

while True:
    try:
        # Receive request from client
        data, addr = server.recvfrom(1024)

        # Get current server time
        server_time = datetime.datetime.now().strftime("%H:%M:%S.%f")

        print(f"Request from {addr}")

        # Send time back to client
        server.sendto(server_time.encode(), addr)

    except Exception as e:
        print("Server Error:", e)