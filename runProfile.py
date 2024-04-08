import tkinter as tk
import MFC
from page import Page
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import Thermotron
import Experiment
import threading
import port_scanner
import Sensors
import random
import time
import json

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #self.showProfiles()
        self.profileList = []
        self.dataFrame = tk.Frame(self)
        self.plotFrame = tk.Frame(self)
        self.monitorFrame = tk.Frame(self)
        self.queueFrame = tk.Frame(self)
        self.resetQueueFrame = tk.Frame(self)
        self.runFrame = tk.Frame(self)
        self.utilityFrame = tk.Frame(self)

        self.runQueue = []
        self.isRunningFrame = tk.Frame(self)
        self.isRunningFrame.pack(side='top')
        queue_label = tk.Label(self, text = 'Queue: ', font=('calibre',10, 'bold'))
        queue_label.pack(side='top')

        self.queueFrame.pack(side='top')
        self.resetQueueFrame.pack(side='top')
        
        resetQueueButton = tk.Button(self.resetQueueFrame, command=self.resetQueue, text = 'Reset Queue')
        resetQueueButton.pack(side='left')

        #devicePortsButton = tk.Button(self.resetQueueFrame, command=self.openNewWindow, text = 'Device Ports')
        #devicePortsButton.pack(side='left')

        
        self.flowRate1_frame = tk.Frame(self.monitorFrame)
        self.flowRate2_frame = tk.Frame(self.monitorFrame)
        self.flowRate3_frame = tk.Frame(self.monitorFrame)
        self.flowRate4_frame = tk.Frame(self.monitorFrame)

        self.temp_frame = tk.Frame(self.monitorFrame)
        self.humidity_frame = tk.Frame(self.monitorFrame)
        self.interval_frame = tk.Frame(self.monitorFrame)
        self.intervalTimeLeft_frame = tk.Frame(self.monitorFrame)

        tempValue_label = tk.Label(self.temp_frame, text = 'Temperature: ', font=('calibre',10, 'bold'))
        humidityValue_label = tk.Label(self.humidity_frame, text = 'Humidity: ', font=('calibre',10, 'bold'))
        intervalValue_label = tk.Label(self.interval_frame, text = 'Interval: ', font=('calibre',10, 'bold'))
        timeLeftValue_label = tk.Label(self.intervalTimeLeft_frame, text = 'Time left in Interval: ', font=('calibre',10, 'bold'))

        flowRate1_label = tk.Label(self.flowRate1_frame, text = 'Flow Rate 1: ', font=('calibre',10, 'bold'))
        flowRate2_label = tk.Label(self.flowRate2_frame, text = 'Flow Rate 2: ', font=('calibre',10, 'bold'))
        flowRate3_label = tk.Label(self.flowRate3_frame, text = 'Flow Rate 3: ', font=('calibre',10, 'bold'))
        flowRate4_label = tk.Label(self.flowRate4_frame, text = 'Flow Rate 4: ', font=('calibre',10, 'bold'))

        self.flowRate1_frame.pack()
        self.flowRate2_frame.pack()
        self.flowRate3_frame.pack()
        self.flowRate4_frame.pack()

        self.temp_frame.pack()
        self.humidity_frame.pack()
        self.interval_frame.pack()
        self.intervalTimeLeft_frame.pack()

        flowRate1_label.pack(side='left')
        flowRate2_label.pack(side='left')
        flowRate3_label.pack(side='left')
        flowRate4_label.pack(side='left')

        tempValue_label.pack(side='left')
        humidityValue_label.pack(side='left')
        intervalValue_label.pack(side='left')
        timeLeftValue_label.pack(side='left')

        self.flowRate1 = 0
        self.flowRate2 = 0
        self.flowRate3 = 0
        self.flowRate4 = 0
        self.temp = 0
        self.humidity = 0
        self.time = 0
        self.interval = 0

        self.experimentRunning = False
        
        isRunningLabel = tk.Label(self.isRunningFrame, text = 'Status: ', font=('calibre',10, 'bold')).pack(side='left')
        isRunningStatusLabel = tk.Label(self.isRunningFrame, text = 'IDLE', font=('calibre',10, 'bold'), fg='green').pack(side='left')

        self.t1 = threading.Thread(target=self.run, daemon=True)
        self.t1.start()
        self.t2 = threading.Thread(target=self.updateLabels, daemon=True)
        #self.t4 = threading.Thread(target=self.checkExperiment, daemon=True)
        self.t2.start()
        #self.t3.start()

        
    
    def showProfileButtons(self):
        #f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Projects\\Capstone\\Capstone\\profiles.csv", 'r')
        f = open("profiles.csv", 'r')

        profiles = f.readlines()
        f.close()

        try:
            self.plotFrame.pack_forget()
            self.monitorFrame.pack_forget()
            self.dataFrame.pack_forget()
            self.runFrame.pack_forget()
            self.utilityFrame.pack_forget()
        except:
            pass
        
        for profile in profiles:
            
            data = profile.split(",")

            if(data[0] in self.profileList):
                continue
            
            profileFrame = tk.Frame(self)
            profileFrame.pack(side="top", fill="x")

            profileButton = tk.Button(profileFrame,command=lambda arg = data[0] : self.showProfile(arg),text = data[0])
            profileButton.pack(side="top", fill="x")

            self.profileList.append(data[0])
        
        self.utilityFrame.pack(side='top')
        self.runFrame.pack(side='top')
        self.dataFrame.pack(side='left')
        self.plotFrame.pack(side='left')

        if self.experimentRunning:
            self.monitorFrame.pack(side='left')

    def clear_dataFrame(self):
        for widgets in self.dataFrame.winfo_children():
            widgets.destroy()
    
    def clear_plotFrame(self):
        for widgets in self.plotFrame.winfo_children():
            widgets.destroy()
    
    def clear_queueFrame(self):
        for widgets in self.queueFrame.winfo_children():
            widgets.destroy()
        self.update()
    
    def clear_utilityFrame(self):
        for widgets in self.utilityFrame.winfo_children():
            widgets.destroy()

    def addToQueue(self, profileName):
        profileLabel = tk.Label(self.queueFrame, text = profileName[0], font=('calibre',10, 'bold'), fg='blue')
        profileLabel.pack(side='left')
        self.runQueue.append(profileName)
        
        if len(self.runQueue) == 1:
            runButton = tk.Button(self.runFrame, command=self.runExp, text = 'Run', fg="green")
            runButton.pack(side='top', fill="x", expand=True)

    def updateLabels(self):

        while(1):

            #flowRate1 = MFC1.getFlowRate('02')
            #flowRate2 = MFC1.getFlowRate('04')
            #flowRate3 = MFC1.getFlowRate('06')
            #flowRate4 = MFC1.getFlowRate('08')

            flowRate1Value_label = tk.Label(self.flowRate1_frame, text = self.flowRate1, font=('calibre',10, 'bold'))
            flowRate2Value_label = tk.Label(self.flowRate2_frame, text = self.flowRate2, font=('calibre',10, 'bold'))
            flowRate3Value_label = tk.Label(self.flowRate3_frame, text = self.flowRate3, font=('calibre',10, 'bold'))
            flowRate4Value_label = tk.Label(self.flowRate4_frame, text = self.flowRate4, font=('calibre',10, 'bold'))

            flowRate1Value_label.pack(side='top')
            flowRate2Value_label.pack(side='top')
            flowRate3Value_label.pack(side='top')
            flowRate4Value_label.pack(side='top')

            temp_label = tk.Label(self.temp_frame, text = self.temp, font=('calibre',10, 'bold'))
            humidity_label = tk.Label(self.humidity_frame, text = self.humidity, font=('calibre',10, 'bold'))
            interval_label = tk.Label(self.interval_frame, text = self.interval, font=('calibre',10, 'bold'))
            time_label = tk.Label(self.intervalTimeLeft_frame, text = self.time, font=('calibre',10, 'bold'))

            temp_label.pack(side='top')
            humidity_label.pack(side='top')
            interval_label.pack(side='top')
            time_label.pack(side='top')
            
            time.sleep(1)

            self.flowRate1_frame.winfo_children()[1].destroy()
            self.flowRate2_frame.winfo_children()[1].destroy()
            self.flowRate3_frame.winfo_children()[1].destroy()
            self.flowRate4_frame.winfo_children()[1].destroy()

            self.temp_frame.winfo_children()[1].destroy()
            self.humidity_frame.winfo_children()[1].destroy()
            self.interval_frame.winfo_children()[1].destroy()
            self.intervalTimeLeft_frame.winfo_children()[1].destroy()

    def resetQueue(self):
        self.clear_queueFrame()
        for widgets in self.runFrame.winfo_children():
            widgets.destroy()
        self.runQueue = []
        self.update()
    
    def resetQueueFrame(self):
        self.clear_queueFrame()
        for widgets in self.runFrame.winfo_children():
            widgets.destroy()
        self.update()

    #Doesn't work on multiple runs

    def stopExp(self):
        self.experimentRunning = False
        self.isRunningFrame.winfo_children()[1].destroy()
        isRunningStatusLabel = tk.Label(self.isRunningFrame, text = 'IDLE', font=('calibre',10, 'bold'), fg='green').pack(side='left')
    
    def pauseExp(self):
        self.isRunningFrame.winfo_children()[1].destroy()
        isRunningStatusLabel = tk.Label(self.isRunningFrame, text = 'PAUSED', font=('calibre',10, 'bold'), fg='yellow').pack(side='left')
    
    def runExp(self):
        self.experimentRunning = True
        self.isRunningFrame.winfo_children()[1].destroy()
        isRunningStatusLabel = tk.Label(self.isRunningFrame, text = 'RUNNING', font=('calibre',10, 'bold'), fg='red').pack(side='left')

    def openNewWindow(self):

        newWindow = tk.Toplevel(self)
        newWindow.title("Device Ports")
    
        # sets the geometry of toplevel
        newWindow.geometry("600x600")

        usb_devices, num_devices = port_scanner.scan_usb_ports()
        MFC_PORT, THERMOTRON_PORT = port_scanner.getDevicePorts(usb_devices)

        with open('devices.json', 'r') as json_file:
            data = json.load(json_file)
        

    def run(self):

        while(1):

            time.sleep(1)

            if (self.experimentRunning):

                self.clear_plotFrame()
                self.clear_queueFrame()
                self.clear_dataFrame()

                self.resetQueueFrame()# needs to be fixed

                usb_devices, num_devices = port_scanner.scan_usb_ports()
                port_scanner.print_usb_devices(usb_devices)
                MFC_PORT, THERMOTRON_PORT, data = port_scanner.getDevicePorts(usb_devices)
                print(MFC_PORT, THERMOTRON_PORT)

                #Send Commands to Devices
                thermotron = Thermotron.Thermotron(THERMOTRON_PORT)   #Initialize Thermotron object
                MFC1 = MFC.MFC_device(MFC_PORT)

                sensors = []
                for device in data:
                    if "Sensor" in device:
                        sensor = Sensors.Sensors(data[device])
                        sensors.append(sensor)

                stopButton = tk.Button(self.utilityFrame, command=lambda:[self.stopExp, thermotron.GUI_Request("STOP")], text = 'Stop Experiment')
                stopButton.pack(side='left')

                pauseButton = tk.Button(self.utilityFrame, command=lambda:[self.pauseExp, thermotron.GUI_Request("HOLD")], text = 'Pause Experiment')
                pauseButton.pack(side='left')

                continueButton = tk.Button(self.utilityFrame, command=lambda:[self.runExp, thermotron.GUI_Request("RUN")], text = 'Continue Experiment')
                continueButton.pack(side='left')

                self.monitorFrame.pack()

                while(1):
                    
                    for profile in self.runQueue:
                        #MFC1_port = 'COM4'
                        
                        MFC1.setFlowRate('02',profile[1])
                        program_number = int(profile[0][-1])
                        MFC1.setFlowRate('04',profile[2])

                        program = Experiment.Experiment(program_number)                      #Create experiment object
                        
                        print("-"*72)                                                        
                        print("Starting Program number: " + str(program.number) + '\n')

                        thermotron.stop()                                                    #Place in stop initially

                        initial_temp = program.intervals[0]["temp"]                          #Set initial temperature and humidity
                        initial_humidity = program.intervals[0]["humidity"]

                        print("Manually running until initial temperature: " + str(initial_temp) + '\n')
                        print("Manually running until initial humidity: " + str(initial_humidity) + '\n')

                        thermotron.run_manual(initial_temp, initial_humidity)   #Start running in manual with initial SP's defined in program

                        setpoint_ok_count = 0

                        while (thermotron.operatingmode == 2 or thermotron.operatingmode == 4) and setpoint_ok_count < 100:  #While in manual/hold and setpoints have not been reached for 100 ticks
                            
                            if thermotron.operatingmode == 2:         #Don't poll while it's in hold (but stay in while loop)

                                thermotron.getStatus()
                                thermotron.getTempandHumidity()
                                print("Temperature is: " + str(thermotron.temp))
                                #print("Humidity is: " + str(thermotron.humidity))

                                if (thermotron.temp < initial_temp - 1 or thermotron.temp > initial_temp + 1): #or thermotron.humidity != initial_humidity:  
                                    
                                    setpoint_ok_count = 0  #Reset count if temp/humidity are out of setpoint bounds
                                
                                else:
                                    setpoint_ok_count = setpoint_ok_count + 1 #Increment count if temp/humidity is within bounds
                        
                        if thermotron.GUI_stop_request == True:               #Break out of schedule if stop button is hit

                            thermotron.GUI_stop_request == False
                            print("Program stopped by GUI\n")
                            self.stopExp()
                            break

                        thermotron.stop()  

                        print("-"*72)
                        print("Starting program number " + str(program.number))
                        
                        thermotron.write_program(program.command)
                        thermotron.run_program(program.number)      #Run desired progam

                        while(thermotron.operatingmode == 3 or thermotron.operatingmode == 4):      #While program is running/hold constantly poll for information
                            
                            if(thermotron.operatingmode == 3):      #Dont poll while its in hold but stay in while loop
                                
                                self.flowRate1 = random.randint(1,100)
                                self.flowRate2 = random.randint(1,100)
                                self.flowRate3 = random.randint(1,100)
                                self.flowRate4 = random.randint(1,100)
                                
                                for sensor in sensors:
                                    sensor.singleMeasurement()
                                    sensor.singleMeasurement()

                                thermotron.poll_experiment()

                                print("Current Interval: " + str(thermotron.interval))
                                print("Current Temperature: " + str(thermotron.temp))
                                print("Current Humidity: " + str(thermotron.humidity))
                                print("Time left in interval: " + str(thermotron.intervaltimeleft) + '\n')

                                self.temp = thermotron.temp
                                self.humidity = thermotron.humidity
                                self.interval = thermotron.interval
                                self.time = thermotron.intervaltimeleft
                            
                            time.sleep(1)

                        if thermotron.GUI_stop_request == True:        #Break out of schedule if stop button is hit

                            thermotron.GUI_stop_request == False

                            print("Program stopped by GUI\n")
                            self.stopExp()
                            break

                        thermotron.stop() #Stop thermotron once program is done
                        print("Program Done")
                
                
                self.resetQueue()
                self.clear_utilityFrame()
                self.showProfile()
                self.monitorFrame.pack_forget()
                
            else:
                time.sleep(1)


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

    
    def showProfile(self, profileName = None):
        #f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Projects\\Capstone\\Capstone\\\profiles.csv", 'r')
        f = open("profiles.csv", 'r')
        profiles = f.readlines()
        f.close()
        #print(profileName)

        self.clear_dataFrame()
        self.clear_plotFrame()


        for profile in profiles:

            data = profile.split(",")
            if (profileName == None):
                break
            elif data[0] == profileName:
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


        

            
