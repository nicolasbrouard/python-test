#!/usr/bin/python
import RPi.GPIO
import time

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(2, RPi.GPIO.OUT)
while True:
	RPi.GPIO.output(2, True)
	time.sleep(0.05)
	RPi.GPIO.output(2, False)
	time.sleep(0.05)

