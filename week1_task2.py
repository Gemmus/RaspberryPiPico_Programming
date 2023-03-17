from machine import Pin
import time

led_onboard = Pin("LED", Pin.OUT)
led3= Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led1 = Pin(20, Pin.OUT)

def timedblink():
    led_onboard.value(0)
    time.sleep(0.85)
    led_onboard.value(1)
    time.sleep(0.15)

while True:
    led3.value(0)
    led2.value(0)
    led1.value(0)
    timedblink()
    
    led3.value(0)
    led2.value(0)
    led1.value(1)
    timedblink()
  
    led3.value(0)
    led2.value(1)
    led1.value(0)
    timedblink()

    led3.value(0)
    led2.value(1)
    led1.value(1)
    timedblink()

    led3.value(1)
    led2.value(0)
    led1.value(0)
    timedblink()

    led3.value(1)
    led2.value(0)
    led1.value(1)
    timedblink()
    
    led3.value(1)
    led2.value(1)
    led1.value(0)
    timedblink()

    led3.value(1)
    led2.value(1)
    led1.value(1)
    timedblink()