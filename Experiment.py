
import csv

class Experiment:
    
#################################################################################################################################################
# Create and delete Object
#################################################################################################################################################
    
    def __init__(self, program_number):  

        file_address = "programs.csv"
        
        self.number = program_number  #Set program number
        
        self.intervals = []           #Create empty interval array

        with open(file_address, 'r') as file:
            
            program_csv = csv.reader(file)

        # Order for CSV = Program #, Flow rate 1, Flow rate 2, Flow rate 3, Flow rate 4, Initial Temp, initial humidity, Interval 1: Final Temp Final humidity Hours Minutes, Interval 2: ......)

            i = 0

            for row in program_csv:     #Iterate through each row of CSV

                i = i + 1

                if i == program_number:  #Execute when the target program is found
                     
                    program_raw = [data for data in row if data not in ""]   #Remove all blank entries

                    program = [float(data) for data in program_raw]        #Create list of floats from row in CSV corresponding to target program


        if program == []:                      #Check to make sure program isn't blank
            
            print("Empty Program found")

        else: 
            self.intervals.append({"FR1": program[0], "FR2": program[1], "FR3": program[2], "FR4": program[3], "temp" : program[4], "humidity": program[5]}) #Initial Interval

            self.interval_count = 0

            for i in range(6, len(program), 4):  # Do one loop per interval (Each data entry is one of 4 per interval, starting at 6 to ignore the intial 6 for the initial interval)
                
                self.intervals.append({"temp" : program[i], "humidity": program[i + 1], "hour" : program[i + 2], "minute" : program[i + 3] })

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

#################################################################################################################################################
# Legacy code
#################################################################################################################################################
    
    """def print_intervals(self):
        

        for i in range(self.interval_count + 1):                          #Print out interval values

            if i == 0:
                print("Program number " + str(self.number) + "\n")
                print("-"*72)
                print("Interval " + str(i) + "\n")
                print("Initial Temp = " + str(self.intervals[i]["temp"]) + '\n')
                print("Intiial Humidity = " + str(self.intervals[i]["humidity"]) + '\n')


            else:
                print("-"*72)
                print("Interval " + str(i) + "\n")
                print("Final Temp = " + str(self.intervals[i]["temp"]) + '\n')
                print("Final Humidity = " + str(self.intervals[i]["humidity"]) + '\n')
                print("Hours = " + str(self.intervals[i]["hour"]) + '\n')
                print("Minutes = " + str(self.intervals[i]["minute"]) + '\n')
            
        print("-"*72)

    def remove_interval(self, index):
        
        if index > self.interval_count or index < 0:
            
            print("Index out of range")


        elif index == 0:                                    #Not allowed to remove initial interval
            
            print("Cannot remove initial interval")


        else:
            self.interval_count = self.interval_count - 1        #Decrement the count of intervals

            self.intervals.pop(index)                     #Remove the specified interval

            self.create_command()                                #Re-create the command


    def add_interval(self, index, temp, humidity, fr1 = None, fr2 = None, fr3 = None, fr4 = None, hour = None, minute = None):

        if index > self.interval_count + 1 or index < 0:

            print("Index out of range")


        elif index == 0:                                   #Replace initial interval (can only have one with 2 parameters)
            
            self.intervals[0] = {"FR1": fr1, "FR2": fr2, "FR3": fr3, "FR4": fr4, "temp" : temp, "humidity": humidity}    
            self.create_command()                                #Re-create the command

        
        elif hour != None and minute != None:
            
            self.interval_count = self.interval_count + 1        #Increment the count of intervals

            self.intervals.insert(index, {"temp" : temp, "humidity": humidity, "hour" : hour, "minute" : minute })      #Insert new interval        
            self.create_command()                                #Re-create the command



    def replace_interval(self, index, temp, humidity, fr1 = None, fr2 = None, fr3 = None, fr4 = None, hour = None, minute = None):

        if index > self.interval_count or index < 0:

            print("Index out of range")
        

        elif index == 0:                               #Replace initial interval (can only have one with 2 parameters)
            
            self.intervals[0] = {"FR1": fr1, "FR2": fr2, "FR3": fr3, "FR4": fr4, "temp" : temp, "humidity": humidity}     
            self.create_command()                                #Re-create the command

        
        else:                                                #Replace any other non initial interval
            
            self.intervals[index] = {"temp" : temp, "humidity": humidity, "hour" : hour, "minute" : minute }                 
            self.create_command()                                #Re-create the command

    def cmdlinecreate(self):
        
        self.number = int(input("Enter profile number: "))           #Set profile ID number and amount of intervals

        self.interval_count = int(input("Enter number of intervals: "))
                

        for i in range(self.interval_count + 1):        #Creates a list of dictionaries storing each interval, Overall list stores entries of dictionaries which hold interval data (1 list entry = 1 dictionary = 1 interval (with defined parameters))
                    
            print("-"*72)
            print("Enter values for interval number " + str(i) + "\n")

            if i == 0:                                                  #Load dictionary for initial interval (interval 0)

                fr1 = int(input("Enter flow rate 1: "))
                fr2 = int(input("Enter flow rate 2: "))
                fr3 = int(input("Enter flow rate 3: "))
                fr4 = int(input("Enter flow rate 4: "))

                temp = int(input("Enter Initial Temperature: "))  
                humidity = int(input("Enter Initial Humidity: "))

                self.intervals.append({"FR1": fr1, "FR2": fr2, "FR3": fr3, "FR4": fr4, "temp" : temp, "humidity": humidity})


            else:

                temp = int(input("Enter final Temperature: "))          #Load dictionary for all other intervals
                humidity = int(input("Enter final Humidity: "))
                hour = int(input("Enter amount of hours: "))
                minute = int(input("Enter amount of minutes: "))

                self.intervals.append({"temp" : temp, "humidity": humidity, "hour" : hour, "minute" : minute })

        self.create_command()                                           #Create list of commands to send to thermotron


    def delete(self):
        
        del self                                            #Delete experiment"""