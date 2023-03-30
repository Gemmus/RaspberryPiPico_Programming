import network
import socket
from time import sleep
from machine import Pin

led_onboard = Pin("LED", Pin.OUT)

ssid = 'KMD758Group5'
password = '105105105M'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
        
try:
    connect()
except KeyboardInterrupt:
    machine.reset()