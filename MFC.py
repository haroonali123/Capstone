import serial
import time

class MFC_device:
    
    def __init__(self, comPort):
        self.port = serial.Serial(port=comPort, baudrate=9600, bytesize=8 , timeout=.1, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE )
        
    def setFlowRate(self, port, value):
        cmd = 'AZ.' + port + 'P01=' + value + '\r'
        self.port.write(cmd.encode())
        response = self.port.readline()
        #print(response)

    def getFlowRate(self, port):
        cmd = 'AZ.' + port + 'P01?\r' 
        self.port.write(cmd.encode())
        time.sleep(0.5)
        response = (self.port.readline().decode()).split(",")[4]
        return response


   
