#!/bin/bash

#Require sudo
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "installing to /usr/bin/automagic-fan/..."
cp fanctl.py /usr/bin/
echo "done"

echo "adding automagic-fan.service service to systemd"
cp automagic-fan.service /lib/systemd/system/
chmod 644 /lib/systemd/system/automagic-fan.service
systemctl daemon-reload
echo "done"

echo "Installation complete."
echo "To start the service, run:            'systemctl start automagic-fan'"
echo "To enable the service on startup, run 'systemctl enable automagic-fan'"

