#!/usr/bin/env python2.7
# coding=utf-8

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if (adcnum > 7) or (adcnum < 0):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)  # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3  # we only need to send 5 bits here
    for i in range(5):
        if commandout & 0x80:
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if GPIO.input(misopin):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1  # first bit is 'null' so drop it
    return adcout


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

power = 5.0
rounded = 3

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def convert_volts(data, places):
    volts = (data * power) / float(1023)
    volts = round(volts, places)
    return volts


# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def convert_temp(volt, places):
    # ADC Value
    # (approx)  Temp  Volts
    #    0      -50    0.00
    #   78      -25    0.25
    #  155        0    0.50
    #  233       25    0.75
    #  310       50    1.00
    #  465      100    1.50
    #  775      200    2.50
    # 1023      280    3.30

    temp = (volt * float(100)) - float(50)
    temp = round(temp, places)
    return temp


try:
    while True:
        temp = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        temp_volt = convert_volts(temp, rounded)
        print "temp volt:", temp, temp_volt
        print "temp °:", convert_temp(temp_volt, rounded)

        resistor = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print "resistor 300 ohms on 3.3V:", resistor, convert_volts(resistor, rounded)

        ground = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print "0 Volts:", ground, convert_volts(ground, rounded)

        mid = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print "3.3 Volts:", mid, convert_volts(mid, rounded)

        high = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print "5 Volts:", high, convert_volts(high, rounded)

        # hang out and do nothing for a half second
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()  # clean up GPIO on CTRL+C exit
