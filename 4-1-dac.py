import RPi.GPIO as GPIO
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT)
def demical2binary(value):
    return [int(element) for element in format(value, '08b')]
try:
    while True:
        user_input=input("Введите число от 0 до 255")
        if user_input.lower() == 'q':
            break
        try:
            value=int(user_input) 
            if value<0:
                print("Введите неотрицательное число")
                continue
            if value>255:
                print("Введите число не больше 255")
                continue
            binary_list=demical2binary(value)
            GPIO.output(dac, binary_list)
            voltage=(value*3.3)/256
            print(f"Предполагаемое напряжение на выходе ЦАП: {voltage:.2f} В")
        except ValueError:
            print("Ошибка, введите числовое значение")
        except Exception as e:
            print(f"Произошла ошибка:{e}")
finally:
    GPIO.output(dac, [0]*len(dac))
    GPIO.cleanup()