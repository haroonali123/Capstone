

import serial
import time

#################################################################################################################################################
# Thermotron class Definition
#################################################################################################################################################

class Thermotron:

    def __init__(self, comPort):
        
        self.write_delay = 0.2         # Minimum time needed between writes

        #Define serial port to communicate with the thermotron
        #Baudrate, bytesize and parity all defined by dip switch position (Timeout can be tweaked)

        self.port = serial.Serial(port = comPort, baudrate = 9600, bytesize = 8, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, timeout = 0.5)

        self.temp = 0                    #Current Temperature and humidity values
 
        self.humidity = 0

        self.operatingmode = 0           #Operating mode variable
        
        self.stop_comms = False          #Variable to prevent collisions on serial communication when using GUI

        self.GUI_stop_request = False    #Used to stop program from GUI

#################################################################################################################################################
#  Set humidity and Temperature
#################################################################################################################################################

    def setTemperature(self, value):          
        
        if self.stop_comms == False:

            cmd = 'LTS' + str(value)
            self.write_command(cmd)

    def setHumidity(self, value):

        if self.stop_comms == False:

            cmd = 'LRS' + str(value)
            self.write_command(cmd)

#################################################################################################################################################
#  Information commands
#################################################################################################################################################

    def getStatus(self):

        if self.stop_comms == False:

            cmd = 'DST'
            self.write_command(cmd)
            response = int(self.read_response())

            mask = 0b00000111                     #Mask the rest of the status byte to only get operating condition relevant bits

            self.operatingmode = response & mask  #Mask and store the operating condition (as an integer)

            # 0 = STOP, 2 = Run manual, 3 = Run Program, 4 = Hold Program

            return self.operatingmode

#################################################################################################################################################
# Polling Commands
#################################################################################################################################################

    def poll_experiment(self):       #Poll various data during experiment
        
        if self.stop_comms == False:

            self.write_command(['DTV', 'DRV', 'DIN', 'DTL', 'DST']) #Send all 5 Commands in one line
            response = self.read_response(5)                        #Read all 5 individual responses

            self.temp = float(response[0])            #Assign all requested variables
            self.humidity = float(response[1])
            self.interval = int(response[2])
            self.intervaltimeleft = response[3]
            
            #Mimic Get status method
            response = int(response[4])
            mask = 0b00000111                     
            self.operatingmode = response & mask  
            

    def getTempandHumidity(self):
        
        if self.stop_comms == False:

            self.write_command(['DTV', 'DRV'])
            response = self.read_response(2)
            self.temp = float(response[0])
            self.humidity = float(response[1])

#################################################################################################################################################
# State control commands
#################################################################################################################################################

    def GUI_Request(self, command):

        self.stop_comms = True               #Stop other commands sent to the thermotron
        
        time.sleep(0.5)                      #Delay to stop read/writes

        if command == "STOP":
            
            self.GUI_stop_request = True
            cmd = 'S'
            self.write_command(cmd)
            self.operatingmode = 0
        
        elif command == "HOLD":
            
            cmd = "H"
            self.write_command(cmd)    
            self.operatingmode = 4
                 

        elif command == "RUN":
            
            cmd = "R"
            self.write_command(cmd)
            self.operatingmode = 3
                     
        else:
            print("Invalid command")
        
        self.stop_comms = False       #Reset the GUI request variable

    def stop(self):                   #Put the thermotron into stop
        
        if self.stop_comms == False:
            
            cmd = 'S'
            self.write_command(cmd)
            self.getStatus()


    def run_program(self, program_number):

        if self.stop_comms == False:

            cmd = "RP" + str(program_number) #Run Given program number
            self.write_command(cmd)
            self.getStatus() 

    def stop_run_program(self,program_number):

        if self.stop_comms == False:

            cmd = ["S", "RP" + str(program_number)] #Run Given program number
            self.write_command(cmd)

    def run_manual(self, temp, humidity):
        
        if self.stop_comms == False:

            cmd = "RM"
            self.write_command(cmd)                     #Place thermotron in run manual mode
            self.getStatus() 

        self.setTemperature(temp)                       #Set both setpoints to desired values
        self.setHumidity(humidity)

    def run(self):

        if self.stop_comms == False:

            cmd = "R"
            self.write_command(cmd)                     #Place the thermotron in run, AFTER holding a program
            self.getStatus() 

    def hold(self):

        if self.stop_comms == False:

            cmd = "H"
            self.write_command(cmd)                     #Place thermotron in hold mode
            self.getStatus() 
        
#################################################################################################################################################
# Read and Write Commands
#################################################################################################################################################

    def write_command(self, command):

        if isinstance(command, list): #Concatenate a list of commands into one

            word = ''

            for entry in command:         #Concatenate commands
                
                word = word + entry + ';'

            word = word[:-1]              #Strip final ";" character

            word = word + '\r\n'                               #Add terminator
            word_bytes = word.encode('ascii')                  #Convert to ASCII bytes
            self.port.write(word_bytes)                        #Write data to Thermotron
            time.sleep(self.write_delay)

        else:         #Write a single command

            word = command + '\r\n'                        #Add mesage terminator
            word_bytes = word.encode('ascii')              #Convert to ASCII bytes
            self.port.write(word_bytes)                    #Write data to Thermotron
            time.sleep(self.write_delay)


    def write_program(self, command_list):                  #Write a list of commands (individual program entries)
        
        if self.stop_comms == False:

            print("Writing program to Thermotron...")

            for command in command_list:                    #Send commands to thermotron to write program
                
                self.write_command(command)

            print("Done writing program\n")


    def read_response(self, multiple = 0, print_text = False):
        
        if multiple == 0:    #Read once

            response_bytes = self.port.readline()                      #Read bytes from thermotron (Readline reads until it sees \n or timesout based on port timeout value)
            response_text = response_bytes.decode('ascii')             #Decode from ASCII bytes to string
            response = response_text.replace('\r\n', '')               #Remove message terminator
            
            if print_text == True:

                if response == "":                                     #Notify user if nothing was received within the timeout window

                    print("No Response received\n")
                    
                else:                                                  #Print message received from thermotron
                    
                    print("Received " + response + " from Thermotron\n")
        
        else:                                                          #Read multiple times and return a list of responses
            response = []

            for i in range(multiple):
                
                response.append(self.read_response())
            
        return response