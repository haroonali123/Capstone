'''
SAMPLE SCRIPT FOR READING SPEC SENSOR DATA
Please refer to the datasheet for the following commands (ASCII). The sensor can be interface with 
any other open serial terminal like Putty to test these commands 
1. Zero Sensor = 'Z' This zeroes the sensor (ie recalibrates the sensor to assume 0ppm of ambient gas concentration)
2. Read Memory = 'e' This reads the sensor parameters that are stored in the sensor's EEPROM. Some of these fields are dynamic
3. Single Shot Transmission = '\r'  This transmits a single sensor measurements to the terminal 
4. Continuous Transmission = 'c' This automatically transmits sensor measurements every second
4. Average Parameter = 'A' This command allows a change to the averaging parameter  which  sets value of averaged samples per unit time
5. Reset Sensor = 'r' This command resets the 
'''

from serial import Serial #Install this module via PIP (added to your global path)
from time import sleep 

###################################################################################
#Initialize the serial interface here (The value of all enumerated USB on the hub)
port=["/dev/ttyUSB0",] #This enumeration is dynamically generated. You can write a snippet of code to capture all of these and create instances. 
serialports=[] #create a list to hold all enumerated USB port values
serial0=Serial(port=port[0], baudrate=9600, timeout=5) #write reiterative code to generate serial instances with parameters
serialports.append(serial0)
###################################################################################
try:
    command='x'
    commandlist = "Zero Sensor='z'\r\nRead Memory='e'\r\nSingle Shot='Enter Key'\r\nSet Average='A'\r\nContinuous Mode='c'\r\nReset Sensor='r'\r\n"
    
    while True:
        command=input('Enter Command: ')
        if command is 'q':
            try:
                for serialport in serialports: serialport.close()
                exit() #a program exit command 
            except Exception as serClose:
                print(serClose.args)  
        if command is 'z':
            for serialport in serialports: #iterate through all available serial ports 
                serialport.write(command.encode()) #write the command to the serial port
                print(serialport.readline().decode('utf-8', errors='replace').replace('\x00', '')) #read and discard output prompt from sensor
        elif command is 'e':
            for serialport in serialports:
                serialport.write(command.encode())
                for linenumber in range(0, 20): print(serialport.readline().decode('utf-8', errors='replace').replace('\x00', '')) #the sensor outputs varying number of line texts, so it must be ranged accordingly
        elif command is '\r':
            for serialport in serialports:
                serialport.write(command.encode())
                print(serialport.readline().decode('utf-8', errors='replace').replace('\x00', ''))
        '''
except Exception as serialEx:
    print(serialEx.args)