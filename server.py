#!/usr/bin/env python
#coding: utf-8

import socket
import thread
import RPi.GPIO as GPIO
import time
import datetime
import random
import math
#import controlLib

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

speed = 30  #初始速度
flag = 0    
car = [4,17,27,22]  #发动机控制引脚
eng = 5
auto = [6,13,19,26] #循迹模块输入
GPIO.setup(car,GPIO.OUT)
GPIO.setup(eng,GPIO.OUT)
GPIO.setup(auto,GPIO.IN)

#转向灯
led = [23,24]
GPIO.setup(led,GPIO.OUT)
#蜂鸣器
buzzer = 18
GPIO.setup(buzzer,GPIO.OUT)

#数字管模块
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
#超声模块
trig = 20
echo = 21
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

#数码管设置
clk = 16
dio = 12
GPIO.setup(clk,GPIO.OUT)
GPIO.setup(dio,GPIO.OUT)

#以下12代表左右侧轮胎 
p_eng = GPIO.PWM(eng,50)
p_positive1 = GPIO.PWM(car[0],50)
p_positive2 = GPIO.PWM(car[2],50)
p_negative1 = GPIO.PWM(car[1],50)
p_negative2 = GPIO.PWM(car[3],50)
p_eng.start(0)
p_positive1.start(0)
p_positive2.start(0)
p_negative1.start(0)
p_negative2.start(0)

def movecar(s,clientSock):
	msg = s.encode('utf-8')
	global speed
	global led
	global buzzer
	GPIO.output(led,[0,0])
	GPIO.output(buzzer,0)
	print (s)
	if s == "up": 
		p_positive1.ChangeDutyCycle(speed)
		p_positive2.ChangeDutyCycle(speed)
		p_negative1.ChangeDutyCycle(0)
		p_negative2.ChangeDutyCycle(0)
		clientSock.send(msg)
	elif s == "down":
		p_positive1.ChangeDutyCycle(0)
		p_positive2.ChangeDutyCycle(0)
		p_negative1.ChangeDutyCycle(30)
		p_negative2.ChangeDutyCycle(30)
		GPIO.output(buzzer,1)
		clientSock.send(msg)
	elif s == "left":
		p_positive1.ChangeDutyCycle(45)
		p_positive2.ChangeDutyCycle(0)
		p_negative1.ChangeDutyCycle(0)
		p_negative2.ChangeDutyCycle(45)
		GPIO.output(led,[0,1])
		clientSock.send(msg)
	elif s == "right":
		p_positive1.ChangeDutyCycle(0)
		p_positive2.ChangeDutyCycle(45)
		p_negative1.ChangeDutyCycle(45)
		p_negative2.ChangeDutyCycle(0)
		GPIO.output(led,[1,0])
		clientSock.send(msg)
	elif s == "speedup": 
		if speed <= 90:
			speed += 10
		msg = 'current speed : '+ str(speed)
		clientSock.send(msg.encode('utf-8'))
	elif s == "slowdown":
		if speed >= 10:
			speed -= 10
		msg = 'current speed : '+ str(speed)
		clientSock.send(msg.encode('utf-8'))
	elif s == "stop":
		p_positive1.ChangeDutyCycle(0)
		p_positive2.ChangeDutyCycle(0)
		p_negative1.ChangeDutyCycle(0)
		p_negative2.ChangeDutyCycle(0)
		clientSock.send(msg)

def automove(clientSock):
	while True:
		global flag
		while flag == 1:
			#if GPIO.input(auto[0]) == GPIO.LOW and GPIO.input(auto[3]) == GPIO.LOW:
			if GPIO.input(auto[1]) == GPIO.HIGH and GPIO.input(auto[2]) == GPIO.HIGH:
				movecar('up',clientSock)
			elif GPIO.input(auto[1]) == GPIO.HIGH and GPIO.input(auto[2]) == GPIO.LOW:
				movecar('right',clientSock)
			elif GPIO.input(auto[1]) == GPIO.LOW and GPIO.input(auto[2]) == GPIO.HIGH:
				movecar('left',clientSock)
			#else:
				#movecar('down',clientSock)

