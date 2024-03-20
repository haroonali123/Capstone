

import serial
import Experiment
import time

#################################################################################################################################################
# Thermotron class Definition
#################################################################################################################################################


class Thermotron:

    def __init__(self, comPort):
        
        self.write_delay = 0.2                         # Minimum time needed between writes

        #Define serial port to communicate with the thermotron
        #Baudrate, bytesize and parity all defined by dip switch position (Timeout can be tweaked)

        self.port = serial.Serial(port = comPort, baudrate = 9600, bytesize = 8, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, timeout = 0.5)

        self.temp = 0                     # Temperature and humidity values
 
        self.humidity = 0

        self.operatingmode = 0

        self.getStatus()

    
    def manualCommands(self):             # Infinitely process and send commands from the command line to the thermotron then read the response
        
        while True:

            print("-"*70)
            cmd = input("Enter command here: ")
            print("")
            self.write_command(cmd)
            response = self.read_response()

#################################################################################################################################################
#  Temperature and Humidity Commands
#################################################################################################################################################

    def getTemperature(self):
        
        cmd = 'DTV'
        self.write_command(cmd)
        self.temp = float(self.read_response())


    def getHumidity(self):
        
        cmd = 'DRV'
        self.write_command(cmd)
        self.humidity = float(self.read_response())

    def setTemperature(self, value):
        cmd = 'LTS' + str(value) + '\r\n'
        self.port.write(cmd.encode())

    def setHumidity(self, value):

        cmd = 'LRS' + str(value) + '\r\n'
        self.port.write(cmd.encode())



#################################################################################################################################################
#  Information commands
#################################################################################################################################################

    def getStatus(self):

        cmd = 'DST'
        self.write_command(cmd)
        response = int(self.read_response())

        mask = 0b00000111                     #Mask the rest of the status byte to only get operating condition relevant bits

        self.operatingmode = response & mask  #Mask and store the operating condition (as an integer)

        # 0 = STOP, 2 = Run manual, 3 = Run Program

    def getInterval(self):
        
        cmd = 'DIN'
        self.write_command(cmd)
        self.interval = int(self.read_response())

    def getIntervalTime(self):
        
        cmd = 'DIT'
        self.write_command(cmd)
        self.intervaltime = int(self.read_response())

    def getIntervalTimeLeft(self):

        cmd = 'DTL'
        self.write_command(cmd)
        self.intervaltimeleft = self.read_response()


#################################################################################################################################################
# Control commands
#################################################################################################################################################

    def run_manual(self, temp, humidity):   #Runs in manual until given setpoints are reached
        
        self.stop()

        self.getStatus()
        if self.operatingmode == 0:

            self.write_command("RM")                     #Place thermotron in run manual mode

        self.getStatus()
        if self.operatingmode == 2:

            self.setTemperature(temp)                  #Set both setpoints to desired values
            self.setHumidity(humidity)

        self.getTemperature()
        self.getHumidity()

        while self.temp != temp and self.humidity != humidity:  

            self.getTemperature()        #Constantly poll for temperature and humidity until its within +/- 1 deg celsius of temp target and +/- 3 percent of humidity target
            self.getHumidity()
            print("Temperature is: " + str(self.temp))


        
        self.stop()


    def run_experiment(self, program_number):

        if isinstance(program_number, int):         #Run a single experiment
        

            program = Experiment.Experiment(program_number)                  #Access specified program from CSV
            self.write_program(program.command)                              #Write the program to the thermotron
            
            self.current_program = program_number    #Set the current program number

            self.run_manual(program.intervals[0]["temp"], program.intervals[0]["humidity"])  #Runs the thermotron (in manual) to the initial setpoints 


            run_program_cmd = "RP" + str(program_number) #Run Given program number
            self.write_command(run_program_cmd)

            

            self.interval = 1  #Set initial interval

            self.getStatus()
            print("-"*72)
            print("Starting program number: " + str(program_number) + '\n')
            
            while(self.operatingmode == 3):      #While program is running constantly poll for information

                    self.poll_experiment()
                    print("Current Interval: " + str(self.interval))
                    print("Current Temperature: " + str(self.temp))
                    print("Current Humidity: " + str(self.humidity))
                    print("Time left in interval: " + str(self.intervaltimeleft) + '\n')

            print("Program Complete\n")

            self.stop()
        else:                                      #Run a sequence of experiments

            for program in program_number:

                self.run_experiment(program)
            

    def poll_experiment(self):       #Poll various data during experiment

        self.getTemperature()
        self.getHumidity()
        self.getIntervalTimeLeft()
        self.getStatus()
        self.getInterval()

    def stop(self):

        cmd = 'S' + '\r\n'
        self.port.write(cmd.encode())


    
#################################################################################################################################################
# Read and Write Commands
#################################################################################################################################################

    def write_command(self, command):
        
        #print("Writing " + command + " to Thermotron\n")
        
        word = command + '\r\n'                        #Add mesage terminator
        word_bytes = word.encode('ascii')                  #Convert to ASCII bytes
        self.port.write(word_bytes)                                           #Write data to Thermotron
        time.sleep(self.write_delay)
        
    
    def read_response(self):
        
        response_bytes = self.port.readline()                                 #Read bytes from thermotron (Readline reads until it sees \n or timesout based on port timeout value)
        response_text = response_bytes.decode('ascii')     #Decode from ASCII bytes to string
        response = response_text.replace('\r\n', '')   #Remove message terminator

        """if response == "":                                                    #Notify user if nothing was received within the timeout window

            print("No Response received\n")
            
        else:                                                                 #Print message received from thermotron
            
            print("Received " + response + " from Thermotron\n")"""

        return response

    def write_program(self, command_list):                  #Write a list of commands (individual program entries)
        
        print("Writing program to Thermotron...")

        for command in command_list:                                   #Send commands to thermotron to write program
            
            self.write_command(command)

        print("Done writing program\n")