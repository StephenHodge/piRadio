#!/usr/bin/env python

#this should hopefully allow you to twist a potentiaomiter and play music

import RPi.GPIO as GPIO
import time
import subprocess
import os
import signal

GPIO.setmode(GPIO.BCM)

lastTrimPot = 0
currentChannel = ""
trimTollerance = 10

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
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
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 20
SPIMISO = 26
SPIMOSI = 19
SPICS = 16

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 6;


while True:

        # read the analog pin
        trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print trim_pot
        trimDifference = abs(trim_pot - lastTrimPot)

        if trimDifference >= trimTollerance:
            set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
            set_volume = round(set_volume)          # round out decimal value
            set_volume = int(set_volume)            # cast volume as integer
            set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
            os.system(set_vol_cmd)  # set volume

        lastTrimPot = trim_pot

        # #
        # # if ((trim_pot != lastTrimPot) & (trim_pot != (lastTrimPot - 1)) & (trim_pot != (lastTrimPot - 2)) & (trim_pot != (lastTrimPot + 1)) & (trim_pot != (lastTrimPot + 2))):
        # #     print "----"
        # #     print trim_pot
        # #
        # #
        # #     if ((trim_pot > 0) & (trim_pot < 512)) & (currentChannel != "Six Music"):
        # #         currentChannel = "Six Music"
        # #         print currentChannel
        # #         try:
        # #             os.killpg(process.pid, signal.SIGTERM)
        # #         except:
        # #             process = subprocess.Popen("./Radio6Music.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        # #
        # #     if ((trim_pot > 500) & (trim_pot < 1024)) & (currentChannel != "Radio One"):
        # #         currentChannel = "Radio One"
        # #         print currentChannel
        # #         try:
        # #             os.killpg(process.pid, signal.SIGTERM)
        # #         except:
        # #             process = subprocess.Popen("./Radio1.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        # #
        # #     # hang and do nothing for half a second
        # #
        # # lastTrimPot = trim_pot

        time.sleep(0.5)
