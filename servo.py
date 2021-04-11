import RPi.GPIO as GPIO
import time

servo_1_pin = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_1_pin, GPIO.OUT)

p = GPIO.PWM(servo_1_pin, 400)


pos = 1

p.start(pos)
time.sleep(2)

for pos in range(0, 100, 10):
    p.start(pos)
    time.sleep(0.5)

    print(pos)


time.sleep(2)
p.stop()

GPIO.cleanup()
