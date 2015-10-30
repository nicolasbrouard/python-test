#!/usr/bin/python
import RPi.GPIO as GPIO

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# set to pull-up (normally closed position)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# setup an indefinite loop that looks for the GPIO 2
while True:

    # door open detected
    GPIO.wait_for_edge(2, GPIO.RISING)
    print("Button pushed!\n")

    # door closed detected
    GPIO.wait_for_edge(2, GPIO.FALLING)
    print("Button released!\n")

# cleanup
GPIO.cleanup()
