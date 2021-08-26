#!/bin/bash

#Require sudo
if [ $EUID != 0 ]; then
  sudo "$0" "$@"
  exit $?
fi

apt-get update
apt-get install python3-pip

pip3 install "https://github.com/rnsc/jetson-fan-ctl/releases/download/v0.1.0/jetsonfanctl-0.1.0-py3-none-any.whl"

echo "adding service to /lib/systemd/system/..."
cp automagic-fan.service /lib/systemd/system/
chmod 644 /lib/systemd/system/automagic-fan.service
echo "done"

echo "creating config at /etc/automagic-fan/"
mkdir /etc/automagic-fan/
cp config.json /etc/automagic-fan/
chmod 664 /etc/automagic-fan/config.json
echo "done"

echo "starting and enabling service..."
systemctl daemon-reload
systemctl start automagic-fan
systemctl enable automagic-fan
echo "done"

echo "automagic-fan installed sucessfully!"
echo ""
echo "To configure, edit /etc/automagic-fan/config.json (needs sudo)"
