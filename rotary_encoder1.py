from machine import Pin
from utime import sleep_ms, time

RotA = Pin(10, Pin.IN)
RotB = Pin(11, Pin.IN)
Rot_Push = Pin(12, Pin.IN, Pin.PULL_UP)

def Rotary_turned(Pin):
    if RotB.value() == 0:
        print('Right/Clockwise')
    else:
        print('Left/Anti-clockwise')
        
def Rotary_pushed(Pin):
    print('Knob pushed')

RotA.irq(handler = Rotary_turned, trigger = Pin.IRQ_RISING)
Rot_Push.irq(handler = Rotary_pushed, trigger = Pin.IRQ_RISING)

while True:
    sleep_ms(100)