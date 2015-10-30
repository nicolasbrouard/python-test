#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# set to pull-up (normally closed position)
# Switch on GPIO18
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        print "button released: ", GPIO.input(18)
        GPIO.wait_for_edge(18, GPIO.FALLING)
        print "button pressed:  ", GPIO.input(18)
        GPIO.wait_for_edge(18, GPIO.RISING)

except KeyboardInterrupt:
    print "Cleanup GPIO"
    GPIO.cleanup()
