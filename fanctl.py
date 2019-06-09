#!/usr/bin/python3
import time
import json
import subprocess as sp

sp.call("jetson_clocks")

try:
	with open("/etc/automagic-fan/config.json","r") as file:
		config=json.load(file)
	FAN_OFF_TEMP=config["FAN_OFF_TEMP"]
	FAN_MAX_TEMP=config["FAN_MAX_TEMP"]
	UPDATE_INTERVAL=config["UPDATE_INTERVAL"]
except:
	FAN_OFF_TEMP=20
	FAN_MAX_TEMP=50
	UPDATE_INTERVAL=2


def read_temp():
	with open("/sys/devices/virtual/thermal/thermal_zone0/temp","r") as file:
		temp_raw=file.read()
	temp=int(temp_raw)/1000
	return temp

def fan_curve(temp):
	spd=255*(temp-FAN_OFF_TEMP)/(FAN_MAX_TEMP-FAN_OFF_TEMP)
	return int(min(max(0,spd),255))

def set_speed(spd):
	with open("/sys/devices/pwm-fan/target_pwm","w") as file:
		file.write(f"{spd}")

while True:
	temp=read_temp()
	spd=fan_curve(temp)
	out=set_speed(spd)
	time.sleep(UPDATE_INTERVAL)


