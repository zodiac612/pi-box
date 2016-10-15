
#!/usr/bin/python
# -*- coding: latin-1 -*-

# include libraries -----------------------------------------------------------

import time, datetime  # time functions
import requests  # library for sending data over http
import thread  # loop is slow, needed for fast led pulse
#import gpio  # led output
import os, sys, ast
#from whatsapp import sendWhatsApps
import ConfigParser
#from sensorHistory import sensorHistory
from time import sleep
#from plotting import plotting_DeviceValues
from sensorCrypt import sensorCrypt
#from sensorLight import sensorLight #ok
#from sensorInterval import sensorInterval #ok
from sensorConfig import sensorConfig #ok
#from sensorThreads import threadPICAM2
#from sensorThreads import threadFritzActors2 #ok
#from sensorThreads import threadNetDiscovery #ok
#from sensorThreads import threadCreatePHPFile #ok
#from sensorThreads import threadWebradioService
#from sensorSwitches import sensorSwitches
#from sensorDevice import moduleDevice
#from sensorService import threadSensors
#import Queue

vVerbose = str(sys.argv[1])
if vVerbose.startswith('test'):
    print 'sensorService starting'
sConfig = sensorConfig('sensorTool.conf', vVerbose)
#sensorSwitches('/home/pi/sensorTool/switches.conf', vVerbose);

# GPIO Settings BCM Layout
#RelayIN1 = gpio.GPIOout(sConfig.getGPIORelayIN1())
#RelayIN2 = gpio.GPIOout(sConfig.getGPIORelayIN2())
#LedG = gpio.GPIOout(sConfig.getGPIOLedGreen())
#LedY = gpio.GPIOout(sConfig.getGPIOLedYellow())
#LedR = gpio.GPIOout(sConfig.getGPIOLedRed())
#BMelder = gpio.GPIOin(sConfig.getGPIOmotion())
#Leuchte = sensorLight(sConfig.getGPIOlight())

# Start state
#LedG.on()
#LedY.on()
#LedR.on()
#boolLeuchte = False

# constants -------------------------------------------------------------------
sCrypt = sensorCrypt(sConfig.getCryptKey())
#MAXTIME = sConfig.getMaxTime() 
#MINTIME = sConfig.getMinTime() 
INTERVAL_SENSORS = sConfig.getIntervalSensors()
#INTERVAL_FRITZACTORS = sConfig.getIntervalActors()
#INTERVAL_WEBRADIO = sConfig.getIntervalWebradio()
#INTERVAL_LANDEVICES = sConfig.getIntervalLANDevices()
SERVER = 'raspberrypi' #sConfig.getServer()
print SERVER

#riggerCountA = sConfig.getTriggerCountA()
#TriggerCountB = sConfig.getTriggerCountB()

#dictInterval = {}
#dictInterval = sensorInterval(sConfig.getDictIntervalle())

vTitel = sConfig.getTitel()

#dictActors = {}    
dictSensors = {}
dictSensors = sConfig.getDictSensors()
iControlSensor = sConfig.getiControlSensor()
iOutdoorSensor = sConfig.getiOutdoorSensor()
boolOutdoorSensor = False
if iOutdoorSensor is not None:
   boolOutdoorSensor = True

# Config Variable leeren
sConfig = None

vBoolLC = True
# fritz off moved after first fritzactors call

#degC = 0
#hPa = 0
#hRel = 0
#degC1 = 0
#hPa1 = 0
#vBoolSensor1 = True
#counterHigh = 0
#counterLow = 0
#timeDuration = 0

INTERVAL_SENSORS = 20
# refresh for sensor data
refreshTime_sensors = time.time()# + INTERVAL_SENSORS

# loop ------------------------------------------------------------------------
#LedR.off()
if vVerbose.startswith('test'):
    print 'Config loaded'
    print str(refreshTime_sensors) + '##' + str(time.time())
    
while True:  # timeDuration <= MAXTIME: 

    # every refreshtime  seconds,  get data from SensorService
    if time.time() > refreshTime_sensors:
        if vVerbose.startswith('test'):
            print str(time.time())+'while: refreshTime_sensors ('+str(refreshTime_sensors)+')'
            print str(refreshTime_sensors) + '##' + str(time.time())
            print '.'
        # Werte holen per http request ::D
        try:
            dictResponse = {}
            
            vBoolUseSensorValueFile = False
            if vBoolUseSensorValueFile:
                try:
                    handle = open ('/var/sensorTool/sensorValues', 'r')
                    line = " "
                    while line:
                        line = handle.readline()
                        print line
                        if len(line) > 0:
                            dictResponse = ast.literal_eval(line)
                    handle.close()
                except Exception as e:
                    print str(e)
            else:
                rqtime = time.time()
                # print 'Get HTTP Service'
                r = requests.get("http://" + SERVER + ":6666")
                # request enthaelt "
                #print r
                vR = sCrypt.Decrypt(r.text[1:len(r.text) - 1])
                # print vR
                dictResponse = ast.literal_eval(str(vR))
                
            print 'dictResponse:' #+ str(dictResponse) 
            for vSensor in dictResponse:
                dictTemp = {}
                dictTemp['ID'] = vSensor
                if 'Time' in dictResponse[vSensor]:
                    dictTemp['Time'] = dictResponse[vSensor]['Time']
                if 'RH' in dictResponse[vSensor]:
                    dictTemp['RH'] = dictResponse[vSensor]['RH']
                if 'T' in dictResponse[vSensor]:
                    dictTemp['T'] = dictResponse[vSensor]['T']
                if 'hPa' in dictResponse[vSensor]:    
                    dictTemp['hPa'] = dictResponse[vSensor]['hPa']
                
                boolBME280 = False
                if (vSensor == 'bme280') :
                    boolBME280 = True
                #print '  ' + str(dictTemp)
                
                for vKey in dictSensors:
                    if dictSensors[vKey].GetHex() == vSensor:
                        dictSensors[vKey].SetSensorData(dictTemp, boolBME280)
                        print dictSensors[vKey].GetInfo()
            print 'Request-Time: ' + str(time.time()-rqtime)
           
        except Exception as e:
            print e

        refreshTime_sensors = time.time() + INTERVAL_SENSORS
    sleep(0.5) # 0.1

print ' - Ende - '

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
