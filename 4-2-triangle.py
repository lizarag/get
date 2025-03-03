import RPi.GPIO as GPIO
import time
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(value):
    return [int(bit) for bit in format(value, '08b')]
try:
    period = float(input("Введите период треугольного сигнала (в секундах): ")) 
    if period <= 0:
        raise ValueError("Период должен быть положительным числом.")
    rel_time = period / 256 

    while True:
        for value in range(256):
            GPIO.output(dac, dec2bin(value))
            time.sleep(rel_time)
        for value in range(255, -1, -1):
            GPIO.output(dac, dec2bin(value))
            time.sleep(rel_time)
finally:
    GPIO.output(dac, [0] * len(dac))
    GPIO.cleanup()