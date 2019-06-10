#!/bin/bash

#Require sudo
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "removing service..."
systemctl stop automagic-fan
systemctl disable automagic-fan
echo "done"

echo "removing /usr/bin/fanctl.py"
rm /usr/bin/fanctl.py
echo "done"

echo "removing service from /lib/systemd/system/automagic-fan.service"
rm /lib/systemd/system/automagic-fan.service
echo "done"

echo "automagic-fan uninstalled sucessfully!"
echo ""
echo "If you are dissatisfied,"
echo "please create an issue at the repo."
