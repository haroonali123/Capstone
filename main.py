from createProfile import Page2
from home import Page1
from runProfile import Page3

import tkinter as tk
import os

#Enumerate ports from hub.
MFC1_port = 'COM4'
MFC2_port = ''
MFC3_port = ''
MFC4_port = ''
Thermotron_port = ''
Sensor1 = ''
Sensor2 = ''
Sensor3 = ''

# enumerate all device ports

#Connect to all devices
#MFC1 = MFC.MFC_device(MFC1_port)
#MFC1.getFlowRate('02')

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        if not os.path.isfile("profiles.csv"):
            f = open("profiles.csv", "w")
            f.close()
        
        if not os.path.isfile("devices.json"):
            f = open("devices.json", "w")
            f.close()

        #createProfiles_btn=tk.Button(self,text = 'Create Profile', command = p2.show)
        #createProfiles_btn.grid(row=5,column=0)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)

        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Remove Profiles", command=lambda:[p1.show(), p1.showProfileButtons()])
        b2 = tk.Button(buttonframe, text="Create New Profile", command=p2.show)
        b3 = tk.Button(buttonframe, text="Run Profile", command=lambda:[p3.show(), p3.showProfileButtons()])

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p3.show()
        p3.showProfileButtons()

root = tk.Tk()
main = MainView(root)
root.title("ESI Labview")
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("800x800")
root.mainloop()
