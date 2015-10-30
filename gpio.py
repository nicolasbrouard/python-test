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
lightOn = True

# setup an indefinite loop that looks for the GPIO 2
while loop:

    # door open detected
    GPIO.wait_for_edge(18, GPIO.RISING)

    # Blink DEL on each button pressed
    GPIO.output(17, not lightOn)
    lightOn = not lightOn

    # Calculate timing
    previousPressedTime = pressedTime
    pressedTime = datetime.now()
    interval = (pressedTime - previousPressedTime).microseconds / 1000
    print "Instant interval: ", interval, " ms"
    pressedCount += 1
    averageInterval = (pressedTime - startTime).microseconds / pressedCount / 1000
    print "Average interval: ", averageInterval, " ms"
    print "Average frequency: ", 1000.0 / averageInterval, " Hz"
    print "Average rpm: ", 1000.0 / averageInterval * 60.0, " rpm"

    # Exit condition
    if interval < 200:
        loop = False

GPIO.output(17, False)

# cleanup
GPIO.cleanup()
