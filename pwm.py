#!usr/bin/evn python
#coding:utf-8

#PWM Pulse Width Modify

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

eng = 5
GPIO.setup(eng,GPIO.OUT)
P_eng = GPIO.PWM(eng,50)

P_eng.start(2.5)
time.sleep(1)

try:
	i = 0
	while True:
		while i < 4:
			i += 0.1
			P_eng.ChangeDutyCycle(2.5 + i)
			print (i)
			time.sleep(0.5)
		while i > 0:
			i -= 0.1
			P_eng.ChangeDutyCycle(2.5 + i)
			print (i)
			time.sleep(0.5)
except KeyboardInterrupt:
	GPIO.setup(eng,0)
	GPIO.cleanup()

'''
led = 18

GPIO.setup(led,GPIO.OUT)
pwmLed = GPIO.PWM(led,50)
pwmLed.start(0)


try:
	
	while True:
		for i in range(1,20):
			pwmLed.ChangeDutyCycle(5*i)
			time.sleep(0.05)
		for i in range(20,-1,-1):
			pwmLed.ChangeDutyCycle(5*i)
			time.sleep(0.05)

except KeyboardInterrupt:
	GPIO.setup(led,0)
	GPIO.cleanup()

led = [23,24]
buzzer = 18
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,[1,1])
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer,1)
try:
	while True:
		pass
except KeyboardInterrupt:
	GPIO.output(led,[0,0])
	GPIO.output(buzzer,0)
	GPIO.cleanup()
'''
