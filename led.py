#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
while True:
	GPIO.output(17, True)
	time.sleep(0.5)
	GPIO.output(17, False)
	time.sleep(0.5)