def getDistance(trig,echo):
	GPIO.output(trig,GPIO.HIGH)
	time.sleep(0.00005)
	GPIO.output(trig,GPIO.LOW)
	k = 0
	while GPIO.input(echo) == GPIO.LOW:
		k += 1
		if k > 200:
			time.sleep(0.5)
			print ("recalculating>>>>")
			return getDistance(trig,echo)
	s =datetime.datetime.now()
	while GPIO.input(echo) == GPIO.HIGH:
		k += 1
		if k > 200:
			time.sleep(0.5)
			print ("recalculating>>>>")
			return getDistance(trig,echo)
	e = datetime.datetime.now()
	t = int ((e-s).microseconds)
	return t*0.017
#获取数据管对应值
def getdata(value):
	ox = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x79]
	data = []
	value = int(value)
	if value >= 0 and value < 10000:
		data.append(ox[value//1000])
		value = value % 1000
		data.append(ox[value//100])
		value = value % 100
		data.append(ox[value//10])
		value = value % 10
		data.append(ox[value])
	else:
		data = [ox[10]]*4
	return data
#开启避障
def startengine(clientSock):
	while True:
		global trig
		global echo
		global p_eng
		global flag
		distance = [-20,-10]
		while flag == 2:
			stuckflag = False
			movecar('up',clientSock)
			p_eng.ChangeDutyCycle(4.4)
			distance[0] = distance[1]
			distance[1] = getDistance(trig,echo)
			tm1637(clk,dio,getdata(distance[1]))
			time.sleep(0.5)
			stuckvalue = distance[0]-distance[1]
			if stuckvalue > -1 and stuckvalue < 1:
				stuckflag = True
				s = 'car is stucked'
				print(s)
				clientSock.send(s.encode('utf-8'))
			if distance[1] < 30 or stuckflag:
				movecar('stop',clientSock)
			#找空地
				i = 0
				searchflag = True
				while searchflag:
					while i < 5:
						p_eng.ChangeDutyCycle(2.5 + i)
						i += 0.5
						distance[0] = distance[1]
						distance[1] = getDistance(trig,echo)
						tm1637(clk,dio,getdata(distance[1]))
						if distance[1] >= 30:
							searchflag = False
							movecar('down',clientSock)
							if i > 1.9:
								time.sleep((i-1.9)*0.1 + 0.2)
								movecar('left',clientSock)
								time.sleep((i-1.9)*0.2 + 0.2)
							else:
								time.sleep((1.9-i)*0.1 + 0.2)
								movecar('right',clientSock)
								time.sleep((1.9-i)*0.2 + 0.2)  
							break
						time.sleep(0.5)
					if searchflag == True:
						movecar('down',clientSock)
						time.sleep(0.5)
						movecar('right',clientSock)
						time.sleep(2)
						break

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
server_address = ('192.168.191.2',9999)
ret = s.bind(server_address)
print(type(ret),ret)
s.listen(15)

try:
	while True:
		print("接收客户端的连接...")
		clientSock,clientAddr = s.accept()   #连接
		print(clientSock,clientAddr)

		thread.start_new_thread(automove,(clientSock,))
		thread.start_new_thread(startengine,(clientSock,))

		while True:
			
			msg = clientSock.recv(1024)
			s = msg.decode('utf-8')
			print(s)
			if s == 'auto' and flag == 0:
				movecar('stop',clientSock)
				flag = 1
			elif s == 'normal':
			#根据flag结束线程
				flag = 0
				movecar('stop',clientSock)
			elif s == 'ultraSound' and flag == 0:
				movecar('stop',clientSock)
				flag = 2
			elif s == 'soundControl' and flag == 0:
				movecar('stop',clientSock)
				flag = 3
			else:
				movecar(s,clientSock)
except KeyboardInterrupt:
	print('--------------------')
	GPIO.cleanup()
	pass
