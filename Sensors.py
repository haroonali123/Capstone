import serial
import time
import os
from datetime import datetime

class Sensors:
    
    def __init__(self, comm_port, file_path = None):
        self.port = serial.Serial(port=comm_port, baudrate=9600, bytesize=8 , timeout=.1, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE )
        self.file_path = file_path
        if self.file_path != None:
            self.file_name = os.path.join(file_path, ("sensor_data_" + str(comm_port)))
    
    def write_or_print(self, num_lines):
        if self.file_path == None:
            for line in range(num_lines):
                print(self.port.readline().decode())
        else:
            with open(self.file_name, 'a') as file:
                file.write("Current Time = {}, ".format(datetime.now()))      
                for line in range(num_lines):
                    file.write(self.port.readline().decode())
        pass

    # this function allows for sensor to be "zeroed" after being unpowered for an extended duration 
    def reCalibrate(self):
        command = "Z"
        self.port.write(command.encode())
        self.write_or_print(3)
        
    # this function returns a single measurement from the sensor
    def singleMeasurement(self):
        command = "\r"
        self.port.write(command.encode())
        self.write_or_print(1)
            
    # this function continuously outputs data to the terminal. press "c" to exit
    def continuousData(self):
        command = "c"
        self.port.write(command.encode())
    
    def e_command(self):
        command = "e"
        self.port.write(command.encode())
        self.write_or_print(15)    
    
#my_sensor = Sensors("COM3", os.getcwd())
# my_sensor.e_command()
#my_sensor.singleMeasurement()