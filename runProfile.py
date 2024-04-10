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
import datetime
import csv

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #self.showProfiles()

        self.mfcList = []
        self.thermotronList = []
        self.sensors = []

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

        devicePortsButton = tk.Button(self.resetQueueFrame, command=self.openNewWindow, text = 'Device Ports')
        devicePortsButton.pack(side='left')

        self.programNum_frame = tk.Frame(self.monitorFrame)
        self.flowRate1_frame = tk.Frame(self.monitorFrame)
        self.flowRate2_frame = tk.Frame(self.monitorFrame)
        self.flowRate3_frame = tk.Frame(self.monitorFrame)
        self.flowRate4_frame = tk.Frame(self.monitorFrame)

        self.temp_frame = tk.Frame(self.monitorFrame)
        self.humidity_frame = tk.Frame(self.monitorFrame)
        self.interval_frame = tk.Frame(self.monitorFrame)
        self.intervalTimeLeft_frame = tk.Frame(self.monitorFrame)

        programNum_label = tk.Label(self.programNum_frame, text = 'Profile: ', font=('calibre',10, 'bold'))
        tempValue_label = tk.Label(self.temp_frame, text = 'Temperature: ', font=('calibre',10, 'bold'))
        humidityValue_label = tk.Label(self.humidity_frame, text = 'Humidity: ', font=('calibre',10, 'bold'))
        intervalValue_label = tk.Label(self.interval_frame, text = 'Interval: ', font=('calibre',10, 'bold'))
        timeLeftValue_label = tk.Label(self.intervalTimeLeft_frame, text = 'Time left in Interval: ', font=('calibre',10, 'bold'))

        flowRate1_label = tk.Label(self.flowRate1_frame, text = 'Flow Rate 1: ', font=('calibre',10, 'bold'))
        flowRate2_label = tk.Label(self.flowRate2_frame, text = 'Flow Rate 2: ', font=('calibre',10, 'bold'))
        flowRate3_label = tk.Label(self.flowRate3_frame, text = 'Flow Rate 3: ', font=('calibre',10, 'bold'))
        flowRate4_label = tk.Label(self.flowRate4_frame, text = 'Flow Rate 4: ', font=('calibre',10, 'bold'))

        self.programNum_frame.pack()
        self.flowRate1_frame.pack()
        self.flowRate2_frame.pack()
        self.flowRate3_frame.pack()
        self.flowRate4_frame.pack()

        self.temp_frame.pack()
        self.humidity_frame.pack()
        self.interval_frame.pack()
        self.intervalTimeLeft_frame.pack()

        programNum_label.pack(side='left')
        flowRate1_label.pack(side='left')
        flowRate2_label.pack(side='left')
        flowRate3_label.pack(side='left')
        flowRate4_label.pack(side='left')

        tempValue_label.pack(side='left')
        humidityValue_label.pack(side='left')
        intervalValue_label.pack(side='left')
        timeLeftValue_label.pack(side='left')

        self.programNum = 0
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

        try:
            usb_devices, num_devices = port_scanner.scan_usb_ports()
            MFC_PORT, THERMOTRON_PORT,data = port_scanner.getDevicePorts(usb_devices)
        except:
            #print("USB Devices not found")
            pass

        self.profileFrameList = []
        self.t1 = threading.Thread(target=self.run, daemon=True)
        self.t1.start()
        self.t2 = threading.Thread(target=self.updateLabels, daemon=True)
        self.t2.start()
        #self.t3.start()

        
    
    def showProfileButtons(self):
        #f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Projects\\Capstone\\Capstone\\profiles.csv", 'r')
        f = open("profiles.csv", 'r')

        profiles = f.readlines()
        f.close()
        self.resetQueue()
        self.profileList = []
        try:
            self.plotFrame.pack_forget()
            self.monitorFrame.pack_forget()
            self.dataFrame.pack_forget()
            self.runFrame.pack_forget()
            self.utilityFrame.pack_forget()
            for frame in self.profileFrameList:
                frame.pack_forget()
            self.profileFrameList = []
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
            self.profileFrameList.append(profileFrame)
        
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
            
            programNum_label = tk.Label(self.programNum_frame, text = self.programNum, font=('calibre',10, 'bold')).pack()
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

            self.programNum_frame.winfo_children()[1].destroy()
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
        self.destroyAddToQueueButton()
        for widgets in self.runFrame.winfo_children():
            widgets.destroy()
        self.runQueue = []
        self.update()
    
    def resetQueueRun(self):
        self.clear_queueFrame()
        for widgets in self.runFrame.winfo_children():
            widgets.destroy()
        self.update()

    def destroyAddToQueueButton(self):
        for widgets in self.resetQueueFrame.winfo_children():
            if widgets.cget('text') == 'Add to Queue':
                widgets.destroy()
                break

    #Doesn't work on multiple runs

    def stopExp(self):
        self.experimentRunning = False
        self.isRunningFrame.winfo_children()[1].destroy()
        isRunningStatusLabel = tk.Label(self.isRunningFrame, text = 'IDLE', font=('calibre',10, 'bold'), fg='green').pack(side='left')
    
    def pauseExp(self):
        self.isRunningFrame.winfo_children()[1].destroy()
        isRunningStatusLabel = tk.Label(self.isRunningFrame, text = 'PAUSED', font=('calibre',10, 'bold'), fg='yellow').pack(side='left')
    
    def getEmail(self, newWindow):

        self.email = self.emailVar.get()
        newWindow.destroy()

        self.experimentRunning = True
        self.isRunningFrame.winfo_children()[1].destroy()
        isRunningStatusLabel = tk.Label(self.isRunningFrame, text = 'RUNNING', font=('calibre',10, 'bold'), fg='red').pack(side='left')

    def runExp(self):

        newWindow = tk.Toplevel(self)
        newWindow.title("Email Notifications")

        self.emailVar = tk.StringVar()
        entryFrame = tk.Frame(newWindow)
        entryFrame.pack(side="top", fill="x", expand=False)
        getEmail_label = tk.Label(entryFrame, text = 'Enter Email Address for Experiment status notifications (optional): ', font=('calibre',10, 'bold'))
        getEmail_entry = tk.Entry(entryFrame,textvariable = self.emailVar, font=('calibre',10,'normal'))
        getEmail_label.pack(side="left", expand=False)
        getEmail_entry.pack(side="left", fill="x", expand=True)

        self.sub_btn=tk.Button(newWindow,text = 'Submit', command=lambda:self.getEmail(newWindow))
        self.sub_btn.pack(side="top")

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def openNewWindow(self):

        newWindow = tk.Toplevel(self)
        newWindow.title("Device Ports")
    
        # sets the geometry of toplevel
        newWindow.geometry("600x600")

        vcmd = (newWindow.register(self.callback))

        self.mfcPortVar=tk.StringVar()
        self.thermotronPortVar=tk.StringVar()

        entryFrame1 = tk.Frame(newWindow)
        entryFrame1.pack(side="top", fill="x", expand=False)
        MFC_label = tk.Label(entryFrame1, text = 'Brooks MFC COM Port #: ', font=('calibre',10, 'bold'))
        self.MFC_entry = tk.Entry(entryFrame1,textvariable = self.mfcPortVar, font=('calibre',10,'normal'), validate='all', validatecommand=(vcmd,'%P'))
        MFC_label.pack(side="left", expand=False)
        self.MFC_entry.pack(side="left", fill="x", expand=True)

        entryFrame2 = tk.Frame(newWindow)
        entryFrame2.pack(side="top", fill="x", expand=False)
        thermotron_label = tk.Label(entryFrame2, text = 'Thermotron COM Port #: ', font=('calibre',10, 'bold'))
        self.thermotron_entry = tk.Entry(entryFrame2,textvariable = self.thermotronPortVar, font=('calibre',10,'normal'), validate='all', validatecommand=(vcmd,'%P'))
        thermotron_label.pack(side="left", expand=False)
        self.thermotron_entry.pack(side="left", fill="x", expand=True)

        self.error_label1 = tk.Label(newWindow, text = 'Please provide port numbers for the MFC and Thermotron', font=('calibre',10, 'bold'), fg='red')

        doneButton = tk.Button(newWindow, command=lambda:[self.getPortEntry(newWindow)], text = 'Use Newly Entered Ports')
        doneButton.pack(side='bottom', fill='x')

        loadSavedButton = tk.Button(newWindow, command=lambda:[self.getSavedPorts(), newWindow.destroy()], text = 'Use Saved Ports')
        loadSavedButton.pack(side='bottom', fill='x')

        self.sensorPortVars = []
        addSensorButton = tk.Button(newWindow, command=lambda:self.addSensorPort(newWindow), text = 'Add Sensor')
        addSensorButton.pack(side='bottom', fill='x')

        self.postSaved(newWindow)
    
    def postSaved(self, newWindow):
            savedFrame = tk.Frame(newWindow)
            savedFrame.pack(side='bottom')

            with open('devices.json', 'r') as json_file:
                data = json.load(json_file)

            sensorLabelList = []
            saved_label = tk.Label(savedFrame, text = 'Previously Saved Device COM Ports:', font=('calibre',10, 'bold'), fg='green').pack(side='top')
            saved_mfc_label = tk.Label(savedFrame, text = 'Brooks MFC COM Port #: ' + data['MFC'], font=('calibre',10, 'bold')).pack(side='top')
            saved_thermotron_label = tk.Label(savedFrame, text = 'Thermotron COM Port #: ' + data['Thermotron'], font=('calibre',10, 'bold')).pack(side='top')

            for device in data:
                if 'Sensor' in device:
                    saved_sensor_label = tk.Label(savedFrame, text = device + ' COM Port #: ' + data[device], font=('calibre',10, 'bold')).pack(side='top')
    
    def getSavedPorts(self):
        
        with open('devices.json', 'r') as json_file:
                data = json.load(json_file)

        self.MFC_PORT = data['MFC']
        self.THERMOTRON_PORT = data['Thermotron']

        self.sensorPorts = []
        for device in data:
                if 'Sensor' in device:
                    self.sensorPorts.append(data[device])

    def getPortEntry(self, newWindow):
        
        if(not self.mfcPortVar.get() or not self.thermotronPortVar.get()):
            self.error_label1.pack(side='bottom')
            return

        self.MFC_PORT = 'COM' + str(self.mfcPortVar.get())
        self.THERMOTRON_PORT = 'COM' + str(self.thermotronPortVar.get())

        devices = {'MFC' : self.MFC_PORT, 'Thermotron' : self.THERMOTRON_PORT}
        self.sensorPorts = []
        
        count = 1
        for sensorPort in self.sensorPortVars:
            self.sensorPorts.append('COM' + str(sensorPort.get()))
            devices['Sensor' + str(count)] = 'COM' + str(sensorPort.get())
            count += 1
        
        
        with open('devices.json', 'w') as json_file:
            json.dump(devices,json_file)

        newWindow.destroy()

    def addSensorPort(self, newWindow):
        
        vcmd = (newWindow.register(self.callback))
        sensorPortVar=tk.StringVar()
        self.sensorPortVars.append(sensorPortVar)
        sensorNum = len(self.sensorPortVars)

        entryFrame1 = tk.Frame(newWindow)
        entryFrame1.pack(side="top", fill="x", expand=False)
        flowRate1_label = tk.Label(entryFrame1, text = 'Sensor' + str(sensorNum) +  ' COM Port #: ', font=('calibre',10, 'bold'))
        self.flowRate1_entry = tk.Entry(entryFrame1,textvariable = sensorPortVar, font=('calibre',10,'normal'), validate='all', validatecommand=(vcmd,'%P'))
        flowRate1_label.pack(side="left", expand=False)
        self.flowRate1_entry.pack(side="left", fill="x", expand=True)

    def on_closing(self):

        if len(self.mfcList):
            self.mfcList[0].port.close()
        if len(self.thermotronList):
            self.thermotronList[0].port.close()
        if len(self.sensors):
            for sensor in self.sensors:
                sensor.port.close()
        self.destroy()

    def run(self):

        while(1):

            time.sleep(1)
            if (self.experimentRunning):

                if len(self.mfcList):
                    MFC1 = self.mfcList[0]
                else:
                    MFC1 = MFC.MFC_device(self.MFC_PORT)
                    self.mfcList.append(MFC1)
                    print('Created MFC object')

                if len(self.thermotronList):
                    thermotron = self.thermotronList[0]
                else:
                    thermotron = Thermotron.Thermotron(self.THERMOTRON_PORT)
                    self.thermotronList.append(thermotron)
                    print("Created thermotron object")

                self.clear_plotFrame()
                self.clear_queueFrame()
                self.clear_dataFrame()
                self.resetQueueRun()

                receive_address = self.email

                #Send Commands to Devices
                #try:
                #thermotron = Thermotron.Thermotron(self.THERMOTRON_PORT)   #Initialize Thermotron object                
                #MFC1 = MFC.MFC_device(self.MFC_PORT)
                #except:
                    #self.experimentRunning = False
                    #print("Thermotron/MFC Ports not connected")

                try:
                    if(not self.sensorPorts):
                        self.experimentRunning = False
                except:
                    self.experimentRunning = False
                    print("Sensor ports not found")

                if(not len(self.sensors)):
                    try: 
                        for sensorPort in self.sensorPorts:
                            self.sensors.append(Sensors.Sensors(sensorPort))
                    except:
                        self.experimentRunning = False
                        print("Sensor Ports not connected")

                stopButton = tk.Button(self.utilityFrame, command=lambda:[self.stopExp(), thermotron.GUI_Request("STOP")], text = 'Stop Experiment')
                stopButton.pack(side='left')

                pauseButton = tk.Button(self.utilityFrame, command=lambda:[self.pauseExp(), thermotron.GUI_Request("HOLD")], text = 'Pause Experiment')
                pauseButton.pack(side='left')

                continueButton = tk.Button(self.utilityFrame, command=lambda:[self.runExp(), thermotron.GUI_Request("RUN")], text = 'Continue Experiment')
                continueButton.pack(side='left')

                self.monitorFrame.pack()
                #try:
    
                for profile in self.runQueue:
                        
                        receive_email = self.email

                        program_number = int(profile[0][-1])
                        self.programNum = program_number
                        
                        
                        if(profile[1] != ''):
                            MFC1.setFlowRate('02',str(int(profile[1])*1000))
                        if(profile[2] != ''):
                            MFC1.setFlowRate('04',str(int(profile[2])*1000))
                        if(profile[3] != ''):
                            MFC1.setFlowRate('06',str(int(profile[3])*1000))
                        if(profile[4] != ''):
                            MFC1.setFlowRate('08',str(int(profile[4])*1000))

                        program = Experiment.Experiment(program_number)                      #Create experiment object
                        
                        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
                        file_name =  current_datetime + "_Program_Number_"+ str(program.number) + ".csv"
                        file_path = "./Thermotron_data/Thermotron_data_" + file_name

                        first_row = ["Started on:", current_datetime, "Program #:", program.number, "Flow Rate 1:", self.flowRate1, "Flow Rate 2:", self.flowRate2, "Flow Rate 3:", self.flowRate3, "Flow Rate 4:", self.flowRate4]
                        headers = ["Interval #", "Time in Interval", "Temperature", "Humidity"]
                        for i in range(len(self.sensors)):
                            headers.append("Sensor" + str(i) + ": Col1")
                            headers.append("Sensor" + str(i) + ": Col2")
                            headers.append("Sensor" + str(i) + ": Col3")
                            headers.append("Sensor" + str(i) + ": Col4")
                            headers.append("Sensor" + str(i) + ": Col5")
                            headers.append("Sensor" + str(i) + ": Col6")
                            headers.append("Sensor" + str(i) + ": Col7")
                            headers.append("Sensor" + str(i) + ": Col8")
                            headers.append("Sensor" + str(i) + ": Col9")
                            headers.append("Sensor" + str(i) + ": Col10")
                            headers.append("Sensor" + str(i) + ": Col11")

                        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")

                        file_name =  current_datetime + "_Program_Number_"+ str(program.number) + ".csv"
                        file_path = "Thermotron_data/Thermotron_data_" + file_name



                        file = open(file_path, mode='a', newline='')
                        writer = csv.writer(file)
                        writer.writerow(first_row)   #Write first row containing information thats constant throughout a program
                        writer.writerow("")
                        writer.writerow(headers)     #Write the headers for the data
                        
                        initial_temp = program.intervals[0]["temp"]                          #Set initial temperature and humidity
                        initial_humidity = program.intervals[0]["humidity"]

                        print('test')
                        thermotron.stop()                                                    #Place in stop initially
                        thermotron.write_program(program.command)                            #Write program to Thermotron
                        thermotron.run_manual(initial_temp, initial_humidity)                #Start running in manual with initial SP's defined in program

                        print("-"*72)                                                        
                        print("Starting Program number: " + str(program.number) + '\n')            
                        print("Manually running until initial temperature: " + str(initial_temp) + '\n')
                        print("Manually running until initial humidity: " + str(initial_humidity) + '\n')

                        setpoint_ok_count = 0
                        
                        start_time = datetime.datetime.now()

                        setpoint_ok_max = 50

                        self.flowRate1 = MFC1.getFlowRate('02')
                        self.flowRate2 = MFC1.getFlowRate('04')
                        self.flowRate3 = MFC1.getFlowRate('06')
                        self.flowRate4 = MFC1.getFlowRate('08')

                        while (thermotron.operatingmode == 2 or thermotron.operatingmode == 4) and setpoint_ok_count < setpoint_ok_max:  #While in manual/hold and setpoints have not been reached for 100 ticks
                            
                            if thermotron.operatingmode == 2:         #Don't poll while it's in hold (but stay in while loop)

                                thermotron.getStatus()
                                thermotron.getTempandHumidity()
                                print("Temperature is: " + str(thermotron.temp))
                                #print("Humidity is: " + str(thermotron.humidity))

                                if (thermotron.temp < initial_temp - 1 or thermotron.temp > initial_temp + 1): #or (thermotron.humidity < initial_humidity - 1 or thermotron.humidity > initial_humidity + 1):
                                    
                                    setpoint_ok_count = 0  #Reset count if temp/humidity are out of setpoint bounds
                                
                                else:
                                    
                                    print("Setpoint ok, tick " + str(setpoint_ok_count) + "/" + str(setpoint_ok_max) + '\n')
                                    setpoint_ok_count = setpoint_ok_count + 1 #Increment count if temp/humidity is within bounds
                        
                        if thermotron.GUI_stop_request == True:               #Break out of schedule if stop button is hit

                            thermotron.GUI_stop_request == False
                            print("Program stopped by GUI\n")

                            [subject, message] = Thermotron.email_msg(program_number = program.number, start_time= current_datetime, early_stop= "GUI")
                            Thermotron.send_email(receiver= receive_email ,subject= subject, message = message, file_path=file_path, file_name= file_name)
                            
                            self.stopExp()
                            break

                        
                        end_time = datetime.datetime.now()

                        print("Manual run took: " + str(end_time - start_time) + '\n')
                        print("-"*72)
                        print("Starting program number " + str(program.number))
                        
                        thermotron.stop_run_program(program.number)      #Stop, then run selected program
                        thermotron.getStatus()

                        while(thermotron.operatingmode == 3 or thermotron.operatingmode == 4):      #While program is running/hold constantly poll for information
                            
                            if(thermotron.operatingmode == 3):      #Dont poll while its in hold but stay in while loop
                                
                                self.flowRate1 = MFC1.getFlowRate('02')
                                self.flowRate2 = MFC1.getFlowRate('04')
                                self.flowRate3 = MFC1.getFlowRate('06')
                                self.flowRate4 = MFC1.getFlowRate('08')

                                thermotron.poll_experiment()

                                time_in_interval = thermotron.intervaltimetotal - thermotron.intervaltimeleft

                                dataToCSV = [thermotron.interval, time_in_interval , thermotron.temp, thermotron.humidity]
                                
                                for sensor in self.sensors:
                                    data = (sensor.singleMeasurement().strip("\r\n")).split(",")
                                    
                                    for col in data:
                                        dataToCSV.append(col)

                                print()

                                writer.writerow(dataToCSV)

                                self.temp = thermotron.temp
                                self.humidity = thermotron.humidity
                                self.interval = thermotron.interval
                                self.time = thermotron.intervaltimeleft


                                print("Current Interval: " + str(thermotron.interval))
                                print("Current Temperature: " + str(thermotron.temp))
                                print("Current Humidity: " + str(thermotron.humidity))

                                print(str(time_in_interval) + " out of " + str(thermotron.intervaltimetotal) + " minutes in interval\n")
                            
                            #time.sleep(0.5)

                        if thermotron.GUI_stop_request == True:        #Break out of schedule if stop button is hit

                            thermotron.GUI_stop_request == False
                            
                            [subject, message] = Thermotron.email_msg(program_number = program.number, start_time= current_datetime, early_stop= "GUI")
                            Thermotron.send_email(receiver= receive_email ,subject= subject, message = message, file_path=file_path, file_name= file_name)
                            
                            print("Program stopped by GUI\n")
                            self.stopExp()
                            break


                        if thermotron.interval == program.interval_count + 1:

                            [subject, message] = Thermotron.email_msg(program_number = program.number, start_time= current_datetime )
                            Thermotron.send_email(receiver= receive_email,subject= subject, message = message, file_path=file_path, file_name= file_name)
                            print("Program Completed")

                        else:

                            [subject, message] = Thermotron.email_msg(program_number = program.number, start_time= current_datetime, early_stop= "STOP")
                            Thermotron.send_email(receiver= receive_email, subject= subject, message = message, file_path=file_path, file_name= file_name)
                            print("Program Stopped from Thermotron")
                        
                        thermotron.stop() #Stop thermotron once program is done
                        file.close()

                
                #except:
                #try:
                #        thermotron.stop
                #       file.close()

                #except:
                #        pass
                #finally:
                        #[subject, message] = Thermotron.email_msg(error = True )
                        #Thermotron.send_email(receiver= receive_address,subject= subject, message = message)
                        #print("Error occured")
                

                self.resetQueue()
                self.clear_utilityFrame()
                self.showProfile()
                self.monitorFrame.pack_forget()
                self.stopExp()
                
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
        #fix

        self.destroyAddToQueueButton()
        addToQueueButton = tk.Button(self.resetQueueFrame, command=lambda:self.addToQueue(data), text = 'Add to Queue')
        addToQueueButton.pack(side='top')


        

            
