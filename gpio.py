#!/usr/bin/python
import RPi.GPIO as GPIO
from datetime import datetime


def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis


#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# set to pull-up (normally closed position)
# Switch on GPIO18
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on GPIO17
GPIO.setup(17, GPIO.OUT)

startTime = datetime.now()
pressedTime = startTime
print startTime
loop = True
average = 0
pressedCount = 0
lightOn = True

try:
    while loop:
        GPIO.wait_for_edge(18, GPIO.RISING)

        # Blink DEL on each button pressed
        GPIO.output(17, not lightOn)
        lightOn = not lightOn

        # Calculate timing
        previousPressedTime = pressedTime
        pressedTime = datetime.now()
        interval = millis_interval(previousPressedTime, pressedTime)
        print "previousPressedTime: ", previousPressedTime
        print "pressedTime: ", pressedTime
        print "Instant interval: ", interval, " us [", interval / 1000, " ms]"
        pressedCount += 1
        averageInterval = millis_interval(startTime, pressedTime) / pressedCount / 1000
        print "presseCount: ", pressedCount
        print "Average interval: ", averageInterval, " ms"
        print "Average frequency: ", 1000.0 / averageInterval, " Hz"
        print "Average rpm: ", 1000.0 / averageInterval * 60.0, " rpm"
except KeyboardInterrupt:
    GPIO.cleanup()
