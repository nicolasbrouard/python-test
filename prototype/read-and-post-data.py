#!/usr/bin/python3

import time
import urllib.parse
import logging

import httplib2

import RPi.GPIO as GPIO


# Configuration
API_KEY = "4VIY5BGG2YK2VUL2"
URL = "https://api.thingspeak.com/update"
SUCCESS_LED = 20
ERROR_LED = 21
LED_ON_DURATION_SECONDS = 0.5

POWER_VOLTS = 5.0
ROUNDED = 3

# Pins connected from the SPI port on the ADC to the Cobbler
SPI_CLK = 18
SPI_MISO = 23
SPI_MOSI = 24
SPI_CS = 25


# Light on success led for LED_ON_DURATION_SECONDS
def success_led():
    GPIO.output(SUCCESS_LED, True)
    time.sleep(LED_ON_DURATION_SECONDS)
    GPIO.output(SUCCESS_LED, False)


# Light on error led for LED_ON_DURATION_SECONDS
def error_led():
    for num in range(1, 3):
        GPIO.output(ERROR_LED, True)
        time.sleep(LED_ON_DURATION_SECONDS)
        GPIO.output(ERROR_LED, False)
        time.sleep(LED_ON_DURATION_SECONDS)


# On success, light on success led and log
def on_success():
    logging.info('Success')
    success_led()


# On error, light on error led and log
def on_error(error, content):
    logging.error('Error %s %s', content, error)
    error_led()


# Read all MCP3008 input PINs
def read_mcp3008():
    logging.info('Reading inputs on MCP3008')

    temp = read_adc(0, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
    logging.debug('Temp (CH0): %s', temp)
    temp_volts = convert_volts(temp, ROUNDED)
    logging.info('Temp (CH0): %s Volts', temp_volts)
    temp_celcius = convert_temp(temp_volts, ROUNDED)
    logging.info('Temp (CH0): %s°C', temp_celcius)

    resistor = read_adc(1, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
    logging.debug('Resistor 10 K-ohms on 3.3V (CH1): %s', resistor)
    resistor_volts = convert_volts(resistor, ROUNDED)
    logging.info('Resistor 10 K-ohms on 3.3V (CH1): %s Volts', resistor_volts)

    ground = read_adc(2, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
    logging.debug('Ground (CH2): %s', ground)
    ground_volts = convert_volts(ground, ROUNDED)
    logging.info('Ground (CH2): %s Volts', ground_volts)

    mid = read_adc(3, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
    logging.debug('3.3 Volts (CH3): %s', mid)
    mid_volts = convert_volts(mid, ROUNDED)
    logging.info('3.3 Volts (CH3): %s Volts', mid_volts)

    high = read_adc(4, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
    logging.debug('5.0 Volts (CH4): %s', high)
    high_volts = convert_volts(high, ROUNDED)
    logging.info('5.0 Volts (CH4): %s Volts', high_volts)

    pressure = read_adc(7, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
    logging.debug('Pressure (CH7): %s', pressure)
    pressure_volts = convert_volts(pressure, ROUNDED)
    logging.info('Pressure (CH7): %s Volts', pressure_volts)
    pressure_psi = convert_pressure(pressure_volts, ROUNDED)
    logging.info('Pressure (CH7): %s PSI', pressure_psi)

    return [temp_volts, temp_celcius, resistor_volts, ground_volts, mid_volts, high_volts, pressure_volts, pressure_psi]


# Post data on the Thingspeak channel
def thingspeak_post(values):
    body = urllib.parse.urlencode({'api_key': API_KEY,
                                   'field1': values[0],
                                   'field2': values[1],
                                   'field3': values[2],
                                   'field4': values[3],
                                   'field5': values[4],
                                   'field6': values[5],
                                   'field7': values[6],
                                   'field8': values[7]
                                   })
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    logging.info('Post %s to %s with api key %s', body, URL, API_KEY)
    response, content = httplib2.Http().request(URL, "POST", body, headers)
    if content == b'0':
        on_error(response, content)
    else:
        on_success()


# read SPI data from MCP3008 chip, 8 possible channels (0 thru 7)
def read_adc(channel, clock_pin, mosi_pin, miso_pin, cs_pin):
    if (channel > 7) or (channel < 0):
        return -1
    GPIO.output(cs_pin, True)

    GPIO.output(clock_pin, False)  # start clock low
    GPIO.output(cs_pin, False)  # bring CS low

    command_out = channel
    command_out |= 0x18  # start bit + single-ended bit
    command_out <<= 3  # we only need to send 5 bits here
    for i in range(5):
        if command_out & 0x80:
            GPIO.output(mosi_pin, True)
        else:
            GPIO.output(mosi_pin, False)
        command_out <<= 1
        GPIO.output(clock_pin, True)
        GPIO.output(clock_pin, False)

    adc_out = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clock_pin, True)
        GPIO.output(clock_pin, False)
        adc_out <<= 1
        if GPIO.input(miso_pin):
            adc_out |= 0x1

    GPIO.output(cs_pin, True)

    adc_out >>= 1  # first bit is 'null' so drop it
    return adc_out


# Convert ADC value to voltage level rounded to specified number of decimal places.
def convert_volts(value, places):
    volts = (value * POWER_VOLTS) / float(1023)
    volts = round(volts, places)
    return volts


# Calculate temperature from TMP36 data, rounded to specified number of decimal places.
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


def convert_pressure(volts, places):
    # TODO convert pressure
    return round(volts, places)


try:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        handlers=[
                            # logging.FileHandler("example1.log"),
                            logging.StreamHandler()
                        ])

    logging.info('Start read-and-post-data.py')

    # setup GPIO using Broadcom SOC channel numbering
    logging.debug('Setup GPIO in mode BCM')
    GPIO.setmode(GPIO.BCM)

    logging.debug('Setup pin %i in OUT', SUCCESS_LED)
    GPIO.setup(SUCCESS_LED, GPIO.OUT)
    logging.debug('Setup pin %i in OUT', ERROR_LED)
    GPIO.setup(ERROR_LED, GPIO.OUT)

    # set up the SPI interface pins
    logging.debug('Setup SPI pins')
    GPIO.setup(SPI_MOSI, GPIO.OUT)
    GPIO.setup(SPI_MISO, GPIO.IN)
    GPIO.setup(SPI_CLK, GPIO.OUT)
    GPIO.setup(SPI_CS, GPIO.OUT)

    data = read_mcp3008()
    thingspeak_post(data)

    # cleanup GPIO
    logging.debug('Cleanup GPIO')
    GPIO.cleanup()
except KeyboardInterrupt:
    logging.debug('Ctrl+C detected, cleanup GPIO')
    GPIO.cleanup()  # cleanup GPIO on CTRL+C
