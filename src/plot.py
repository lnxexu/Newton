import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

def plot_results(T_initial, T_ambient, k, C, parent):
    for widget in parent.winfo_children():
        widget.destroy()
        
    # Use more points for smoother curve and adjust time range
    max_time = 200  # seconds
    time = np.linspace(0, max_time, 1000)
    temperature = T_ambient + C * np.exp(-k * time)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(time/60, temperature, 'b-', linewidth=2)  # Convert to minutes for display
    ax.axhline(y=T_ambient, color="r", linestyle="--", label="Ambient Temperature")
    ax.set(xlabel='Time (minutes)', 
           ylabel='Temperature (°C)',
           title='Newton\'s Law of Cooling')
    
    # Add grid and improve appearance
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    
    # Add initial and ambient temperature annotations
    ax.annotate(f'Initial: {T_initial:.1f}°C', xy=(0, T_initial), 
                xytext=(10, T_initial+2), arrowprops=dict(arrowstyle='->'))
    ax.annotate(f'Ambient: {T_ambient:.1f}°C', xy=(max_time/60, T_ambient),
                xytext=(max_time/60-20, T_ambient+2), arrowprops=dict(arrowstyle='->'))
    
    canvas = FigureCanvasTkAgg(fig, parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)