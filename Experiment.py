
import csv

class Experiment:
    
#################################################################################################################################################
# Create and delete Object
#################################################################################################################################################
    
    def __init__(self, program_number):  

        file_address = "profiles.csv"

        self.number = program_number #set program number
        
        self.intervals = []           #Create empty interval array
        
        self.interval_count = 0

        program = []

        with open(file_address, 'r') as file:
            
            program_csv = csv.reader(file)
        
        # Order for CSV = Profile #1 ,Flow rate 1, Flow rate 2, Flow rate 3, Flow rate 4, Initial Temp, initial humidity, Interval 1: Final Temp, Final humidity, Hours, Minutes, Interval 2: ......)

            for row in program_csv:     #Iterate through each row of CSV

                if int(row[0][-1]) == program_number:  #Iterate until requested program is found
                    
                    program = row


        if program == []:                      #Check to make sure program isn't blank
            
            print("Empty Program found")

        else:

            for i in range(len(program)):   #Replace "" blank entries with 0
                
                if program[i] == "":

                    program[i] = 0

            self.intervals.append({"FR1": float(program[1]), "FR2": float(program[2]), "FR3": float(program[3]), "FR4": float(program[4]), "temp" : float(program[5]), "humidity": float(program[6])}) #Initial Interval

            
            
            for i in range(7, len(program), 4):  # Do one loop per interval (Each data entry is one of 4 per interval, starting at 6 to ignore the intial 6 for the initial interval)

                self.intervals.append({"temp" : float(program[i]), "humidity": float(program[i + 1]), "hour" : int(program[i + 2]), "minute" : int(program[i + 3])})

                self.interval_count = self.interval_count + 1  #Count number of intervals for command creation

            self.create_command()  #Create Command



#################################################################################################################################################
# Command generation and editing for thermotron
#################################################################################################################################################

    def create_command(self):
        
        self.command = []
        self.command.append("LPM" + str(self.number) + "," + str(self.interval_count) + ",V")           #LPMp,i,V command as defined in manual (prepares Thermotron to read program from PC)

        for i in range(self.interval_count + 1):                                

            if i == 0:                                                                   #Interval 0 command

                self.command.append("LPI" + str(i) + "," + str(self.intervals[i]["temp"]) + "," + str(self.intervals[i]["humidity"]))

            else:                                                                        #All remaining interval commands

                if self.intervals[i]["hour"] == 0 and self.intervals[i]["minute"] == 0:                          #Guaranteed soak intervals (defined in manual), adds deviation parameter of 1 deg C for temp and 3% for humidity

                    self.command.append("LPI" + str(i) + "," + str(self.intervals[i]["temp"]) + "," + str(self.intervals[i]["humidity"]) + ",," + str(int(self.intervals[i]["hour"])) + "," + str(int(self.intervals[i]["minute"])) + ",,,,,,1,3")

                else:                                                                                            #Normal ramp based intervals (no deviation parameter)
                    self.command.append("LPI" + str(i) + "," + str(self.intervals[i]["temp"]) + "," + str(self.intervals[i]["humidity"]) + ",," + str(int(self.intervals[i]["hour"])) + "," + str(int(self.intervals[i]["minute"])))
        
        return self.command