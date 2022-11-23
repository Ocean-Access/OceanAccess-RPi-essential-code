#!/bin/sh
echo "We will install the following packages \n"
echo "https://github.com/pololu/dual-g2-high-power-motor-driver-rpi to use the motor controller"
echo "https://github.com/bluerobotics/ping-python to use the Blue Robotics Ping Sonar \n"
echo "installing the motor driver first \n"

sudo apt install python-pigpio
sudo systemctl start pigpiod
git clone https://github.com/pololu/dual-g2-high-power-motor-driver-rpi
cd dual-g2-high-power-motor-driver-rpi
sudo python setup.py install

echo "now we will install the blue robotics ping sonar"
pip install --user bluerobotics-ping --upgrade