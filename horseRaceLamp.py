#!/usr/bin/env python
# coding=utf-8

import RPi.GPIO as GPIO
import time
import random

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

led1=[14,15,18]
led2=[24,25,8]
led3=[12,16,20]

GPIO.setup(led1,GPIO.OUT,initial=0)
GPIO.setup(led2,GPIO.OUT,initial=0)
GPIO.setup(led3,GPIO.OUT,initial=0)

try:
    while True:
        GPIO.output(led1,[random.randint(0,1),random.randint(0,1),random.randint(0,1)])
        time.sleep(1)
        GPIO.output(led1,[0,0,0])
        GPIO.output(led2,[random.randint(0,1),random.randint(0,1),random.randint(0,1)])
        time.sleep(1)
        GPIO.output(led2,[0,0,0])
        GPIO.output(led3,[random.randint(0,1),random.randint(0,1),random.randint(0,1)])
        time.sleep(1)
        GPIO.output(led3,[0,0,0])
except:
    GPIO.output(led1,[0,0,0])
    GPIO.output(led2,[0,0,0])
    GPIO.output(led3,[0,0,0])
GPIO.cleanup()
