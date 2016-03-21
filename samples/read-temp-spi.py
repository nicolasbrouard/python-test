#!/usr/bin/env python2.7

# Ne fonctionne pas

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def read_channel(channel):
    adc = spi.xfer([1, (8 + channel) << 4, 0])
    print adc
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def convert_volts(data, places):
    volts = (data * 5.0) / float(1023)
    volts = round(volts, places)
    return volts


# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def convert_temp(data, places):
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

    temp = ((data * 330) / float(1023)) - 50
    temp = round(temp, places)
    return temp


# Define sensor channels
temp_channel = 0

# Define delay between readings
delay = 2

while True:
    # Read the temperature sensor data
    temp_level = read_channel(temp_channel)
    temp_volts = convert_volts(temp_level, 2)
    temp = convert_temp(temp_level, 2)

    # Print out results
    print "--------------------------------------------"
    print("Temp : {} ({}V) {} deg C".format(temp_level, temp_volts, temp))

    # Wait before repeating loop
    time.sleep(delay)
