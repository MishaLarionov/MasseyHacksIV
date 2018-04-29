# Webserver to take the distance between ultrasonic sensor and feet
# Sensors should have to connect to the websocket? idk

import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 6969               # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("New data! " + str(data))
            conn.sendall(b'Got data: ' + data)
