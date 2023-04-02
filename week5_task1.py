import network
import socket
import ssd1306
from time import sleep
from machine import Pin, I2C

# OLED
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# SSID
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
    oled.text(ip, 10, 30, 1)
    oled.show()
    return ip
        
try:
    connect()
except KeyboardInterrupt:
    machine.reset()

