#Create a new Profile
import tkinter as tk
from page import Page
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.profile = []

        self.flowRate1=tk.StringVar()
        self.flowRate2=tk.StringVar()
        self.flowRate3=tk.StringVar()
        self.flowRate4=tk.StringVar()
        self.initialTemp=tk.StringVar()
        self.initialHum=tk.StringVar()
        self.finalTemp=tk.StringVar()
        self.finalHum=tk.StringVar()
        self.hours=tk.StringVar()
        self.minutes=tk.StringVar()

        self.intervalTemp=tk.StringVar()
        self.intervalHum=tk.StringVar()
        self.intervalHours=tk.StringVar()
        self.intervalMinutes=tk.StringVar()

        self.yTemp = []
        self.yHum = []
        self.xAxis = []

        entryFrame1 = tk.Frame(self)
        entryFrame1.pack(side="top", fill="x", expand=False)
        flowRate1_label = tk.Label(entryFrame1, text = 'Flow Rate 1: ', font=('calibre',10, 'bold'))
        self.flowRate1_entry = tk.Entry(entryFrame1,textvariable = self.flowRate1, font=('calibre',10,'normal'))
        flowRate1_label.pack(side="left", expand=False)
        self.flowRate1_entry.pack(side="left", fill="x", expand=True)

        entryFrame2 = tk.Frame(self)
        entryFrame2.pack(side="top", fill="x", expand=False)
        flowRate2_label = tk.Label(entryFrame2, text = 'Flow Rate 2: ', font=('calibre',10, 'bold'))
        self.flowRate2_entry = tk.Entry(entryFrame2,textvariable = self.flowRate2, font=('calibre',10,'normal'))
        flowRate2_label.pack(side="left", expand=False)
        self.flowRate2_entry.pack(side="left", fill="x", expand=True)

        entryFrame21 = tk.Frame(self)
        entryFrame21.pack(side="top", fill="x", expand=False)
        flowRate3_label = tk.Label(entryFrame21, text = 'Flow Rate 3: ', font=('calibre',10, 'bold'))
        self.flowRate3_entry = tk.Entry(entryFrame21,textvariable = self.flowRate3, font=('calibre',10,'normal'))
        flowRate3_label.pack(side="left", expand=False)
        self.flowRate3_entry.pack(side="left", fill="x", expand=True)

        entryFrame22 = tk.Frame(self)
        entryFrame22.pack(side="top", fill="x", expand=False)
        flowRate4_label = tk.Label(entryFrame22, text = 'Flow Rate 4: ', font=('calibre',10, 'bold'))
        self.flowRate4_entry = tk.Entry(entryFrame22,textvariable = self.flowRate4, font=('calibre',10,'normal'))
        flowRate4_label.pack(side="left", expand=False)
        self.flowRate4_entry.pack(side="left", fill="x", expand=True)

        entryFrame3 = tk.Frame(self)
        entryFrame3.pack(side="top", fill="x", expand=False)
        initialTemp_label = tk.Label(entryFrame3, text = 'Initial Temperature: ', font=('calibre',10, 'bold'))
        self.initialTemp_entry = tk.Entry(entryFrame3,textvariable = self.initialTemp, font=('calibre',10,'normal'))
        initialTemp_label.pack(side="left", expand=False)
        self.initialTemp_entry.pack(side="left", fill="x", expand=True)

        entryFrame4 = tk.Frame(self)
        entryFrame4.pack(side="top", fill="x", expand=False)
        initialHum_label = tk.Label(entryFrame4, text = 'Initial Humidity: ', font=('calibre',10, 'bold'))
        self.initialHum_entry = tk.Entry(entryFrame4,textvariable = self.initialHum, font=('calibre',10,'normal'))
        initialHum_label.pack(side="left", expand=False)
        self.initialHum_entry.pack(side="left", fill="x", expand=True)

        entryFrame5 = tk.Frame(self)
        entryFrame5.pack(side="top", fill="x", expand=False)
        finalTemp_label = tk.Label(entryFrame5, text = 'Final Temperature: ', font=('calibre',10, 'bold'))
        self.finalTemp_entry = tk.Entry(entryFrame5,textvariable = self.finalTemp, font=('calibre',10,'normal'))
        finalTemp_label.pack(side="left", expand=False)
        self.finalTemp_entry.pack(side="left", fill="x", expand=True)

        entryFrame6 = tk.Frame(self)
        entryFrame6.pack(side="top", fill="x", expand=False)
        finalHum_label = tk.Label(entryFrame6, text = 'Final Humidity: ', font=('calibre',10, 'bold'))
        self.finalHum_entry = tk.Entry(entryFrame6,textvariable = self.finalHum, font=('calibre',10,'normal'))
        finalHum_label.pack(side="left", expand=False)
        self.finalHum_entry.pack(side="left", fill="x", expand=True)

        entryFrame7 = tk.Frame(self)
        entryFrame7.pack(side="top", fill="x", expand=False)
        hours_label = tk.Label(entryFrame7, text = 'Time (Hours): ', font=('calibre',10, 'bold'))
        self.hours_entry = tk.Entry(entryFrame7,textvariable = self.hours, font=('calibre',10,'normal'))
        hours_label.pack(side="left", expand=False)
        self.hours_entry.pack(side="left", fill="x", expand=True)

        entryFrame8 = tk.Frame(self)
        entryFrame8.pack(side="top", fill="x", expand=False)
        minutes_label = tk.Label(entryFrame8, text = 'Time (Minutes): ', font=('calibre',10, 'bold'))
        self.minutes_entry = tk.Entry(entryFrame8,textvariable = self.minutes, font=('calibre',10,'normal'))
        minutes_label.pack(side="left", expand=False)
        self.minutes_entry.pack(side="left", fill="x", expand=True)
        

        self.sub_btn=tk.Button(self,text = 'Submit', command=self.getEntryValues)
        self.sub_btn.pack(side="top")

        self.errorFrame1 = tk.Frame(self)
        self.errorFrame2 = tk.Frame(self)

        self.error_label1 = tk.Label(self.errorFrame1, text = 'Please provide at least 1 Flow Rate', font=('calibre',10, 'bold'), fg='red')
        self.error_label2 = tk.Label(self.errorFrame1, text = 'Please provide all initial and final Temperature and Humidity values', font=('calibre',10, 'bold'), fg='red')
        self.error_label3 = tk.Label(self.errorFrame1, text = 'Please provide a time (Hours and/or Minutes)', font=('calibre',10, 'bold'), fg='red')
        #flowRate2=tk.StringVar()

    def clearEntryFields(self):
        self.finalTemp_entry.delete(0, 'end')
        self.flowRate1_entry.delete(0, 'end')
        self.flowRate2_entry.delete(0, 'end')
        self.initialTemp_entry.delete(0, 'end')
        self.initialHum_entry.delete(0, 'end')
        self.finalHum_entry.delete(0, 'end')
        self.hours_entry.delete(0, 'end')
        self.minutes_entry.delete(0, 'end')
        self.flowRate3_entry.delete(0, 'end')
        self.flowRate4_entry.delete(0, 'end')

    def clearIntervalEntryFields(self):
        pass

    def getEntryValues(self):        
        
        if(not self.flowRate1.get() and not self.flowRate2.get() and not self.flowRate3.get() and not self.flowRate4.get()):
            self.error_label2.pack_forget()
            self.error_label3.pack_forget()
            self.errorFrame1.pack(side="top")
            self.error_label1.pack(side="top", expand=False)
        
        elif(not self.initialTemp.get() or not self.initialHum.get() or not self.finalTemp.get() or not self.finalHum.get()):
            self.error_label1.pack_forget()
            self.error_label3.pack_forget()
            self.errorFrame1.pack(side="top")
            self.error_label2.pack(side="top", expand=False)
        
        elif(not self.hours.get() and not self.minutes.get()):
            self.error_label1.pack_forget()
            self.error_label2.pack_forget()
            self.errorFrame1.pack(side="top")
            self.error_label3.pack(side="top", expand=False)

        else:
            self.error_label1.pack_forget()
            self.error_label2.pack_forget()
            self.error_label3.pack_forget()

            self.profile.append(self.flowRate1.get())
            self.profile.append(self.flowRate2.get())
            self.profile.append(self.flowRate3.get())
            self.profile.append(self.flowRate4.get())
            self.profile.append(self.initialTemp.get())
            self.profile.append(self.initialHum.get())
            self.profile.append(self.finalTemp.get())
            self.profile.append(self.finalHum.get())

            if(not self.hours.get()):
                self.profile.append('0')
            else:
                self.profile.append(self.hours.get())
            
            if(not self.minutes.get()):
                self.profile.append('0')
            else:
                self.profile.append(self.minutes.get())
            
            self.sub_btn.pack_forget()
            self.clearEntryFields()
            self.openNewWindow()

    def saveToCSV(self):

        #Need to initialize csv before
        f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Capstone_Project\\Capstone\\profiles.csv", "r")
        profileNum = len(f.readlines()) + 1
        f.close()

        f = open("C:\\Users\\ppart\\OneDrive\\Desktop\\School Stuff\\Capstone_Project\\Capstone\\profiles.csv", "a")
        f.write("Profile #" + str(profileNum) + "," + ",".join(self.profile) + "\n")
        f.close()
        
        self.profile = []
        self.yHum = []
        self.yTemp =[]
        self.xAxis = []
        self.sub_btn.pack(side="top")

    def openNewWindow(self):
     
        newWindow = tk.Toplevel(self)
        newWindow.title("New Window")
    
        # sets the geometry of toplevel
        newWindow.geometry("600x600")

        plotFrame = tk.Frame(newWindow)
        self.yTemp.append(int(self.profile[4]))
        self.yTemp.append(int(self.profile[6]))

        self.yHum.append(int(self.profile[5]))
        self.yHum.append(int(self.profile[7]))

        time = (int(self.profile[8]) * 60) + int(self.profile[9])
        self.xAxis.append(0)
        self.xAxis.append(time)
        

        fig1 = Figure(figsize = (5, 5),dpi = 100)
        plot1 = fig1.add_subplot(111)
        fig1.suptitle('Program Graph', fontsize=12)
        plot1.plot(self.xAxis,self.yTemp, label='Temperature')
        plot1.plot(self.xAxis,self.yHum, label='Humidity')
        plot1.legend()
        canvas1 = FigureCanvasTkAgg(fig1,plotFrame)   
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left")

        entryFrame1 = tk.Frame(newWindow)
        entryFrame1.pack(side="top", fill="x", expand=False)
        temp_label = tk.Label(entryFrame1, text = 'Temperature: ', font=('calibre',10, 'bold'))
        temp_entry = tk.Entry(entryFrame1,textvariable = self.intervalTemp, font=('calibre',10,'normal'))
        temp_label.pack(side="left", expand=False)
        temp_entry.pack(side="left", fill="x", expand=True)

        entryFrame2 = tk.Frame(newWindow)
        entryFrame2.pack(side="top", fill="x", expand=False)
        hum_label = tk.Label(entryFrame2, text = 'Humidity: ', font=('calibre',10, 'bold'))
        hum_entry = tk.Entry(entryFrame2,textvariable = self.intervalHum, font=('calibre',10,'normal'))
        hum_label.pack(side="left", expand=False)
        hum_entry.pack(side="left", fill="x", expand=True)

        entryFrame3 = tk.Frame(newWindow)
        entryFrame3.pack(side="top", fill="x", expand=False)
        hours_label = tk.Label(entryFrame3, text = 'Time (Hours): ', font=('calibre',10, 'bold'))
        hours_entry = tk.Entry(entryFrame3,textvariable = self.intervalHours, font=('calibre',10,'normal'))
        hours_label.pack(side="left", expand=False)
        hours_entry.pack(side="left", fill="x", expand=True)

        entryFrame4 = tk.Frame(newWindow)
        entryFrame4.pack(side="top", fill="x", expand=False)
        minutes_label = tk.Label(entryFrame4, text = 'Time (Minutes): ', font=('calibre',10, 'bold'))
        minutes_entry = tk.Entry(entryFrame4,textvariable = self.intervalMinutes, font=('calibre',10,'normal'))
        minutes_label.pack(side="left", expand=False)
        minutes_entry.pack(side="left", fill="x", expand=True)

        addInterval_btn=tk.Button(newWindow,text = 'Add Interval', command= lambda : self.addInterval(temp_entry,hum_entry,hours_entry,minutes_entry,plot1,canvas1))
        addInterval_btn.pack(side="top")

        done_btn=tk.Button(newWindow,text = 'Done', command=lambda:[self.saveToCSV(), newWindow.destroy()])
        done_btn.pack(side="top")

        self.errorIntervalFrame1 = tk.Frame(newWindow)
        self.errorIntervalFrame1.pack(side="top")
        self.error_IntervalLabel1 = tk.Label(self.errorIntervalFrame1, text = 'Please provide Temperature and Humidity values', font=('calibre',10, 'bold'), fg='red')
        self.error_IntervalLabel2 = tk.Label(self.errorIntervalFrame1, text = 'Please provide a time (Hours and/or Minutes)', font=('calibre',10, 'bold'), fg='red')

        plotFrame.pack(side="top", expand=False)

    def addInterval(self,temp_entry,hum_entry,hours_entry,minutes_entry,plot,canvas):

        if(not self.intervalTemp.get() or not self.intervalHum.get()):
            self.error_IntervalLabel2.pack_forget()
            #self.errorIntervalFrame1.pack(side="top")
            self.error_IntervalLabel1.pack(side="top", expand=False)
        
        elif(not self.intervalHours.get() and not self.intervalMinutes.get()):
            self.error_IntervalLabel1.pack_forget()
            #self.errorIntervalFrame1.pack(side="top")
            self.error_IntervalLabel2.pack(side="top", expand=False)

        else:
            self.error_IntervalLabel1.pack_forget()
            self.error_IntervalLabel2.pack_forget()

            self.profile.append(self.intervalTemp.get())
            self.profile.append(self.intervalHum.get())

            if(not self.intervalHours.get()):
                self.profile.append('0')
                hours = 0
            else:
                self.profile.append(self.intervalHours.get())
                hours = int(self.intervalHours.get())
            
            if(not self.intervalMinutes.get()):
                self.profile.append('0')
                mins = 0
            else:
                self.profile.append(self.intervalMinutes.get())
                mins = int(self.intervalMinutes.get())
            
            self.yTemp.append(int(self.intervalTemp.get()))
            self.yHum.append(int(self.intervalHum.get()))
            time = (hours * 60) + mins + int(self.xAxis[-1])
            self.xAxis.append(time)

            temp_entry.delete(0, 'end')
            hum_entry.delete(0, 'end')
            hours_entry.delete(0, 'end')
            minutes_entry.delete(0, 'end')

            plot.clear()
            plot.plot(self.xAxis, self.yTemp, label='Temperature')
            plot.plot(self.xAxis, self.yHum, label='Humidity')
            plot.legend()
            canvas.draw()
