#!/usr/bin/env python

#this should hopefully allow you to twist a potentiaomiter and play music
import RPi.GPIO as GPIO
import time
import subprocess
import os
import signal

#variables for LED GPIO
LED_PIN = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

#variables for chipset thingy
DEBUG = 1
lastTrimPot_tune = 0
lastTrimPot_vol = 0
currentChannel = ""
trimTollerance = 10
waveBand = ""
trim_pot_vol = 0
trim_pot_tune = 0


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
potentiometer_tune = 7
potentiometer_vol = 6

#setups for the buttons
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def ledMode(Mode):
    GPIO.output(LED_PIN, Mode)

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

def playStation(trim_pot_tune):

    trimDifference_tune = abs(trim_pot_tune - lastTrimPot_tune)

    if trimDifference_tune >= trimTollerance:

        if waveBand == "BBC":

            if ((trim_pot_tune >= 0) & (trim_pot_tune < 170)) & (currentChannel != "Radio_One"):
                currentChannel = "Radio One"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/BBC1.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 170) & (trim_pot_tune < 340)) & (currentChannel != "Radio_Two"):
                currentChannel = "Radio Two"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/BBC2.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 340) & (trim_pot_tune < 510)) & (currentChannel != "Radio_Three"):
                currentChannel = "Radio Three"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/BBC3.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 510) & (trim_pot_tune < 680)) & (currentChannel != "Radio_Four"):
                currentChannel = "Radio Four"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/BBC4.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 680) & (trim_pot_tune <= 850)) & (currentChannel != "Radio_Five"):
                currentChannel = "Radio Five"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/BBC5Live.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 850) & (trim_pot_tune < 1024)) & (currentChannel != "Six_Music"):
                currentChannel = "Six Music"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/BBC6Music.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        if waveBand == "Secular":

            if ((trim_pot_tune >= 0) & (trim_pot_tune < 341) & (currentChannel != "Radio_Devon")):
                currentChannel = "Radio_Devon"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/BBCRadioDevon.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 341) & (trim_pot_tune < 682) & (currentChannel != "ClassicFM")):
                currentChannel = "ClassicFM"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/ClassicFM.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 341) & (trim_pot_tune < 682) & (currentChannel != "RadioNorthDevon")):
                currentChannel = "RadioNorthDevon"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/RadioNorthDevon.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        if waveBand == "Christian":

            if ((trim_pot_tune >= 0) & (trim_pot_tune < 256) & (currentChannel != "CrossRhythms2")):
                currentChannel = "CrossRhythms2"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/CrossRhythms2.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 256) & (trim_pot_tune < 512) & (currentChannel != "CrossRhythms")):
                currentChannel = "CrossRhythms"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/CrossRhythms.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 512) & (trim_pot_tune < 768) & (currentChannel != "HopeFM")):
                currentChannel = "HopeFM"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/HopeFM.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 768) & (trim_pot_tune < 1024) & (currentChannel != "PremareLondon")):
                currentChannel = "PremareLondon"
                print currentChannel
                processStream = subprocess.Popen("./RadioStreams/PremareLondon.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        lastTrimPot_tune = trim_pot_tune

def adjustVolume(trim_pot_vol):

    #trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    #print trim_pot

    trimDifference_vol = abs(lastTrimPot_vol - trim_pot_vol)

    if trimDifference_vol >= trimTollerance:

        set_volume = trim_pot_vol / 10.24       # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
        set_volume = round(set_volume)          # round out decimal value
        set_volume = int(set_volume)            # cast volume as integer
        set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
        os.system(set_vol_cmd)  # set volume
        print 'volume set to:'
        print set_vol_cmd
        lastTrimPot_vol = trim_pot_vol


while True:

    print "----"

    input_state = GPIO.input(21)
    if input_state == False:
        waveBand = "BBC"

    input_state = GPIO.input(13)
    if input_state == False:
        waveBand = "Secular"

    input_state = GPIO.input(12)
    if input_state == False:
        waveBand = "Christian"

    adjustVolume(readadc(potentiometer_vol, SPICLK, SPIMOSI, SPIMISO, SPICS))
    playStation(readadc(potentiometer_tune, SPICLK, SPIMOSI, SPIMISO, SPICS))

    print "----"
    time.sleep(0.5)
