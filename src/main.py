# main.py
import tkinter as tk
from tkinter import ttk
from combined_calculator import CombinedCalculator

# Create main window
window = tk.Tk()
window.title("Newton's Law of Cooling Calculator")
window.geometry("1500x800")


# Configure main window grid with consistent padding
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=0)  # Title row
window.rowconfigure(1, weight=1)  # Content row

# Title frame with consistent padding
title_frame = ttk.Frame(window, padding="20")  # Increased padding
title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)  # Added padding

title_text = "Program Created by: Kendra Clarisse I. Gonzales\nStubcode: 742\nFinal Project: Newton's Law of Cooling Calculator"
title_label = ttk.Label(title_frame, text=title_text, justify=tk.CENTER, font=('Arial', 14, 'bold'))
title_label.pack(pady=15)  # Increased padding

# Main content frame with balanced spacing
main_frame = ttk.Frame(window, padding="20")  # Increased padding
main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))  # Added consistent padding
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

# Input section (left side) with consistent spacing
input_frame = ttk.Frame(main_frame)
input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))  # Balanced padding between sections

# Plot section (right side)
plot_frame = ttk.Frame(main_frame)
plot_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))  # Balanced padding between sections

# Create calculator instance
calculator = CombinedCalculator(input_frame, plot_frame)

window.mainloop()