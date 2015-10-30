#!/usr/bin/python
import RPi.GPIO as GPIO
from datetime import datetime

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# set to pull-up (normally closed position)
# Switch on GPIO18
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on GPIO17
GPIO.setup(17, GPIO.OUT)

startTime = datetime.now()
pressedTime = startTime
loop = True
average = 0
pressedCount = 0

# setup an indefinite loop that looks for the GPIO 2
while loop:

    # door open detected
    GPIO.wait_for_edge(18, GPIO.RISING)
    print("Button pushed!\n")
    GPIO.output(17, True)
    previousPressedTime = pressedTime
    pressedTime = datetime.now()
    interval = (pressedTime - previousPressedTime).microseconds
    print "Instant interval: " + interval + " ms"
    pressedCount += 1
    averageInterval = (pressedTime - startTime).microseconds / pressedCount
    print "Average interval: " + averageInterval + " ms"
    print "Average frequency: " + 1000 / averageInterval + " ms"
    if interval < 500:
        loop = False

    # door closed detected
    GPIO.wait_for_edge(18, GPIO.FALLING)
    print("Button released!\n")
    GPIO.output(17, False)
    releaseTime = datetime.now()

    print "Button pressed for " + (releaseTime - pressedTime).microseconds + " ms"

# cleanup
GPIO.cleanup()
