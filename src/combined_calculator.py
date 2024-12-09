import tkinter as tk
from matplotlib import pyplot as plt
import numpy as np
from tkinter import ttk, messagebox
from datapoint import DataPoint
from utilities import (
    convert_to_celsius, calculate_initial_temperature, calculate_C, 
    calculate_k, calculate_time, calculate_temperature
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CombinedCalculator:
   # combined_calculator.py modifications
    def __init__(self, parent, plot_frame):
        self.parent = parent
        self.plot_frame = plot_frame
        self.data_points = []
        
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        
        # Input container
        input_container = ttk.Frame(parent)
        input_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Room temperature frame
        room_temp_frame = ttk.LabelFrame(input_container, text="Room Temperature", padding=10)
        room_temp_frame.pack(fill=tk.X, pady=(0, 10))
        
        temp_frame = ttk.Frame(room_temp_frame)
        temp_frame.pack(fill=tk.X)
        ttk.Label(temp_frame, text="Temperature:", width=12).pack(side=tk.LEFT, padx=5)
        self.room_temp = ttk.Entry(temp_frame, width=15)
        self.room_temp.pack(side=tk.LEFT, padx=5)
        self.room_temp_unit = ttk.Combobox(temp_frame, values=["Celsius", "Kelvin", "Fahrenheit"], 
                                        width=12, state="readonly")
        self.room_temp_unit.pack(side=tk.LEFT, padx=5)
        self.room_temp_unit.set("Celsius")
        
        # Calculation mode frame
        calc_mode_frame = ttk.LabelFrame(input_container, text="Calculation Mode", padding=10)
        calc_mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.calc_mode = tk.StringVar(value="time")
        mode_frame = ttk.Frame(calc_mode_frame)
        mode_frame.pack(fill=tk.X)
        for text, value in [("Calculate Time", "time"), 
                        ("Calculate Temperature", "temp"),
                        ("Calculate Initial Temperature", "initial_temp")]:
            ttk.Radiobutton(mode_frame, text=text, variable=self.calc_mode, 
                        value=value).pack(side=tk.LEFT, padx=10)
        
        # Data points frame
        data_frame = ttk.LabelFrame(input_container, text="Data Points", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Column headers
        headers_frame = ttk.Frame(data_frame)
        headers_frame.pack(fill=tk.X, pady=(0, 5))

        # Configure grid columns with fixed widths
        for i in range(4):
            headers_frame.columnconfigure(i, weight=1, minsize=100)

        # Headers with exact widths matching DataPoint fields
        column_configs = [
            ("Time", 15),
            ("Unit", 12),
            ("Temperature", 15),
            ("Unit", 12)
        ]

        for col, (text, width) in enumerate(column_configs):
            ttk.Label(headers_frame, text=text, width=width, style='Header.TLabel').grid(
                row=0, column=col, padx=5, pady=2, sticky='ew'
            )

        # Data points container with matching grid layout
        self.points_container = ttk.Frame(data_frame)
        self.points_container.pack(fill=tk.BOTH, expand=True)
        for i in range(4):
            self.points_container.columnconfigure(i, weight=1, minsize=100)

        # Buttons frame
        button_frame = ttk.Frame(data_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="Add Row", command=self.add_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Row", command=self.remove_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calculate", command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(input_container, text="Results", padding=10)
        results_frame.pack(fill=tk.X)
        
        self.result_label = ttk.Label(results_frame, text="", justify=tk.LEFT)
        self.result_label.pack(fill=tk.X, pady=5)
        self.param_label = ttk.Label(results_frame, text="", justify=tk.LEFT)
        self.param_label.pack(fill=tk.X, pady=5)
        
        # Add initial rows
        self.add_row()
        self.add_row()

    def add_row(self):
        row = DataPoint(self.points_container, len(self.data_points))
        self.data_points.append(row)
        
    def remove_row(self):
        if len(self.data_points) > 1:
            point = self.data_points.pop()
            point.time_entry.destroy()
            point.time_unit.destroy()
            point.temp_entry.destroy()
            point.temp_unit.destroy()

    def calculate(self):
        try:
            T_ambient = convert_to_celsius(float(self.room_temp.get()), self.room_temp_unit.get())
            points = []
            all_points = []
            
            # Collect all points with their original units
            for i, point in enumerate(self.data_points):
                values = point.get_values()
                if values:
                    time, temp, time_unit = values
                    points.append((time, temp, time_unit))  # time is now in seconds
                    all_points.append((i, time, temp, True, time_unit))
                else:  # Incomplete point
                    time_value = point.time_entry.get()
                    temp_value = point.temp_entry.get()
                    time_unit = point.time_unit.get()
                    
                    if self.calc_mode.get() == "time" and temp_value:
                        temp = convert_to_celsius(float(temp_value), point.temp_unit.get())
                        all_points.append((i, None, temp, False, time_unit))
                    elif self.calc_mode.get() == "temp" and time_value:
                        # Convert time to seconds
                        time = float(time_value)
                        if time_unit == "Minutes":
                            time *= 60
                        elif time_unit == "Hours":
                            time *= 3600
                        all_points.append((i, time, None, False, time_unit))
                    elif self.calc_mode.get() == "initial_temp":
                        all_points.append((i, None, None, False, time_unit))
                
            if len(points) < 2:
                messagebox.showerror("Error", "Need at least 2 complete data points")
                return
            
            t1, T1, _ = points[0]  # t1 is in seconds
            t2, T2, _ = points[1]  # t2 is in seconds
            
            # Calculate parameters (k will be in per second)
            k = calculate_k(T1, T2, T_ambient, t1, t2)
            C = calculate_C(T1, T_ambient)
            
            if self.calc_mode.get() == "initial_temp":
                initial_temp_celsius = calculate_initial_temperature(T1, T_ambient, k, t1)
                # Display initial temperature based on the combobox selection
                if self.room_temp_unit.get() == "Kelvin":
                    display_temp = initial_temp_celsius + 273.15
                elif self.room_temp_unit.get() == "Fahrenheit":
                    display_temp = initial_temp_celsius * 9.0/5.0 + 32
                else:
                    display_temp = initial_temp_celsius

                results_text = f"Initial Temperature = {display_temp:.2f} {self.room_temp_unit.get()}"
                self.result_label.config(text=results_text)
                self.plot_results(T1, T_ambient, k, C, initial_temp=initial_temp_celsius)
                return
            
            # Calculate results for all points
            results = []
            for idx, time, temp, is_complete, time_unit in all_points:
                if is_complete:
                    results.append(f"Row {idx+1}: Complete data point")
                    continue
                    
                if self.calc_mode.get() == "time" and temp is not None:
                    time = calculate_time(temp, T_ambient, T1, k)
                    # display time based on the combobox selection
                    if time_unit == "Minutes":
                        time /= 60
                    elif time_unit == "Hours":
                        time /= 3600
                    results.append(f"Row {idx+1}: Time = {time:.2f} {time_unit}")
                
                elif self.calc_mode.get() == "temp" and time is not None:
                    temp = calculate_temperature(T1, T_ambient, k, time)
                    # display temperature based on the combobox selection
                    if self.room_temp_unit.get() == "Kelvin":
                        temp += 273.15
                    elif self.room_temp_unit.get() == "Fahrenheit":
                        temp = temp * 9.0/5.0 + 32
                    results.append(f"Row {idx+1}: Temperature = {temp:.2f} {self.room_temp_unit.get()}")
            
            # Update result labels with more detailed information
            results_text = "Results:\n" + "\n".join(results)
            self.result_label.config(text=results_text)
            
            # Plot results
            self.plot_results(T1, T_ambient, k, C)
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numerical values")

    def clear(self): 
        self.room_temp.delete(0, tk.END)
        for point in self.data_points:
            point.clear()
        self.result_label.config(text="")
        self.param_label.config(text="")
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def plot_results(self, T_initial, T_ambient, k, C, initial_temp=None):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        if initial_temp is not None and self.calc_mode.get() == "initial_temp":
            T_initial = initial_temp

        # Get current units
        temp_unit = self.room_temp_unit.get()
        
        # Get time unit from first complete data point
        time_unit = "Minutes"  # default
        for point in self.data_points:
            if point.get_values():
                time_unit = point.time_unit.get()
                break
        
        # Calculate max time based on cooling rate
        cooling_time = -1/k * np.log(0.01)  # Time to reach 99% of cooling
        max_time = min(max(cooling_time * 1.2, 3600), 7200)  # Between 1-2 hours
        times = np.linspace(0, max_time, 1000)
        
        # Convert time axis based on unit
        display_times = times.copy()
        if time_unit == "Minutes":
            display_times /= 60
        elif time_unit == "Hours":
            display_times /= 3600
        
        # Calculate temperatures in Celsius
        temperatures = [calculate_temperature(T_initial, T_ambient, k, t) for t in times]
        
        # Convert temperatures if needed
        if temp_unit == "Kelvin":
            temperatures = [t + 273.15 for t in temperatures]
            T_ambient += 273.15
            T_initial += 273.15
        elif temp_unit == "Fahrenheit":
            temperatures = [t * 9.0/5.0 + 32 for t in temperatures]
            T_ambient = T_ambient * 9.0/5.0 + 32
            T_initial = T_initial * 9.0/5.0 + 32

        # Create figure with better size
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Plot with improved styling
        ax.plot(display_times, temperatures, 'b-', linewidth=2, label='Temperature curve')
        ax.axhline(y=T_ambient, color="r", linestyle="--", label="Ambient Temperature")
        
        # Set labels and title
        ax.set_xlabel(f'Time ({time_unit})')
        ax.set_ylabel(f'Temperature ({temp_unit})')
        ax.set_title("Newton's Law of Cooling")
        
        # Add grid and improve appearance
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='best')
        
        # Calculate annotation positions in display units
        time_max_display = max_time
        if time_unit == "Minutes":
            time_max_display /= 60
        elif time_unit == "Hours":
            time_max_display /= 3600
        
        # Add annotations
        ax.annotate(f'Initial: {T_initial:.1f}°{temp_unit[0]}', 
                    xy=(0, T_initial),
                    xytext=(time_max_display*0.1, T_initial+2),
                    arrowprops=dict(arrowstyle='->'))
        ax.annotate(f'Ambient: {T_ambient:.1f}°{temp_unit[0]}',
                    xy=(time_max_display, T_ambient),
                    xytext=(time_max_display*0.8, T_ambient+2),
                    arrowprops=dict(arrowstyle='->'))

        # Display plot
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)