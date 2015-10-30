#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# set to pull-up (normally closed position)
# Switch on GPIO18
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def my_callback(channel):
    print "falling edge detected on 18"


def my_callback2(channel):
    print "rising edge detected on 18"


# when a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(18, GPIO.FALLING, callback=my_callback, bouncetime=20)

# when a falling edge is detected on port 23, regardless of whatever
# else is happening in the program, the function my_callback2 will be run
# 'bouncetime=300' includes the bounce control written into interrupts2a.py
GPIO.add_event_detect(23, GPIO.RISING, callback=my_callback2, bouncetime=20)

try:
    time.sleep(100)

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit