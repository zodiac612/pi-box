#!/bin/sh
vV=$1
#if [ "$vV" = "1" ]; then
#    vV=1
#else
#	vV=0
#fi


echo $vV > /sys/class/backlight/rpi_backlight/brightness

#/etc/sudoers
#pi ALL=NOPASSWD:/home/pi/dev/pi-box/SwitchBacklight.sh
