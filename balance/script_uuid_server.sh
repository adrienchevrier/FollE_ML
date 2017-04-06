#!/bin/bash

while true ; do
	#statements

	# enable bluetooth
	sudo systemctl start bluetooth

	sleep 1

	# run the program bluez
	echo -e 'remove 2C:59:8A:A2:DD:16 \nquit' | bluetoothctl
	echo -e 'remove C0:EE:FB:D8:7B:FD \nquit' | bluetoothctl
	echo -e 'power on\ndiscoverable on\t \nquit' | bluetoothctl

	sleep 1

	sudo python Bluetooth_Balance.py

	
done
sudo reboot