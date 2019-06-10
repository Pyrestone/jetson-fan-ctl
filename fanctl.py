#!/usr/bin/env python
from __future__ import print_function, division

import time
import json

CONFIG_FILENAME = "/etc/automagic-fan/config.json"
DEFAULT_SETTINGS = {
    'FAN_OFF_TEMP': 20,
    'FAN_MAX_TEMP': 50,
    'UPDATE_INTERVAL': 2,
}

# uncomment to Maximize jetson performance by setting static max frequency to CPU, GPU and EMC clocks.
# sp.call("jetson_clocks")

config = dict(DEFAULT_SETTINGS)  # copy of DEFAULT_SETTINGS as config

try:
    with open(CONFIG_FILENAME, "r") as config_file:
        print('Loading config: {fn}'.format(fn=CONFIG_FILENAME))
        config.update(json.load(config_file))
except FileNotFoundError:
    pass


def read_temp():
    with open("/sys/devices/virtual/thermal/thermal_zone0/temp", "r") as f:
        temp_raw = f.read()
    return int(temp_raw) / 1000


def fan_curve(tmp):
    speed = 255 * (tmp - config['FAN_OFF_TEMP']) / (config['FAN_MAX_TEMP'] - config['FAN_OFF_TEMP'])
    return int(min(max(0, speed), 255))


def set_speed(spd):
    if not 0 <= spd <= 255:
        raise ValueError('spd')
    with open("/sys/devices/pwm-fan/target_pwm", "w") as f:
        f.write(str(spd))


while True:
    temp = read_temp()
    set_speed(fan_curve(temp))
    time.sleep(config['UPDATE_INTERVAL'])
