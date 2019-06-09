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

echo "removing /usr/bin/automagic-fan/..."
rm -r /usr/bin/automagic-fan
echo "done"

echo "removing service from /lib/systemd/system/..."
rm /lib/systemd/system/automagic-fan.service
echo "done"

echo "removing config at /etc/automagic-fan/"
rm -r /etc/automagic-fan/
echo "done"

echo "automagic-fan uninstalled sucessfully!"
echo ""
echo "If you are dissatisfied,"
echo "please create an issue at the repo."
