#!/usr/bin/python3

import time
import json
import subprocess as sp

def read_temp():
  try:
    with open("/sys/devices/virtual/thermal/thermal_zone0/temp","r") as file:
      temp_raw=file.read()
    temp=int(temp_raw)/1000
    return temp
  except:
    print("Couldn't read the system temperature, returning 0")
    return 0

def fan_curve(temp, fan_off_temp, fan_max_temp):
  spd=255*(temp-fan_off_temp)/(fan_max_temp-fan_off_temp)
  return int(min(max(0,spd),255))

def set_speed(spd):
  try:
    with open("/sys/devices/pwm-fan/target_pwm","w") as file:
      file.write(f"{spd}")
  except:
    print("Couldn't set the fan speed")

def main():
  try:
    with open("/etc/automagic-fan/config.json","r") as file:
      config=json.load(file)
    fan_off_temp=config["FAN_OFF_TEMP"]
    fan_max_temp=config["FAX_MAX_TEMP"]
    update_interval=config["UPDATE_INTERVAL"]
    max_perf=config["MAX_PERF"]
  except:
    print("Error loading /etc/automagic-fan/config.json.\nPlease check your config file.\nProceeding with default settings.")
    fan_off_temp=20
    fan_max_temp=50
    update_interval=2
    max_perf=0

  if max_perf>0:
    print("Maximizing clock speeds with jetson_clocks")
    try:
      sp.call("jetson_clocks")
    except Exception as e:
      print(f"Error calling jetson_clocks: {repr(e)}")
  print("Setup complete.\nRunning normally.")
  last_spd=-1
  while True:
    temp=read_temp()
    spd=fan_curve(temp, fan_off_temp, fan_max_temp)
    if spd!=last_spd:
      set_speed(spd)
      last_spd=spd
    time.sleep(update_interval)
