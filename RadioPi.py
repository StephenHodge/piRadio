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
waveBand = 0;

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
potentiometer_tune = 7;
potentiometer_vol = 6;

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


while True:

    input_state1 = GPIO.input(21)
    input_state2 = GPIO.input(13)
    input_state3 = GPIO.input(12)

    if input_state1 == False:
        waveBand = 1
        #print("Button is PIN 21 DOWN")
    else input_state2 == False:
        waveBand = 2
        #print("Button is PIN 13 DOWN")
    else input_state3 == False:
        waveBand = 3
        #print("Button is PIN 12 DOWN")


    # read the analog pin
    trim_pot_tune = readadc(potentiometer_tune, SPICLK, SPIMOSI, SPIMISO, SPICS)
    trimDifference_tune = abs(trim_pot_tune - lastTrimPot_tune)

    if trimDifference_tune >= trimTollerance:

        print "tune:"
        print trim_pot_tune
        print "..."

        if waveBand == 1:

            if (trim_pot_tune < 250) & (currentChannel != "Radio_One"):
                currentChannel = "Radio_One"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/BBC1.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 250) & (trim_pot_tune < 300)) & (currentChannel != "Radio_Two"):
                currentChannel = "Radio_Two"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/BBC2.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 300) & (trim_pot_tune < 350)) & (currentChannel != "Radio_Three"):
                currentChannel = "Radio_Three"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/BBC3.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 350) & (trim_pot_tune < 400)) & (currentChannel != "Radio_Four"):
                currentChannel = "Radio_Four"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/BBC4.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if (trim_pot_tune >= 400) & (currentChannel != "Radio_Five"):
                currentChannel = "Radio_Five"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/BBC5Live.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        if waveBand == 2:

            if (trim_pot_tune < 250) & (currentChannel != "Six_Music"):
                currentChannel = "Six_Music"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/BBC6Music.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 250) & (trim_pot_tune < 300)) & (currentChannel != "Radio_Devon"):
                currentChannel = "Radio_Devon"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/BBCRadioDevon.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 300) & (trim_pot_tune < 350)) & (currentChannel != "ClassicFM"):
                currentChannel = "ClassicFM"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/ClassicFM.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 350) & (trim_pot_tune < 400)) & (currentChannel != "CrossRhythms"):
                currentChannel = "CrossRhythms"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/CrossRhythms.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 400) & (trim_pot_tune <= 450)) & (currentChannel != "CrossRhythms2"):
                currentChannel = "CrossRhythms2"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/CrossRhythms2.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if (trim_pot_tune >= 450) & (currentChannel != "HopeFM"):
                currentChannel = "HopeFM"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/HopeFM.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        if waveBand == 3:

            if (trim_pot_tune < 250) & (currentChannel != "PremareLondon"):
                currentChannel = "PremareLondon"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/PremareLondon.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            if ((trim_pot_tune >= 250)) & (currentChannel != "RadioNorthDevon"):
                currentChannel = "RadioNorthDevon"
                print currentChannel
                process = subprocess.Popen("./RadioStreams/RadioNorthDevon.sh", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        lastTrimPot_tune = trim_pot_tune

        # read the analog pin
        trim_pot_vol = readadc(potentiometer_vol, SPICLK, SPIMOSI, SPIMISO, SPICS)

        trimDifference = abs(trim_pot_vol - lastTrimPot_vol)

        if trimDifference >= trimTollerance:
            set_volume = trim_pot_vol / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
            set_volume = round(set_volume)          # round out decimal value
            set_volume = int(set_volume)            # cast volume as integer
            set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
            os.system(set_vol_cmd)  # set volume

            print "Volume: "
            print trim_pot_vol
            print "..."

        lastTrimPot_vol = trim_pot_vol

        time.sleep(0.5)
