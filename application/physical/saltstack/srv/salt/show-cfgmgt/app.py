#!/usr/bin/env python3

from gpiozero import RGBLED
from gpiozero import Button
from signal import pause
import os.path
import yaml

if ( os.path.isfile('config.yml')):
  with open("config.yml", "r") as configfile:
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

print(cfg['performance'])
print(speed)

led = RGBLED(red=17, green=18, blue=27)
button = Button(24)
state = 'init'
led.color = (0,0,1)

def state_transition():
  global state #eeeww
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
