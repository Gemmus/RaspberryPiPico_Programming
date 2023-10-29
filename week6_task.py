# The aim is to learn to use the Raspberry Pi Pico W to make HTTP requests to a server and handle the responses from those servers. 

import network
import socket
from time import sleep
import ssd1306
from machine import Pin, I2C
import urequests as requests
import ujson

i2c = I2C(1, sda=Pin(14), scl=Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

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
    print(f"The IP address is : {ip}")
    return ip
    
try:
    ip = connect()
    r = requests.get(url="http://192.168.105.143:8000")
    print(r.status_code)
except KeyboardInterrupt:
    machine.reset()

APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"

LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

try:
    response = requests.post(
        url = TOKEN_URL,
        data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
        headers = {'Content-Type':'application/x-www-form-urlencoded'},
        auth = (CLIENT_ID, CLIENT_SECRET))
    
    response = response.json()
    access_token = response["access_token"]
    intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]
    
    data_set = {
        "type": "RRI",
        "data": intervals,
        "analysis": {"type": "readiness"}
        }
      
    response = requests.post(
        url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
        headers = { "Authorization": "Bearer {}".format(access_token),
                    "X-Api-Key": APIKEY },
        json = data_set)
    
    response = response.json()
    print(response)
    
    SNS = response['analysis']['sns_index']
    PNS = response['analysis']['pns_index']

    print("SNS: ", SNS)
    print("PNS: ", PNS)

    
    oled.text(f'SNS: {SNS}', 0, 0, 1)
    oled.text(f'PNS: {PNS}', 0, 10, 1)
    oled.show()
    
except KeyboardInterrupt:
    machine.reset()
