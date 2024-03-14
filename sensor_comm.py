'''
SCRIPT FOR READING SPEC SENSOR DATA
Datasheet has the following commands (ASCII). The sensor can be interface with 
Any other open serial terminal like Putty to test these commands 
1. Zero Sensor = 'Z' This zeroes the sensor (ie recalibrates the sensor to assume 0ppm of ambient gas concentration)
2. Read Memory = 'e' This reads the sensor parameters that are stored in the sensor's EEPROM. Some of these fields are dynamic
3. Single Shot Transmission = '\r'  This transmits a single sensor measurements to the terminal 
4. Continuous Transmission = 'c' This automatically transmits sensor measurements every second
4. Average Parameter = 'A' This command allows a change to the averaging parameter  which  sets value of averaged samples per unit time
5. Reset Sensor = 'r' This command resets the 
'''

# python packages
import serial
import time
# our methods
import port_scanner # scans for all usb device which are connected to laptop

# the method returns a tuple of the usb devices connected and how many there are
usb_device_list, num_of_devices = port_scanner.scan_usb_ports()

# determine comm ports of each sensor
sensor_port = []

for i in range (num_of_devices):
    current_device = usb_device_list[i]["device_description"]
    current_device = current_device.split(" (") # strip any comm port info at the end of the string
    if (current_device[0] == 'Silicon Labs CP210x USB to UART Bridge'):
        sensor_port.append(usb_device_list[i]["device_name"]) # add the comm port of sensor to the list "sensor_port"
    else:
        continue

num_sensors = len(sensor_port) # number of sensors plugged in

# now we know which ports have a sensor. open a communication link for each individual sensor

# this functions purpose is to poll all sensors which are currently 
def poll_sensor_data(sensor_command):
    continue

def user_input():
    continue

