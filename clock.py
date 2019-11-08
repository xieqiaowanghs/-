#!/usr/bin/evn python
#coding:utf-8

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def start(clk,dio):
	#clk high dio high->low
	GPIO.output(clk,GPIO.HIGH)
	GPIO.output(dio,GPIO.HIGH)
	GPIO.output(dio,GPIO.LOW)#start
	GPIO.output(clk,GPIO.LOW)

def stop(clk,dio):
	GPIO.output(clk,GPIO.LOW)
	GPIO.output(dio,GPIO.LOW)
	GPIO.output(clk,GPIO.HIGH)
	GPIO.output(dio,GPIO.HIGH)

def sendData(clk,dio,data):
	for i in range(0,8):
		GPIO.output(clk,GPIO.LOW)
		if data & (1<<i) == 0:
			GPIO.output(dio,GPIO.LOW)
		else:
			GPIO.output(dio,GPIO.HIGH)
		GPIO.output(clk,GPIO.HIGH)
	#第八个下降沿
	GPIO.output(clk,GPIO.LOW)
	#触发ack
	GPIO.output(dio,GPIO.HIGH)
	GPIO.output(clk,GPIO.HIGH)
	GPIO.setup(dio,GPIO.IN)

	if GPIO.input(dio) == GPIO.HIGH:
		GPIO.setup(dio,GPIO.OUT)
		return
	GPIO.setup(dio,GPIO.OUT)
def tm1637(clk,dio,data):
	start(clk,dio)
	sendData(clk,dio,0B01000000)
	stop(clk,dio)

	start(clk,dio)
	sendData(clk,dio,0B11000000)

	sendData(clk,dio,data[0])
	sendData(clk,dio,data[1])
	sendData(clk,dio,data[2])
	sendData(clk,dio,data[3])
	stop(clk,dio)

	start(clk,dio)
	sendData(clk,dio,0B10001111)
	stop(clk,dio)

clk = 16
dio = 12
GPIO.setup(clk,GPIO.OUT)
GPIO.setup(dio,GPIO.OUT)
tm1637(clk,dio,[0x3f,0x06,0x5b,0x3f])
try:
	while True:
		pass
except KeyboardInterrupt:
	GPIO.output(clk,GPIO.LOW)
	GPIO.output(dio,GPIO.LOW)
	GPIO.cleanup()

