# Write a code that calculates the basic HRV analysis parameters and shows the values on the OLED: 
# ▪ Mean PPI
# ▪ mean heart rate (HR)
# ▪ Standard deviation of PPI (SDNN)
# ▪ Root mean square of successive differences (RMSSD)

import array
import ssd1306
from machine import Pin, I2C
from utime import sleep_ms

# OLED
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Rotary encoder button
button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)

# Testdata
test_set2 = array.array('I', [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812,
812, 756, 820, 812, 800])

def meanPPI_calculator(data):
    sumPPI = 0
    for i in data:
        sumPPI += i
    meanPPI = sumPPI/len(data)
    print('Mean PPI value:', int(meanPPI), 'ms')
    return meanPPI

def meanHR_calculator(meanPPI):
    HR = 60000/meanPPI
    rounded_HR = round(HR, 0)
    print('Mean HR value:', int(rounded_HR), 'bpm')
    return rounded_HR

def SDNN_calculator(data, PPI):
    summary = 0
    for i in data:
        summary += (i-PPI)**2
    SDNN = (summary/(len(data)-1))**(1/2)
    rounded_SDNN = round(SDNN, 0)
    print('SDNN value:', int(rounded_SDNN), 'ms')
    return rounded_SDNN

def RMSSD_calculator(data):
    i = 0
    summary = 0
    while i < len(data)-1:
        summary += (data[i+1]-data[i])**2
        i +=1
    RMSSD = (summary/(len(data)-1))**(1/2)
    rounded_RMSSD = round(RMSSD, 0)
    print('RMSSD value:', int(rounded_RMSSD), 'ms')
    return rounded_RMSSD
        
PPI2 = meanPPI_calculator(test_set2)
HR2 = meanHR_calculator(PPI2)
SSDN2 = SDNN_calculator(test_set2, PPI2)
RMSSD2 = RMSSD_calculator(test_set2)
    
oled.text('MeanPPI:'+ str(int(PPI2)) +'ms', 0, 0, 1)
oled.text('MeanHR:'+ str(int(HR2)) +'bpm', 0, 10, 1)
oled.text('SDNN:'+str(int(SSDN2)) +'ms', 0, 20, 1)
oled.text('RMSSD:'+str(int(RMSSD2)) +'ms', 0, 30, 1)
oled.show()

while True:
    if button.value() == 0:
        oled.fill(0)
        oled.show()
