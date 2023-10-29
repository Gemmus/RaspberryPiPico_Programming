# Write a program that implements a menu system to control LED brightness. 
# The menu has two modes: LED selection and brightness control. 
# User toggles between the modes by pressing the encoder button.

# When the program is in LED selection mode turning the encoder switches between LEDs. 
# The selected LED is displayed on the screen.

# When user presses the button program enters brightness control mode where turning the encoder adjusts the brightness of the selected LED.

# The current brightness is displayed on the screen as both percentage (0 – 100%) and a horizontal bar.

# Turning the knob immediately increases or decreases the brightness of the LED andupdates the display.

# When user presses the button to switch back to LED selection mode the current brightness will remain on the LED. 
# Adjusting one LEDs brightness may not affect the other LEDs.

import ssd1306
from machine import Pin, I2C, PWM, ADC
import utime

###############
#  GPIO Pins  #
###############

# Rotary Encoder
rot_push = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
rota = Pin(10, mode = Pin.IN, pull = Pin.PULL_UP)
rotb = Pin(11, mode = Pin.IN, pull = Pin.PULL_UP)

# LEDs
led = [20, 21, 22]
list_of_led = []
for x in range(0,3):
#    list_of_led.append(Pin(led[x], Pin.OUT))
    list_of_led.append(PWM(Pin(led[x])))
    list_of_led[x].freq(1000)

# OLED
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

###############
#  VARIABLES  #
###############

# Menu selection variables and switch filtering
mode = 0
count = 0
switch_state = 0

# Variables for LEDs selection
value = 0
previous_value = 1

# Variables for Brightness
brightness = [20000,20000,20000]
previous_state = [1,1,1]

###############
#  FUNCTIONS  #
###############

# LED selection
def led_changed():
    global previous_value
    global value
    global brightness
    
    if previous_value != rota.value():
        if rota.value() == 0:
            if rotb.value() == 0:
                value = (value - 1)%3
                print('anti-clockwise', value+1, brightness[value])
            else:
                value = (value + 1)%3
                print('clockwise', value+1, brightness[value])
        previous_value = rota.value()

# OLED displays LED number
def oled_on():
    oled.fill(0)
    if value == 0:
        oled.text('LED1', 0, 0, 1)
        oled.text('LED2', 0, 10, 0)
        oled.text('LED3', 0, 20, 0)
    if value == 1:
        oled.text('LED1', 0, 0, 0)
        oled.text('LED2', 0, 10, 1)
        oled.text('LED3', 0, 20, 0)
    if value == 2:
        oled.text('LED1', 0, 0, 0)
        oled.text('LED2', 0, 10, 0)
        oled.text('LED3', 0, 20, 1)
    oled.show()
    
# Brightness selection
def brightness_changed():
    global previous_brightness
    global brightness
    global value
    
    if previous_state[value] != rota.value():
        if rota.value() == 0:
            if rotb.value() == 0:
                if brightness[value] > 0:
                    brightness[value] = (brightness[value] - 2000)
                print("anti-clockwise", brightness[value])
            else:
                if brightness[value] < 40000:
                    brightness[value] = (brightness[value] + 2000)
                print("clockwise", brightness[value])
        previous_state[value] = rota.value()
    
# OLED displys brightness level
def oled_display():
    oled.fill(0)
    if value == 0:
        oled.text('LED1', 0, 0, 1)
        oled.text('LED2', 0, 10, 0)
        oled.text('LED3', 0, 20, 0)
    if value == 1:
        oled.text('LED1', 0, 0, 0)
        oled.text('LED2', 0, 10, 1)
        oled.text('LED3', 0, 20, 0)
    if value == 2:
        oled.text('LED1', 0, 0, 0)
        oled.text('LED2', 0, 10, 0)
        oled.text('LED3', 0, 20, 1)
    procentage = int(brightness[value]/400)
    oled.text('Brightness: ' + str(procentage) + '%', 0, 36, 1)
    oled.rect(15, 50, 101, 10, 1)
    oled.fill_rect(15, 50, procentage, 10, 1)
    oled.show()
    
    
####################
#  MAIN PROGRAMME  #
####################

while True:
    # Filtering the Rotary Push button and enable selection of mode
    new_state = rot_push.value()
    if new_state != switch_state:
        count += 1
        if count > 3:
            if new_state == 0:
                if mode == 0:
                    mode = 1
                else:
                    mode = 0
            switch_state = new_state
            count = 0
    else:
        count = 0
    utime.sleep(0.01)
    
    # Functions of the modes
    oled_display()
    if mode == 0:
#        oled_on
        for i in range(0,3):
            list_of_led[i].duty_u16(0)
            led_changed()
            list_of_led[value].duty_u16(brightness[value])
                        
    else:
        new_brightness = brightness_changed()
        list_of_led[value].duty_u16(brightness[value])
#        oled_display()
