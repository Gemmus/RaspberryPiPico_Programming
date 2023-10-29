#Write a code that turns the protoboard’s LEDs on and off in sequence. Switch the values every second.

from machine import Pin
import time

led3= Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led1 = Pin(22, Pin.OUT)

while True:
    led3.value(0)
    led2.value(0)
    led1.value(0)
    time.sleep(1)
       
    led3.value(0)
    led2.value(0)
    led1.value(1)
    time.sleep(1)
  
    led3.value(0)
    led2.value(1)
    led1.value(0)
    time.sleep(1)
      
    led3.value(1)
    led2.value(0)
    led1.value(0)
    time.sleep(1)


    
