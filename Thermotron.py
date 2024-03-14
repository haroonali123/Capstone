import serial

class Thermotron:

    def init(self, comPort):
        self.port = serial.Serial(port=comPort, baudrate=9600, bytesize=8 , timeout=.1, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE )

    def setTemperature(self, port, value):
        cmd = 'LTS' + value + '\r\n'
        self.port.write(cmd.encode())
        response = self.port.readline()
        print(response)

    def setHumidity(self, port, value):
        cmd = 'LRS' + value + '\r\n'
        self.port.write(cmd.encode())
        response = self.port.readline()
        print(response)

    def getTemperature(self, port):
        cmd = 'DTV' + '\r\n'
        self.port.write(cmd.encode())
        response = self.port.readline()
        print(response)

    def getHumidity(self, port):
        cmd = 'DTS' + '\r\n'
        self.port.write(cmd.encode())
        response = self.port.readline()
        print(response)
