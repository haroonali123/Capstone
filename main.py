import Thermotron
import MFC
import Sensors
#import serial

#Enumerate ports from hub.
MFC1_port = 'COM4'
MFC2_port = ''
Thermotron_port = ''
Sensor1 = ''
Sensor2 = ''
Sensor3 = ''

#Connect to all devices
MFC1 = MFC.MFC_device(MFC1_port)
MFC1.getFlowRate('02')

#Run experiment