# !usr/bin/evn python
# coding:utf-8

import RPi.GPIO as GPIO
import time
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trig = 18
echo = 23

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

def getDistance(trig,echo):
	GPIO.output(trig,GPIO.HIGH)
	time.sleep(0.00005)
	GPIO.output(trig,GPIO.LOW)
#防死循环
	while GPIO.input(echo) == GPIO.LOW:
		pass

	s = datetime.datetime.now()
	while GPIO.input(echo) == GPIO.HIGH:
		pass
	e = datetime.datetime.now()
	t = int((e-s).microseconds)
	
	return t*0.017
try:
	print (getDistance(trig,echo))
except KeyboardInterrupt:
	GPIO.output(trig,GPIO.low)
	GPIO.cleanup()
