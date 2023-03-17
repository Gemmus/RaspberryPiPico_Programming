#task1
from machine import Pin
import time

led3= Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led1 = Pin(20, Pin.OUT)

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
    
    
#task2
from machine import Pin
import time

led_onboard = Pin("LED", Pin.OUT)
led1= Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(22, Pin.OUT)

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
    
    
#task3
from machine import Pin, PWM
import time

led_onboard = Pin("LED", Pin.OUT)

led20 = PWM(Pin(20))
led20.freq(1000)

led21 = PWM(Pin(21))
led21.freq(1000)

led22 = PWM(Pin(22))
led22.freq(1000)

def timedblink0():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    time.sleep(3)
    
def timedblink1():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    for duty in range(0,65535):
        led20.duty_u16(duty)
        time.sleep(0.0001)
        
    for duty in range(65535, 0, -1):
        led20.duty_u16(duty)
        time.sleep(0.0001)
       
def timedblink2():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    for duty in range(0,65535):
        led21.duty_u16(duty)
        time.sleep(0.0001)
        
    for duty in range(65535, 0, -1):
        led21.duty_u16(duty)
        time.sleep(0.0001)

def timedblink3():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    for duty in range(0,65535):
        led20.duty_u16(duty)
        led21.duty_u16(duty)
        time.sleep(0.0001)
        
    for duty in range(65535, 0, -1):
        led20.duty_u16(duty)
        led21.duty_u16(duty)
        time.sleep(0.0001)

def timedblink4():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    for duty in range(0,65535):
        led22.duty_u16(duty)
        time.sleep(0.0001)
        
    for duty in range(65535, 0, -1):
        led22.duty_u16(duty)
        time.sleep(0.0001)
    
def timedblink5():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    for duty in range(0,65535):
        led20.duty_u16(duty)
        led22.duty_u16(duty)
        time.sleep(0.0001)
        
    for duty in range(65535, 0, -1):
        led20.duty_u16(duty)
        led22.duty_u16(duty)
        time.sleep(0.0001)
    
def timedblink6():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    for duty in range(0,65535):
        led21.duty_u16(duty)
        led22.duty_u16(duty)
        time.sleep(0.0001)
        
    for duty in range(65535, 0, -1):
        led21.duty_u16(duty)
        led22.duty_u16(duty)
        time.sleep(0.0001)

def timedblink7():
    led_onboard.value(1)
    time.sleep(0.2)
    led_onboard.value(0)
    for duty in range(0,65535):
        led20.duty_u16(duty)
        led21.duty_u16(duty)
        led22.duty_u16(duty)
        time.sleep(0.0001)
        
    for duty in range(65535, 0, -1):
        led20.duty_u16(duty)
        led21.duty_u16(duty)
        led22.duty_u16(duty)
        time.sleep(0.0001)

while True:
    timedblink0()
    timedblink1()
    timedblink2()
    timedblink3()
    timedblink4()
    timedblink5()
    timedblink6()
    timedblink7()