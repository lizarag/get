import RPi.GPIO as GPIO
pwm_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, 1000)
pwm.start(0)    
try:
    while True:
        duty_cycle = input("Введите коэффициент заполнения (0-100): ")
        try:
            duty_cycle = float(duty_cycle)
            if 0 <= duty_cycle <= 100:
                pwm.ChangeDutyCycle(duty_cycle)
                voltage = (duty_cycle / 100) * 3.3 
                print(f"Предполагаемое значение напряжения: {voltage:.2f} V")
            else:
                print("Ошибка: Коэффициент заполнения должен быть в диапазоне от 0 до 100")
        except ValueError:
            print("Ошибка: Пожалуйста, введите числовое значение")      
except KeyboardInterrupt:
    print("Программа остановлена пользователем")
finally:
    pwm.stop() 
    GPIO.cleanup()
    print("Настройки GPIO очищены")
