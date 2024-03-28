import tkinter as tk
import MFC
from page import Page
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import Thermotron
import Experiment
import threading
import port_scanner
import Sensors
import os

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #self.showProfiles()
        self.profileList = []
        self.dataFrame = tk.Frame(self)
        self.plotFrame = tk.Frame(self)
        self.queueFrame = tk.Frame(self)
        self.resetQueueFrame = tk.Frame(self)
        self.runFrame = tk.Frame(self)

        self.runQueue = []

        queue_label = tk.Label(self, text = 'Queue: ', font=('calibre',10, 'bold'))
        queue_label.pack(side='top')

        self.queueFrame.pack(side='top')
        self.resetQueueFrame.pack(side='top')
        
        resetQueueButton = tk.Button(self.resetQueueFrame, command=self.resetQueue, text = 'Reset')
        resetQueueButton.pack(side='top')

        self.t1 = threading.Thread(target=self.run, daemon=True)
        #t1.start()
        
    
    def showProfileButtons(self):
        #f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Projects\\Capstone\\Capstone\\profiles.csv", 'r')
        f = open("profiles.csv", 'r')

        profiles = f.readlines()
        f.close()
        
        for profile in profiles:
            
            data = profile.split(",")

            if(data[0] in self.profileList):
                continue
            
            profileFrame = tk.Frame(self)
            profileFrame.pack(side="top", fill="x")

            profileButton = tk.Button(profileFrame,command=lambda arg = data[0] : self.showProfile(arg),text = data[0])
            profileButton.pack(side="top", fill="x")

            self.profileList.append(data[0])
        
        self.dataFrame.pack(side='left')
        self.plotFrame.pack(side='left')
        self.runFrame.pack(side='bottom', fill='x')


    
    def clear_dataFrame(self):
        for widgets in self.dataFrame.winfo_children():
            widgets.destroy()
    
    def clear_plotFrame(self):
        for widgets in self.plotFrame.winfo_children():
            widgets.destroy()
    
    def clear_queueFrame(self):
        for widgets in self.queueFrame.winfo_children():
            widgets.destroy()

    def addToQueue(self, profileName):
        profileLabel = tk.Label(self.queueFrame, text = profileName[0], font=('calibre',10, 'bold'), fg='blue')
        profileLabel.pack(side='top')
        self.runQueue.append(profileName)
        
        if len(self.runQueue) == 1:
            runButton = tk.Button(self.runFrame, command=self.t1.start, text = 'Run', fg="green")
            runButton.pack(side='top', fill="x", expand=True)

    def resetQueue(self):
        self.clear_queueFrame()
        for widgets in self.runFrame.winfo_children():
            widgets.destroy()
        self.runQueue = []

    #Doesn't work on multiple runs
    def run(self):

        usb_devices, num_devices = port_scanner.scan_usb_ports()
        port_scanner.print_usb_devices(usb_devices)
        MFC_PORT, THERMOTRON_PORT = port_scanner.getDevicePorts(usb_devices)
        print(MFC_PORT, THERMOTRON_PORT)

        #Send Commands to Devices
        thermotron = Thermotron.Thermotron(THERMOTRON_PORT)   #Initialize Thermotron object
        MFC1 = MFC.MFC_device(MFC_PORT)

        #Hard coded
        sensor1 = Sensors.Sensors("COM5")
        sensor2 = Sensors.Sensors("COM9")


        for profile in self.runQueue:
            #MFC1_port = 'COM4'
            
            MFC1.setFlowRate('02',profile[1])
            program_number = int(profile[0][-1])
            MFC1.setFlowRate('04',profile[2])
            print(program_number)

            program = Experiment.Experiment(program_number)
            print("-"*72)
            print("Starting Program number: " + str(program.number) + '\n')

            thermotron.stop()

            initial_temp = program.intervals[0]["temp"]
            initial_humidity = program.intervals[0]["humidity"]

            print("Manually running until initial temperature: " + str(initial_temp) + '\n')

            thermotron.run_manual(initial_temp, initial_humidity)   #Start running in manual with initial SP's defined in program
            thermotron.getStatus()

            while thermotron.operatingmode == 2:         #While in manual, Poll temp and humidity

                if thermotron.oktopoll:
                    
                    thermotron.getStatus()

                    if thermotron.temp != initial_temp: #or thermotron.humidity != initial_humidity:  
                            thermotron.getTempandHumidity()
                            print("Temperature is: " + str(thermotron.temp))
                            #print("Humidity is: " + str(thermotron.humidity))

                    else:                                   #Once both SP's are reached stop Thermotron
                        thermotron.stop()

            print("-"*72)
            print("Starting program number " + str(program.number))
            
            thermotron.write_program(program.command)
            thermotron.run_program(program.number)      #Run desired progam
            thermotron.getStatus()

            while(thermotron.operatingmode == 3 or thermotron.operatingmode == 4):      #While program is running constantly poll for information

                if thermotron.oktopoll:
                    
                    sensor1.singleMeasurement()
                    sensor2.singleMeasurement()
                    thermotron.poll_experiment()
                    print("Current Interval: " + str(thermotron.interval))
                    print("Current Temperature: " + str(thermotron.temp))
                    print("Current Humidity: " + str(thermotron.humidity))
                    print("Time left in interval: " + str(thermotron.intervaltimeleft) + '\n')

            thermotron.stop() #Stop thermotron once program is done
            print("Program Done")
            

        
        self.clear_plotFrame()
        self.clear_queueFrame()
        self.clear_dataFrame()

    def getXY(self, data):
        
        time = (int(data[9]) * 60) + int(data[10])
        xAxis = [0, time]
        yTemp = [int(data[5]), int(data[7])]
        yHum = [int(data[6]), int(data[8])]

        i = 11
        c = 0
        while(i < len(data)):
            if c == 0:
                yTemp.append(int(data[i]))
                c += 1
            elif c == 1:
                yHum.append(int(data[i]))
                c += 1
            elif c == 2:
                time += (int(data[i]) * 60)
                c += 1
            elif c == 3:
                time += + int(data[i])
                xAxis.append(time)
                c = 0

            i += 1

        return yTemp,yHum,xAxis

    
    def showProfile(self, profileName):
        #f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Projects\\Capstone\\Capstone\\\profiles.csv", 'r')
        f = open("profiles.csv", 'r')
        profiles = f.readlines()
        f.close()
        print(profileName)

        self.clear_dataFrame()
        self.clear_plotFrame()

        for profile in profiles:
            data = profile.split(",")
            if data[0] == profileName:
                break
        
        
        profile_label = tk.Label(self.dataFrame, text = data[0], font=('calibre',10, 'bold'), fg="blue")
        profile_label.pack()

        fig1 = Figure(figsize = (5, 5),dpi = 100)
        plot1 = fig1.add_subplot(111)
        
        yTemp,yHum,xAxis = self.getXY(data)

        plot1.plot(xAxis,yTemp, label='Temperature')
        plot1.plot(xAxis,yHum, label='Humidity')
        plot1.legend()
        plot1.set_xlabel("Time (minutes)")
        plot1.set_ylabel("Degrees Celsius / % Humidity")
        canvas1 = FigureCanvasTkAgg(fig1,self.plotFrame)   
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="top")

        flowRate1_label = tk.Label(self.dataFrame, text = 'Flow Rate 1: ' + data[1], font=('calibre',10, 'bold'))
        flowRate2_label=tk.Label(self.dataFrame, text = 'Flow Rate 2: ' + data[2], font=('calibre',10, 'bold'))
        flowRate3_label=tk.Label(self.dataFrame, text = 'Flow Rate 3: ' + data[3], font=('calibre',10, 'bold'))
        flowRate4_label=tk.Label(self.dataFrame, text = 'Flow Rate 4: ' + data[4], font=('calibre',10, 'bold'))
        initialTemp_label=tk.Label(self.dataFrame, text = 'Initial Temperature: ' + data[5], font=('calibre',10, 'bold'))
        initialHum_label=tk.Label(self.dataFrame, text = 'Initial Humidity: ' + data[6], font=('calibre',10, 'bold'))
        finalTemp_label=tk.Label(self.dataFrame, text = 'Final Temperature: ' + data[7], font=('calibre',10, 'bold'))
        finalHum_label=tk.Label(self.dataFrame, text = 'Final Humidity: ' + data[8], font=('calibre',10, 'bold'))
        hours_label=tk.Label(self.dataFrame, text = 'Hours: ' + data[9], font=('calibre',10, 'bold'))
        minutes_label=tk.Label(self.dataFrame, text = 'Minutes: ' + data[10], font=('calibre',10, 'bold'))

        flowRate1_label.pack()
        flowRate2_label.pack()
        flowRate3_label.pack()
        flowRate4_label.pack()
        initialTemp_label.pack()
        initialHum_label.pack()
        finalTemp_label.pack()
        finalHum_label.pack()
        hours_label.pack()
        minutes_label.pack()

        addToQueueButton = tk.Button(self.plotFrame, command=lambda:self.addToQueue(data), text = 'Add to Queue')
        addToQueueButton.pack(side='top')


        

            