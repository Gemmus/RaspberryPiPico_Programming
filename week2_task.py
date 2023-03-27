import ssd1306
from machine import Pin, I2C
from utime import sleep_ms

led1 = Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(22, Pin.OUT)

button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
button1 = Pin(9, mode = Pin.IN, pull = Pin.PULL_UP)
button2 = Pin(8, mode = Pin.IN, pull = Pin.PULL_UP)
button3 = Pin(7, mode = Pin.IN, pull = Pin.PULL_UP)

i2c = I2C(1, sda=Pin(14), scl=Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        
def button_handler(pin):
    if pin.value() == 0:
        led1.value(0)
        led2.value(0)
        led3.value(0)
        
button.irq(handler = button_handler, trigger = button.IRQ_FALLING)

btn1_state = button1.value()
btn2_state = button2.value()
btn3_state = button3.value()

while True:
    sleep_ms(10)
    btn1_new_state = button1.value()
    btn2_new_state = button2.value()
    btn3_new_state = button3.value()
    
    if btn1_state != btn1_new_state:
        count1 += 1
        if count1 > 5:
            btn1_state = btn1_new_state
            count1 = 0
            if btn1_new_state == 0:
                led1.toggle()
                oled.text('LED1 ON', 0, 0, 1)
                oled.show()
    else:
        count1 = 0
        
    if btn2_state != btn2_new_state:
        count2 += 1
        if count2 > 5:
            btn2_state = btn2_new_state
            count2 = 0
            if btn2_new_state == 0:
                led2.toggle()
                oled.text('LED2 ON', 0, 15, 1)
                oled.show()
    else:
        count2 = 0
        
    if btn3_state != btn3_new_state:
        count3 += 1
        if count3 > 5:
            btn3_state = btn3_new_state
            count3 = 0
            if btn3_new_state == 0:
                led3.toggle()
                oled.text('LED3 ON', 0, 30, 1)
                oled.show()
    else:
        count3 = 0
        
    if button.value() == 0:
        oled.fill(0)
        oled.show()
