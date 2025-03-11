import RPi.GPIO as GPIO
import time
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=0)
GPIO.setup(comp, GPIO.IN)
def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc():
    value=0
    for i in range(7,-1,-1):
        value+=2**i
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        if GPIO.input(comp) == 0:
            value-=2**i
    return value
try:
    while True:
        digital_value = adc()
        voltage = (digital_value / 256) * 3.3
        print(f"Цифровое значение: {digital_value}, Напряжение: {voltage:.2f} В")
        time.sleep(0.1)
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()