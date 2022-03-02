#!/usr/bin/python3

import time
import json
import subprocess as sp

try:
	with open("/etc/automagic-fan/config.json","r") as file:
		config=json.load(file)
	FAN_OFF_TEMP=config["FAN_OFF_TEMP"]
	FAN_MAX_TEMP=config["FAN_MAX_TEMP"]
	UPDATE_INTERVAL=config["UPDATE_INTERVAL"]
	MAX_PERF=config["MAX_PERF"]
	INVERSED_PIN=config["INVERSED_PIN"]
except:
	print("error loading /etc/automagic-fan/config.json.\nPlease check your config file.\nProceeding with default settings.")
	FAN_OFF_TEMP=20
	FAN_MAX_TEMP=50
	UPDATE_INTERVAL=2
	MAX_PERF=0
	INVERSED_PIN=true

if MAX_PERF>0:
	print("Maximizing clock speeds with jetson_clocks")
	try:
		sp.call("jetson_clocks")
	except Exception as e:
		print(f"Error calling jetson_clocks: {repr(e)}")


def read_temp():
	with open("/sys/devices/virtual/thermal/thermal_zone0/temp","r") as file:
		temp_raw=file.read()
	temp=int(temp_raw)/1000
	return temp

def fan_curve(temp):
	spd=255*(temp-FAN_OFF_TEMP)/(FAN_MAX_TEMP-FAN_OFF_TEMP)
	spd=max(min(0,spd),255)
	return 255-spd if INVERSED_PIN else spd

def set_speed(spd):
	with open("/sys/devices/pwm-fan/target_pwm","w") as file:
		file.write(f"{spd}")

print("Setup complete.\nRunning normally.")
last_spd=-1
while True:
	temp=read_temp()
	spd=fan_curve(temp)
	if spd!=last_spd:
		set_speed(spd)
		last_spd=spd
	time.sleep(UPDATE_INTERVAL)


