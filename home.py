import tkinter as tk
from page import Page
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import time
import threading
import MFC
import random
import Thermotron

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.profileList = []
        self.dataFrame = tk.Frame(self)
        self.plotFrame = tk.Frame(self)
        self.monitorFrame = tk.Frame(self)
        self.queueFrame = tk.Frame(self)

        self.runQueue = []
        self.isRunningFrame = tk.Frame(self)
        self.isRunningFrame.pack(side='top')

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
        self.profileFrameList = []

        #self.t3.start()

    def showProfileButtons(self):
        #f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Projects\\Capstone\\Capstone\\profiles.csv", 'r')
        f = open("profiles.csv", 'r')

        profiles = f.readlines()
        f.close()
        self.profileList = []

        try:
            self.plotFrame.pack_forget()
            self.monitorFrame.pack_forget()
            self.dataFrame.pack_forget()
            for frame in self.profileFrameList:
                frame.pack_forget()
            self.profileFrameList = []
        except:
            print('could not forget')
        
        for profile in profiles:
            
            data = profile.split(",")
            
            profileFrame = tk.Frame(self)
            profileFrame.pack(side="top", fill="x")

            profileButton = tk.Button(profileFrame,command=lambda arg = data[0] : self.showProfile(arg),text = data[0])
            profileButton.pack(side="top", fill="x")

            self.profileList.append(data[0])
            self.profileFrameList.append(profileFrame)
        
        self.dataFrame.pack(side='left')
        self.plotFrame.pack(side='left')

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

        deleteButton = tk.Button(self.plotFrame, command=lambda:self.deleteProfile(data), text = 'Delete')
        deleteButton.pack(side='top')
    
    def deleteProfile(self, profileName):

        f = open("profiles.csv", 'r')
        profiles = f.readlines()
        f.close()

        f = open("profiles.csv", 'w')

        found = False
        for profile in profiles:
            
            data = profile.split(",")

            #if(data[0] != profileName[0] and found):
            #    data[0] = 'Profile #' + str(int(data[0][-1]) - 1)
            #    f.write(",".join(data))
            if(data[0] != profileName[0]):
                f.write(profile)
            else:
                found = True
        
        f.close()
        self.showProfileButtons()
                
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
    
    def clear_dataFrame(self):
        for widgets in self.dataFrame.winfo_children():
            widgets.destroy()
    
    def clear_plotFrame(self):
        for widgets in self.plotFrame.winfo_children():
            widgets.destroy()


        

            

