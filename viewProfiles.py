import tkinter as tk
from page import Page

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #label = tk.Label(self, text="View Profiles")
        #label.pack(side="top", fill="both", expand=True)