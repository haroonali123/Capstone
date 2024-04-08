import Thermotron
import Experiment
import datetime
import csv

thermotron = Thermotron.Thermotron('COM3')   #Initialize Thermotron object
thermotron.write_read_manual()
program_list = [4,3]     #Define program queue
program_queue = [Experiment.Experiment(program) for program in program_list] #Create list of program objects


flow_rate1 = 0
flow_rate2 = 0
flow_rate3 = 0
flow_rate4 = 0

try:
    for program in program_queue:
                
                try:
                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
                    file_path = "./Thermotron_data/Thermotron_data_" + current_datetime + "_Program_Number_"+ str(program.number) + ".csv"

                    first_row = ["Started on:", current_datetime, "Program #:", program.number, "Flow Rate 1:", flow_rate1, "Flow Rate 2:", flow_rate2, "Flow Rate 3:", flow_rate3, "Flow Rate 4:", flow_rate4]
                    headers = ["Interval #", "Time in Interval", "Temperature", "Humidity"]

                    file = open(file_path, mode='a', newline='')

                    writer = csv.writer(file)

                    writer.writerow(first_row)   #Write first row containing information thats constant throughout a program
                    writer.writerow(headers)     #Write the headers for the data
                    writer.writerow("")
                        

                    print("-"*72)                                                        
                    print("Starting Program number: " + str(program.number) + '\n')

                    thermotron.stop()                                                    #Place in stop initially

                    thermotron.write_program(program.command)                            #Write program to Thermotron

                    initial_temp = program.intervals[0]["temp"]                          #Set initial temperature and humidity
                    initial_humidity = program.intervals[0]["humidity"]

                    print("Manually running until initial temperature: " + str(initial_temp) + '\n')
                    print("Manually running until initial humidity: " + str(initial_humidity) + '\n')

                    start_time = datetime.datetime.now()
                        
                    thermotron.run_manual(initial_temp, initial_humidity)   #Start running in manual with initial SP's defined in program

                    setpoint_ok_count = 0
                    setpoint_ok_max = 1500

                    while (thermotron.operatingmode == 2) and setpoint_ok_count < setpoint_ok_max:  #While in manual/hold and setpoints have not been reached for 100 ticks
                            
                        thermotron.getStatus()
                        thermotron.getTempandHumidity()
                        print("Temperature is: " + str(thermotron.temp))
                        #print("Humidity is: " + str(thermotron.humidity))

                        if (thermotron.temp < initial_temp - 1 or thermotron.temp > initial_temp + 1): #or (thermotron.humidity < initial_humidity - 1 or thermotron.humidity > initial_humidity + 1:  
                                    
                            setpoint_ok_count = 0  #Reset count if temp/humidity are out of setpoint bounds
                                
                        else:
                            print("Setpoint ok, tick " + str(setpoint_ok_count) + "/" + str(setpoint_ok_max) + '\n')
                            setpoint_ok_count = setpoint_ok_count + 1 #Increment count if temp/humidity is within bounds
                        
                    if thermotron.GUI_stop_request == True:               #Break out of schedule if stop button is hit

                        thermotron.GUI_stop_request == False
                        print("Program stopped by GUI\n")
                        break

                    end_time = datetime.datetime.now()

                    print("Manual run took: " + str(end_time - start_time) + '\n')
                    print("-"*72)
                    print("Starting program number " + str(program.number))
                        
                    thermotron.stop_run_program(program.number)      #Stop, then run selected program
                    thermotron.getStatus()
                        
                        
                    while(thermotron.operatingmode == 3 or thermotron.operatingmode == 4):      #While program is running/hold constantly poll for information
                            
                        if(thermotron.operatingmode == 3):      #Dont poll while its in the Hold but stay in while loop
                                
                            
                            thermotron.poll_experiment()
                                
                            writer.writerow([thermotron.interval], [thermotron.intervaltimetotal - thermotron.intervaltimeleft], thermotron.temp, thermotron.humidity)
                            
                            print("Current Interval: " + str(thermotron.interval))
                            print("Current Temperature: " + str(thermotron.temp))
                            print("Current Humidity: " + str(thermotron.humidity))
                            print(str(thermotron.intervaltimetotal - thermotron.intervaltimeleft) + "out of " + str(thermotron.intervaltimetotal) + " minutes\n")

                    if thermotron.GUI_stop_request == True:        #Break out of schedule if stop button is hit

                        thermotron.GUI_stop_request == False
                        print("Program stopped by GUI\n")
                        break

                    thermotron.stop() #Stop thermotron once program is done

                    file.close()
                    print("Program Completed without Error")

                finally:
                    print("Program Stopped by error")
                    file.close()

except KeyboardInterrupt:
     print("Program stopped by command line")