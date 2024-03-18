import tkinter as tk
from page import Page

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #label = tk.Label(self, text="Run Profile")
        #label.pack(side="top", fill="both", expand=True)