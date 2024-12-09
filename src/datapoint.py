import tkinter as tk
from tkinter import ttk
from utilities import convert_to_celsius

class DataPoint:
    def __init__(self, parent, row):
        # Create widgets with matching widths
        self.time_entry = ttk.Entry(parent, width=15)
        self.time_unit = ttk.Combobox(parent, values=["Seconds", "Minutes", "Hours"],
                                     width=12, state="readonly")
        self.temp_entry = ttk.Entry(parent, width=15)
        self.temp_unit = ttk.Combobox(parent, values=["Celsius", "Kelvin", "Fahrenheit"],
                                     width=12, state="readonly")
        
        # Grid layout with consistent spacing
        self.time_entry.grid(row=row, column=0, padx=5, pady=2, sticky='ew')
        self.time_unit.grid(row=row, column=1, padx=5, pady=2, sticky='ew')
        self.temp_entry.grid(row=row, column=2, padx=5, pady=2, sticky='ew')
        self.temp_unit.grid(row=row, column=3, padx=5, pady=2, sticky='ew')
        
        # Set defaults
        self.time_unit.set("Seconds")
        self.temp_unit.set("Celsius")

    def get_values(self):
        if self.time_entry.get() and self.temp_entry.get():
            raw_time = float(self.time_entry.get())
            if self.time_unit.get() == "Minutes":
                time = raw_time * 60
            elif self.time_unit.get() == "Hours":
                time = raw_time * 3600
            else:
                time = raw_time
                
            temp = convert_to_celsius(float(self.temp_entry.get()), self.temp_unit.get())
            return time, temp, self.time_unit.get()
        return None

    def clear(self):
        self.time_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.time_unit.set("Seconds")
        self.temp_unit.set("Celsius")