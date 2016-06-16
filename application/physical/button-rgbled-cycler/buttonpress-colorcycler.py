#!/usr/bin/env python3
#/** 
#  * A simple script to read button presses and cycle through colors.
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

state = 'init'
led.color = (0,0,1)

if ( os.path.isfile('performance.yml')):
  with open("performance.yml", "r") as configfile:
    cfg = yaml.load(configfile)
elif ( os.path.isfile('performance_orig.yml')):
  with open("performance.yml", "r") as configfile:
    cfg = yaml.load(configfile)

if cfg['performance'] == "":
  speed=2
elif cfg['performance'] == "silver":
  speed=2
elif cfg['performance'] == "gold":
  speed=1
elif cfg['performance'] == "platinum":
  speed=0.5
else:
   speed=2

def state_transition():

  global state #eeeww

  #even worse: Read the file on every button press
  #better would be: https://github.com/gorakhargosh/watchdog#example-api-usage
  if ( os.path.isfile('performance.yml')):
    with open("performance.yml", "r") as configfile:
      cfg = yaml.load(configfile)
  elif ( os.path.isfile('performance_orig.yml')):
    with open("performance.yml", "r") as configfile:
      cfg = yaml.load(configfile)

  if cfg['performance'] == "":
    speed=2
  elif cfg['performance'] == "silver":
    speed=2
  elif cfg['performance'] == "gold":
    speed=1
  elif cfg['performance'] == "platinum":
    speed=0.5
  else:
    speed=2

  print(state)
  if ( state is 'init'):
    state = 'init2green'
    led.blink(speed,speed,on_color=(0,1,0))
  elif ( state is 'init2green'):
    state = 'green2yellow'
    led.blink(speed,speed,on_color = (1,0.7,0))
  elif ( state is 'green2yellow'):
    state = 'yellow2red'
    led.blink(speed,speed,on_color = (1,0,0))
  elif ( state is 'yellow2red'):
    state = 'red2yellow'
    led.blink(speed,speed,on_color = (1,0.7,0))
  elif ( state is 'red2yellow'):
    state = 'yellow2green'
    led.blink(speed,speed,on_color = (0,1,0))
  elif ( state is 'yellow2green'):
    state = 'green2yellow'
    led.blink(speed,speed,on_color = (1,1,0))
  elif ( state is 'error'):
    state = 'init'
    led.blink(speed,speed,on_color = (1,1,1))
  print(state)

led.blink(speed,speed)
button.when_pressed = state_transition

pause()
