#!/usr/bin/python
# -*- coding: latin-1 -*-

# include libraries -----------------------------------------------------------

import time, datetime  # time functions
#import requests  # library for sending data over http
import thread  # loop is slow, needed for fast led pulse
import gpio  # led output
import os, sys, ast
from time import sleep

#vVerbose = str(sys.argv[1])
#if vVerbose.startswith('test'):
#    print 'pi-box starting'

# GPIO Settings BCM Layout
#TasterG = gpio.GPIOin(21)
#TasterB = gpio.GPIOin(16)
#TasterR = gpio.GPIOin(20)
#LedG = gpio.GPIOout(26)
#LedY = gpio.GPIOout(19)
#LedR = gpio.GPIOout(13)
BMelder = gpio.GPIOin(27)

# Start state
#LedR.on()
sleep(0.1)

INTERVAL_SENSORS = 60
INTERVAL_MD = 60
refreshTime_sensors = time.time() + INTERVAL_SENSORS
refreshTime_MD = time.time() + INTERVAL_MD
boolTasterG=False
boolTasterB=False
boolTasterR=False
boolBackLight=True
boolRun=True
boolMD=True
BoolDisplayAlwaysActive=False

#LedY.on()
sleep(0.1)

# functions for print out and WhatsApp
def LedsOFF():
#    LedG.on()
#    LedY.on()
#    LedR.on()
#    LedR.off()
    sleep(0.1)
#    LedY.off()
    sleep(0.1)
#    LedG.off()
    sleep(0.1)
    pass

def switchBL(trigger = 0):
	os.system("sudo /home/pi/dev/pi-box/SwitchBacklight.sh " + str(trigger))


def fadebacklight(trigger = 'on'):
    if trigger == 'on':
#        x = 255
        x = 128

        while x >= 0:
            os.system("sudo /home/pi/dev/pi-box/fadeBacklight.sh " + str(x))
            x = x - 25
    elif trigger=='off':
        x = 0       
#        while x < 256:
        while x < 128:
            os.system("sudo /home/pi/dev/pi-box/fadeBacklight.sh " + str(x))
            x = x + 10
        
fadebacklight('off')
os.system("epiphany-browser --display=:0 http://raspberrypi/index_kiosk.php & ")
sleep(20)
os.system("xte -x :0 \"key F11\"")
#LedG.on()
sleep(0.1)
print '  starte Schleife'
#LedsOFF()
    
while boolRun:
#    if TasterB.status() == 0 and TasterR.status() == 0:
#        print '  going done...'
#        boolRun = False
#        LedsOFF()
#        sleep(0.2)
#    elif TasterB.status() == 0:
#        print '    switch yellow LED'
#        if LedY.status() == 1:
#            os.system('killall epiphany-browser')
#            LedY.off()
#        else:
#            b_command = 'epiphany-browser -a --profile /home/pi/.config  http://raspberrypi/index_kiosk.php'
#            os.system(b_command + ' &')
#            LedY.on()
#        sleep(0.2)
#    elif TasterG.status() == 0:
#        if LedG.status() == 1:
#            LedG.off()
#            BoolDisplayAlwaysActive=False
#        else:
#            LedG.on()
#            BoolDisplayAlwaysActive=True
 #       print '    switch BoolDisplayAlwaysActive = ' + str(BoolDisplayAlwaysActive)
 #       sleep(0.2)
#    elif TasterR.status() == 0:
#        print '   switch red LED'
#        print '   switch Backlight'
#        if boolBackLight:
#            boolBackLight=False
#            LedR.on()
#            fadebacklight('on')
 #           switchBL(1)
 #       else:
 #           boolBackLight=True
 #           LedR.off()
 #           switchBL(0)
 #           fadebacklight('off')
 #       sleep(0.2)
    
    if (BMelder.status() == 1):
        #print 'Motion'
        boolMD = True
    else:
        #print 'No Motion'
        boolMD = False
        
    if boolMD:
        refreshTime_MD = time.time() + INTERVAL_MD
        #print str(refreshTime_MD)
        if not boolBackLight:
            boolBackLight=True
            #LedR.off()
            switchBL(0)
            fadebacklight('off')

    #print str(refreshTime_MD) + ' < ' + str(time.time()) + str(boolBackLight)
    if refreshTime_MD < time.time() and boolBackLight:
        #print str(refreshTime_MD) + ' < ' + str(time.time()) + str(boolBackLight)
        boolBackLight=False
#        LedR.on()
        fadebacklight('on')
        switchBL(1)
    
    sleep(0.01) # 0.1

print 'Ende - '

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

