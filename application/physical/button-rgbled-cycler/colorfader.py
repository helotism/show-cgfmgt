#!/usr/bin/env python3
#/** 
#  * A simple script to fade a RGB led through colors.
#  * 
#  * Copyright (c) 2016 Christian Prior
#  * Licensed under the MIT License. See LICENSE file in the project root for full license information.
#  * 
#  * Works with gpiozero on all its supported Raspberry Pi boards.
#  * Used as a sample "application" to demonstrate Saltstack's event-driven infrastructure capabilities.
#  * 
#  */

from gpiozero import RGBLED
from gpiozero import Button
from time import sleep
import random
from signal import pause
import os.path
import yaml

if ( os.path.isfile('config.yml')):
  with open("config.yml", "r") as configfile:
    cfg = yaml.load(configfile)
elif ( os.path.isfile('config_orig.yml')):
  with open("config.yml", "r") as configfile:
    cfg = yaml.load(configfile)


led = RGBLED(red=cfg['red_pin'], green=cfg['green_pin'], blue=cfg['blue_pin'])
button = Button(cfg['button_pin'])

colors = [ (1,0,0), (0,1,0), (1,1,0), (1,1,1) ]

#while True:
#  led.blink(on_time=1, off_time=1, fade_in_time=1, fade_out_time=1, on_color=random.choice(colors), off_color=(0, 0, 0), n=1, background=False)
#  sleep(1)

while True:
  led.color = random.choice(colors)
  sleep(2)

