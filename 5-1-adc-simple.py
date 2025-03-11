import RPi.GPIO as GPIO
import time
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)


def decimal2binary(value):
    return [int(element) for element in format(value, '08b')]

def adc():
    for value in range(256):
        binary_value = decimal2binary(value)    
        GPIO.output(dac, binary_value)
        time.sleep(0.01)
        if GPIO.input(comp):
            return value

try:
    while True:
        digital_value = adc()
        voltage = (digital_value / 255) * 3.3
        print(
            f"Цифровое значение: {digital_value}, Напряжение: {voltage:.2f} В")
finally:
    GPIO.output(dac, [0]*len(dac))
    GPIO.cleanup()
