import Thermotron
import Experiment

thermotron = Thermotron.Thermotron('com3')   #Initialize Thermotron object

program_list = [2,5]     #Define program queue
program_queue = [Experiment.Experiment(program) for program in program_list] #Create list of program objects

for program in program_queue:  #Cycle through each program

    print("-"*72)
    print("Starting Program number: " + str(program.number) + '\n')

    thermotron.stop()

    initial_temp = program.intervals[0]["temp"]
    initial_humidity = program.intervals[0]["humidity"]

    print("Manually running until initial temperatures\n")

    thermotron.run_manual(initial_temp, initial_humidity)   #Start running in manual with initial SP's defined in program

    while thermotron.getStatus() == 2:         #While in manual, Poll temp and humidity

        if thermotron.temp != initial_temp: #or thermotron.humidity != initial_humidity:  

                thermotron.getTempandHumidity()
                print("Temperature is: " + str(thermotron.temp))
                #print("Humidity is: " + str(thermotron.humidity))

        else:                                   #Once both SP's are reached stop Thermotron
            thermotron.stop()

    print("-"*72)
    print("Starting program\n")

    thermotron.run_program(program.number)      #Run desired progam

    while(thermotron.operatingmode == 3):      #While program is running constantly poll for information

        thermotron.poll_experiment()
        print("Current Interval: " + str(thermotron.interval))
        print("Current Temperature: " + str(thermotron.temp))
        print("Current Humidity: " + str(thermotron.humidity))
        print("Time left in interval: " + str(thermotron.intervaltimeleft) + '\n')

    thermotron.stop() #Stop thermotron once program is done
    print("Program Done")