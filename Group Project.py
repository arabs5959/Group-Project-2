import time
from machine import Pin, time_pulse_us, PWM, ADC, I2C


# I2C signal pins
I2C_SDA = 14
I2C_SCL = 15

# ADS 1015 configuration information
ADS1015_ADDR = 0x48
ADS1015_PWM = 2     # port 2 has (low-pass filtered) PWM signal

# You will need to upload the file ads1x15.py to the pico for the following code to work properly
from ads1x15 import ADS1015

i2c = I2C(1, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL))
adc = ADS1015(i2c, ADS1015_ADDR, 1)

# scan i2c bus to get a listing of all I2C devices... including the ADC that has the servo feedback values
addresses = i2c.scan()
for address in addresses:
	print(hex(address))

#Set up PWM Pins:
PWM_OUT_PIN = 16  # 
PWM_IN_PIN  = 17  # 
# Read filtered PWM input from the header
value = adc.read(0, ADS1015_PWM)
print(value)
pwm = PWM(Pin(PWM_IN_PIN))
pwm.freq(1000)  # Set the frequency to 1 kHz
pwm.duty_u16(32768)  # Set the duty cycle to 50% (32768 out of 65535)
# Configure your input GPIO pin (e.g., GP14 on Raspberry Pi Pico)

def read_pwm_siganl(pin, timeout=5000):
    high_time = time_pulse_us(pin, 1, timeout)

    low_time = time_pulse_us(pin, 0, timeout)

    total_period = high_time + low_time
    frequency = 1000000 / total_period

    duty_cycle = (high_time / total_period) * 100
    
    return frequency, duty_cycle, high_time, low_time
print("\nStarting readings... Press Ctrl+C to stop.") #Line 46-59 were written by ai
try:
    while True:
        # Read the filtered analog voltage from the ADS1015
        analog_val = adc.read(0, ADS1015_PWM)
        
        # Read the raw digital PWM timing from Pin 17
        freq, duty, high, low = read_pwm_signal(pwm_in_pin)
        
        print(f"ADS1015 Analog Value: {analog_val}")
        print(f"Measured PWM -> Freq: {freq:.1f}Hz, Duty: {duty:.1f}%, High: {high}us, Low: {low}us")
        print("-" * 50)
        
        time.sleep(1)