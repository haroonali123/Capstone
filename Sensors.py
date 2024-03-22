import serial
import time

class Sensors:
    
    def __init__(self, comm_port):
        self.port = serial.Serial(port=comm_port, baudrate=9600, bytesize=8 , timeout=.1, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE )

    # this function allows for sensor to be "zeroed" after being unpowered for an extended duration 
    def reCalibrate(self):
        command = "Z"
        self.port.write(command.encode())
        for line in range(3):
            print(self.port.readline().decode()) #read and discard output prompt from sensor

    # this function returns a single measurement from the sensor
    def singleMeasurement(self):
        command = "\r"
        self.port.write(command.encode())
        for line in range(3):
            print(self.port.readline().decode())
            
    # this function continuously outputs data to the terminal. press "c" to exit
    def continuousData(self):
        command = "c"
        self.port.write(command.encode())
    
