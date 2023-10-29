# This task is divided into two parts that can be completed separately and then integrated into a complete solution.

# Part 1. Implement a program that uses Piotimer and ADC to sample PPG signal at
# 250Hz frequency and passes the sampled data to the main program. In the first
# phase main program can just print each sample so that you can, for example with the
# data with Thonny’s plotter view.

# Part 2. Implement an algorithm that finds the heart rate from sampled PPG signal.

from piotimer import Piotimer as Timer # hardware
# from machine import Timer #software
from ssd1306 import SSD1306_I2C
from machine import Pin, ADC, I2C, PWM
from fifo import Fifo
import utime
import array


##########################
#   GPIO and frequency   #
##########################

# ADC-converter
adc = ADC(26)

# OLED
i2c = I2C(1, scl = Pin(15), sda = Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Sample Rate, Buffer
samplerate = 250
samples = Fifo(samplerate / 5)


#################
#   Functions   #
#################

# Reading data from sensor
def read_adc(tid):
    x = adc.read_u16()
    samples.put(x)
    
tmr = Timer(freq = samplerate, callback = read_adc)

# Mean PPI Calculator
def meanPPI_calculator(data):
    sumPPI = 0
    for i in data:
        sumPPI += i
    meanPPI = sumPPI/len(data)
    print('Mean PPI value:', int(meanPPI), 'ms')
    return meanPPI

# Mean HR Calculator
def meanHR_calculator(meanPPI):
    HR = 60000/meanPPI
    rounded_HR = round(HR, 0)
    print('Mean HR value:', int(rounded_HR), 'bpm')
    return int(rounded_HR)

# SDNN Calculator
def SDNN_calculator(data, PPI):
    summary = 0
    for i in data:
        summary += (i-PPI)**2
    SDNN = (summary/(len(data)-1))**(1/2)
    rounded_SDNN = round(SDNN, 0)
    print('SDNN value:', int(rounded_SDNN), 'ms')
    return int(rounded_SDNN)

# RMSSD Calculator
def RMSSD_calculator(data):
    i = 0
    summary = 0
    while i < len(data)-1:
        summary += (data[i+1]-data[i])**2
        i +=1
    RMSSD = (summary/(len(data)-1))**(1/2)
    rounded_RMSSD = round(RMSSD, 0)
    print('RMSSD value:', int(rounded_RMSSD), 'ms')
    return int(rounded_RMSSD)

# SDSD Calculator
def SDSD_calculator(data):
    i = 0
    k = 0
    PP_array = array.array('I')
    first_value = 0
    second_value = 0
    while i < len(data)-1:
        PP_array.append(int(data[i+1]-data[i]))
        i += 1
    while k < len(PP_array)-1:
        first_value += (PP_array[k]**2)
        second_value += PP_array[k]
        k += 1 
    first = first_value/(len(PP_array)-1)
    second = (second_value/(len(PP_array)))**2
    SDSD = (first - second)**(1/2)
    rounded_SDSD = round(SDSD, 0)
    print('SDSD value:', int(rounded_SDSD))
    return int(rounded_SDSD)

# SDSD_float Calculator
def SDSD_float_calculator(data):
    i = 0
    PP_array = array.array('l')
    first_value = 0
    second_value = 0
    while i < len(data)-1:
        PP_array.append(int(data[i+1])-int(data[i]))
        i += 1
    i = 0
    while i < len(PP_array)-1:
        first_value += float(PP_array[i]**2)
        second_value += float(PP_array[i])
        i += 1
    first = first_value/(len(PP_array)-1)
    second = (second_value/(len(PP_array)))**2
    SDSD = (first - second)**(1/2)
    rounded_SDSD = round(SDSD, 0)
    print('SDSD value:', int(rounded_SDSD))
    return int(rounded_SDSD)

# SD1 Calculator        
def SD1_calculator(SDSD):
    SD1 = ((SDSD**2)/2)**(1/2)
    rounded_SD1 = round(SD1, 0)
    print('SD1 value:', int(rounded_SD1))
    return int(rounded_SD1)

# SD2 Calculator
def SD2_calculator(SDNN, SDSD):
    SD2 = ((2*(SDNN**2))-((SDSD**2)/2))**(1/2)
    rounded_SD2 = round(SD2, 0)
    print('SD2 value:', int(rounded_SD2))
    return int(rounded_SD2)


###########################
#   Plotting the signal   #
###########################

x1 = -1
y1 = 32
m0 = 65535 / 2 # moving average
a = 1/10 # weight for adding new data to moving average

disp_div = samplerate / 25
disp_count = 0
buffer = array.array('H')
capture_length = samplerate * 60 # length of capture, ie. * 180 = 3 min

while len(buffer) < capture_length:
    if not samples.empty():
        x = samples.get()
        buffer.append(x)
        disp_count += 1
        
        if disp_count >= disp_div:
            disp_count = 0
            m0 = (1-a)*m0 + a*x # Calculate moving average
            y2 = int(32*(m0-x)/10000 + 32) # Scale the value to fit into OLED
            #y2 = int(64-(x/65535)*64) # Alternative scaling without moving average
            y2 = max(0, min(64, y2)) # Limit the values between 0..64
            x2 = x1 + 1
            oled.line(x2, 0, x2, 64, 0) # Clean up one line
            oled.line(x1, y1, x2, y2, 1) # Draw the new line
            oled.show()
            x1 = x2
            if x1 > 127:
                x1 = -1
            y1 = y2
            #print(x)

tmr.deinit()


################################
#   Sampling, Peak Detection   #
################################

index = 0
avg_size = int(samplerate * 0.5)
sample_sum = 0

while(index < avg_size):
    sample_sum = sample_sum + buffer[index]
    index += 1
    
min_bpm = 30
max_bpm = 200
sample_peak = 0
sample_index = 0
previous_peak = 0
previous_index = 0
PPI_array = array.array('I')

while(index < len(buffer)):
    sample_avg = sample_sum / avg_size
    sample_val = buffer[index]

    if sample_val > sample_avg * 1.05:
        if sample_val > sample_peak:
            sample_peak = sample_val
            sample_index = index
            
    else:
        if sample_peak > 0:
            if (sample_index - previous_index) > (60 * samplerate / min_bpm):
                previous_peak = 0
                previous_index = 0
            else:
                if sample_peak >= (0.8 * previous_peak):
                    if (sample_index - previous_index) > (60 * samplerate / max_bpm):
                        if previous_peak > 0:
                            interval = sample_index - previous_index
                            interval_ms = int(interval * 1000 / samplerate)
                            PPI_array.append(interval_ms)
                            #print("BPM: " + str((samplerate / interval) * 60))
                        previous_peak = sample_peak
                        previous_index = sample_index
                #print("Sample " + str(sample_index) + " peak: " + str(sample_peak))
        sample_peak = 0

    sample_sum = sample_sum + buffer[index] - buffer[index-avg_size]
    index += 1
    
    
#################################################
#   Mean PPI, Mean HR, SSDN, RMSSD Calculator   #
#################################################

print(PPI_array)
mean_PPI = meanPPI_calculator(PPI_array)
mean_HR = meanHR_calculator(mean_PPI)
SDNN = SDNN_calculator(PPI_array, mean_PPI)
RMSSD = RMSSD_calculator(PPI_array)
SDSD = SDSD_float_calculator(PPI_array)
SD1 = SD1_calculator(SDSD)
SD2 = SD2_calculator(SDNN, SDSD)
    
oled.fill(0)
oled.text('MeanPPI:'+ str(int(mean_PPI)) +'ms', 0, 0, 1)
oled.text('MeanHR:'+ str(int(mean_HR)) +'bpm', 0, 10, 1)
oled.text('SDNN:'+str(int(SDNN)) +'ms', 0, 20, 1)
oled.text('RMSSD:'+str(int(RMSSD)) +'ms', 0, 30, 1)
oled.text('SD1:'+str(int(SD1)), 0, 40, 1)
oled.text('SD2:'+str(int(SD2)), 0, 50, 1)
oled.show()
