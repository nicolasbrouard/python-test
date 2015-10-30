#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# cleanup
GPIO.cleanup()

# setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)

count = 0
while count < 9:
    GPIO.output(17, True)
    time.sleep(0.5)
    GPIO.output(17, False)
    time.sleep(0.5)
    count += 1

# cleanup
GPIO.cleanup()
