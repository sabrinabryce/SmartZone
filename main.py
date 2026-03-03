# main.py
import utime
import web
import log
from wifi import *
from control import *
from actuators import ir_emitter

# -----------------------------
# Network Setup
# -----------------------------
ap = start_ap()
server = start_server()

ir_emitter(True)

print("SmartZone System Started")

# -----------------------------
# Main Loop
# -----------------------------
while True:

    state = update_system()
    log.log_state(state)

    try:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()
        path = request.split(" ")[1]

        response = web.route(path, state)

        conn.send("HTTP/1.1 200 OK\r\n")

        if path.startswith("/status"):
            conn.send("Content-Type: application/json\r\n")
            conn.send("Cache-Control: no-cache\r\n")
        else:
            conn.send("Content-Type: text/html\r\n")

        conn.send("Connection: close\r\n\r\n")
        conn.sendall(response)
        conn.close()

    except OSError:
        pass


