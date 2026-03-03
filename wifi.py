# wifi.py
import network
import socket
from config import *

def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=AP_SSID, password=AP_PASSWORD)
    ap.active(True)
    while not ap.active():
        pass
    print("AP active:", ap.ifconfig())
    return ap

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(1)
    return s
