#!/bin/bash
pkill -SIGKILL mpg321
pkill -9 python
sudo git pull
sudo python RadioPi.py
