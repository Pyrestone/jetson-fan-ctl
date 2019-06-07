import subprocess as sp
import time

FAN_OFF_TEMP=20
FAN_MAX_TEMP=50
UPDATE_INTERVAL=2


def read_temp():
	temp_raw=sp.check_output(["cat","/sys/devices/virtual/thermal/thermal_zone0/temp"])
	temp=int(temp_raw.decode("utf8"))/1000
	return temp

def fan_curve(temp):
	spd=255*(temp-FAN_OFF_TEMP)/(FAN_MAX_TEMP-FAN_OFF_TEMP)
	return int(min(max(0,spd),255))

def set_speed(spd):
	return sp.check_output(['sudo', 'sh', '-c', f'echo {spd} > /sys/devices/pwm-fan/target_pwm'])

while True:
	temp=read_temp()
	spd=fan_curve(temp)
	out=set_speed(spd)
	time.sleep(UPDATE_INTERVAL)


