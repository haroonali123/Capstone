import Thermotron
import Experiment

thermotron = Thermotron.Thermotron('COM3')   #Initialize Thermotron object

program_list = [2,3]     #Define program queue
program_queue = [Experiment.Experiment(program) for program in program_list] #Create list of program objects

for program in program_queue:  #Cycle through each program

            print("-"*72)                                                        
            print("Starting Program number: " + str(program.number) + '\n')

            thermotron.stop()                                                    #Place in stop initially

            initial_temp = program.intervals[0]["temp"]                          #Set initial temperature and humidity
            initial_humidity = program.intervals[0]["humidity"]

            print("Manually running until initial temperature: " + str(initial_temp) + '\n')
            print("Manually running until initial humidity: " + str(initial_humidity) + '\n')

            thermotron.run_manual(initial_temp, initial_humidity)   #Start running in manual with initial SP's defined in program

            setpoint_ok_count = 0

            while (thermotron.operatingmode == 2 or thermotron.operatingmode == 4) and setpoint_ok_count < 200:  #While in manual/hold and setpoints have not been reached for 100 ticks
                
                if thermotron.operatingmode == 2:         #Don't poll while it's in hold (but stay in while loop)

                    thermotron.getStatus()
                    thermotron.getTempandHumidity()
                    print("Temperature is: " + str(thermotron.temp))
                    #print("Humidity is: " + str(thermotron.humidity))

                    if (thermotron.temp < initial_temp - 1 or thermotron.temp > initial_temp + 1): #or thermotron.humidity != initial_humidity:  
                        
                        setpoint_ok_count = 0  #Reset count if temp/humidity are out of setpoint bounds
                    else:
                        setpoint_ok_count = setpoint_ok_count + 1 #Increment count if temp/humidity is within bounds
                        print("Temperature within range")
            
            if thermotron.GUI_stop_request == True:               #Break out of schedule if stop button is hit

                thermotron.GUI_stop_request == False
                print("Program stopped by GUI\n")
                break

            thermotron.stop()  

            print("-"*72)
            print("Starting program number " + str(program.number))
            
            thermotron.write_program(program.command)
            thermotron.run_program(program.number)      #Run desired progam

            while(thermotron.operatingmode == 3 or thermotron.operatingmode == 4):      #While program is running/hold constantly poll for information
                
                if(thermotron.operatingmode == 3):      #Dont poll while its in hold but stay in while loop
                    
                    
                    #sensor1.singleMeasurement()
                    #sensor2.singleMeasurement()
                    thermotron.poll_experiment()

                    print("Current Interval: " + str(thermotron.interval))
                    print("Current Temperature: " + str(thermotron.temp))
                    print("Current Humidity: " + str(thermotron.humidity))
                    print("Time left in interval: " + str(thermotron.intervaltimeleft) + '\n')

            if thermotron.GUI_stop_request == True:        #Break out of schedule if stop button is hit

                thermotron.GUI_stop_request == False
                print("Program stopped by GUI\n")
                break

            thermotron.stop() #Stop thermotron once program is done
            print("Program Done")