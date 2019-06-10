# jetson-fan-ctl
Automagic fan control for the Nvidia Jetson Nano

## Requirements:

### Hardware
You will need a 5V PWM fan for this to make any sense.  
I used the **Noctua nf-a4x20 5V PWM** fan.

Additionally, I recommend you use the barrel jack with a 4A power supply.  

### Software

All necessary dependencies are already installed on the Jetson Nano. jetson-fan-ctl only depends on python2.

## How to install:

    ./install.sh

## How to customize:

Create /etc/automagic-fan/config.json with your favorite editor (I'm using nano):  

    sudo nano /etc/automagic-fan/config.json

The following options are supported:

    {
    "FAN_OFF_TEMP":20,
    "FAN_MAX_TEMP":50,
    "UPDATE_INTERVAL":2
    }

<code>FAN_OFF_TEMP</code> is the temperature below which the fan is turned off.  
<code>FAN_MAX_TEMP</code> is the temperature above which the fan is at 100% speed.  
<code>UPDATE_INTERVAL</code> is the update interval for the script in seconds

Any changes in the script or configuration will be will be applied on reboot or after a service restart like:

    sudo service automagic-fan restart
    
    (OR)
    
    systemctl restart automagic-fan
