import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [17, 27, 22, 5, 6, 13, 19, 26]
comp = 14
troyka = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

start_time = time.time()
voltages = []
maxVoltage = 3.3

def decimal2binary(value):
    return [int(element) for element in format(value, '08b')]

def adc():
    for value in range(256):
        signal = decimal2binary(value)
        GPIO.output(dac, signal)  # Установка значения на ЦАП
        time.sleep(0.01)  # Задержка для стабилизации сигнала
        compValue = GPIO.input(comp)
        if compValue == 0:
            voltage = value / 255 * maxVoltage
            return voltage


try:
    # Заряд конденсатора
    GPIO.output(troyka, GPIO.HIGH)
    while True:
        voltage = adc()  # Получаем напряжение от АЦП
        voltages.append(voltage)  # Добавляем напряжение в список
        if voltage >= 0.97 * maxVoltage:  # Если достигнуто 97% от входного напряжения
            break

    # Разряд конденсатора
    GPIO.output(troyka, GPIO.LOW)
    while True:
        voltage = adc()  # Получаем напряжение от АЦП
        voltages.append(voltage)  # Добавляем напряжение в список
        if voltage <= 0.02 * maxVoltage:  # Если достигнуто 2% от входного напряжения
            break

finally:
    end_time = time.time()
    duration = end_time - start_time

    # Вывод результатов
    print(f"Общая продолжительность эксперимента: {duration:.2f} секунд")

    if len(voltages) > 1:
        period = duration / len(voltages)
        rate = 1 / period
        step = (3.3 / (2 ** 8))

        print(f"Период одного измерения: {period:.4f} секунд")
        print(f"Средняя частота дискретизации: {rate:.2f} Гц")
        print(f"Шаг квантования АЦП: {step:.4f} В")

        # Сохранение данных в файлы
        with open('data.txt', 'w') as data_file:
            for voltage in voltages:
                data_file.write(f"{voltage:.4f}\n")

        with open('settings.txt', 'w') as settings_file:
            settings_file.write(f"Средняя частота дискретизации: {rate:.2f} Гц\n")
            settings_file.write(f"Шаг квантования АЦП: {step:.4f} В\n")

        # Построение графика
        plt.plot(range(len(voltages)), voltages)
        plt.xlabel('Номер измерения')
        plt.ylabel('Напряжение (В)')
        plt.title('Зависимость показаний АЦП от номера измерения')
        plt.show()

    GPIO.cleanup()
