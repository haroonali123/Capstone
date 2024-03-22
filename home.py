import tkinter as tk
from page import Page
import time
import threading
import MFC
import random
import Thermotron

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.flowRate1_frame = tk.Frame(self)
        self.flowRate2_frame = tk.Frame(self)
        self.flowRate3_frame = tk.Frame(self)
        self.flowRate4_frame = tk.Frame(self)

        self.temp_frame = tk.Frame(self)
        self.humidity_frame = tk.Frame(self)
        self.interval_frame = tk.Frame(self)
        self.intervalTimeLeft_frame = tk.Frame(self)

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

        t1 = threading.Thread(target=self.pollMFC, daemon=True)
        t1.start()

        #t2 = threading.Thread(target=self.pollThermotron, daemon=True)
        #t2.start()

    def pollSensors(self):
        while(1):
            pass
    
    def pollThermotron(self):
        thermotron = Thermotron.Thermotron('COM4')
        while(1):
            thermotron.poll_experiment()

            tempValue_label = tk.Label(self.temp_frame, text = thermotron.temp, font=('calibre',10, 'bold'))
            humidityValue_label = tk.Label(self.humidity_frame, text = thermotron.humidity, font=('calibre',10, 'bold'))
            intervalValue_label = tk.Label(self.interval_frame, text = thermotron.interval, font=('calibre',10, 'bold'))
            timeLeftValue_label = tk.Label(self.intervalTimeLeft_frame, text = thermotron.intervaltimeleft, font=('calibre',10, 'bold'))

            tempValue_label.pack(side='left')
            humidityValue_label.pack(side='left')
            intervalValue_label.pack(side='left')
            timeLeftValue_label.pack(side='left')

            time.sleep(1)

            self.temp_frame.winfo_children()[1].destroy()
            self.humidity_frame.winfo_children()[1].destroy()
            self.interval_frame.winfo_children()[1].destroy()
            self.intervalTimeLeft_frame.winfo_children()[1].destroy()

    
    def pollMFC(self):
        #MFC1_port = 'COM4'
        #MFC1 = MFC.MFC_device(MFC1_port)

        while(1):

            flowRate1 = random.randint(1,100)
            flowRate2 = random.randint(1,100)
            flowRate3 = random.randint(1,100)
            flowRate4 = random.randint(1,100)

            #flowRate1 = MFC1.getFlowRate('02')
            #flowRate2 = MFC1.getFlowRate('04')
            #flowRate3 = MFC1.getFlowRate('06')
            #flowRate4 = MFC1.getFlowRate('08')

            flowRate1Value_label = tk.Label(self.flowRate1_frame, text = flowRate1, font=('calibre',10, 'bold'))
            flowRate2Value_label = tk.Label(self.flowRate2_frame, text = flowRate2, font=('calibre',10, 'bold'))
            flowRate3Value_label = tk.Label(self.flowRate3_frame, text = flowRate3, font=('calibre',10, 'bold'))
            flowRate4Value_label = tk.Label(self.flowRate4_frame, text = flowRate4, font=('calibre',10, 'bold'))

            flowRate1Value_label.pack(side='left')
            flowRate2Value_label.pack(side='left')
            flowRate3Value_label.pack(side='left')
            flowRate4Value_label.pack(side='left')
            
            time.sleep(1)

            self.flowRate1_frame.winfo_children()[1].destroy()
            self.flowRate2_frame.winfo_children()[1].destroy()
            self.flowRate3_frame.winfo_children()[1].destroy()
            self.flowRate4_frame.winfo_children()[1].destroy()


            

