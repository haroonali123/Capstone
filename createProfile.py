#Create a new Profile
import tkinter as tk
from page import Page

class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #label = tk.Label(self, text="Create Profiles")
        #label.pack(side="top", fill="both", expand=True)

        self.flowRate1=tk.StringVar()
        self.flowRate2=tk.StringVar()

        entryFrame = tk.Frame(self)
        entryFrame.pack(side="top", fill="x", expand=False)
        flowRate1_label = tk.Label(entryFrame, text = 'Flow Rate 1: ', font=('calibre',10, 'bold'))
        flowRate1_entry = tk.Entry(entryFrame,textvariable = self.flowRate1, font=('calibre',10,'normal'))
        flowRate1_label.pack(side="left", expand=False)
        flowRate1_entry.pack(side="left", fill="x", expand=True)

        
        entryFrame2 = tk.Frame(self)
        entryFrame2.pack(side="top", fill="x", expand=False)
        flowRate2_label = tk.Label(entryFrame2, text = 'Flow Rate 2: ', font=('calibre',10, 'bold'))
        flowRate2_entry = tk.Entry(entryFrame2,textvariable = self.flowRate2, font=('calibre',10,'normal'))
        flowRate2_label.pack(side="left", expand=False)
        flowRate2_entry.pack(side="left", fill="x", expand=True)
        sub_btn=tk.Button(self,text = 'Submit', command=self.getEntryValues)
        sub_btn.pack(side="top")

        #flowRate2=tk.StringVar()

    def getEntryValues(self):
        name=self.flowRate1.get()
        self.saveToCSV()
        print("The flow rate is : " + name)

    def saveToCSV(self):
        f = open("profiles.csv")
        f.write(self.flowRate1 + "," + self.flowRate2)
        f.close()
