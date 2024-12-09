import numpy as np

def convert_to_celsius(temp, unit):
    if unit == "Celsius":
        return temp
    elif unit == "Kelvin":
        return temp - 273.15
    elif unit == "Fahrenheit":
        return (temp - 32) * 5.0/9.0
    
def calculate_initial_temperature(T_t, T_a, k, t):  
    T_0 = (T_t - T_a) * np.exp(k * t) + T_a  
    return T_0  


def calculate_C(T_initial, T_ambient):
    """Calculate integration constant C = T_initial - T_ambient"""
    return T_initial - T_ambient

def calculate_k(T1, T2, T_ambient, t1, t2, time_unit="Seconds", temp_unit="Celsius"):
    """Calculate cooling constant k based on the given time and temperature units"""
    # Convert temperatures to Celsius
    T1 = convert_to_celsius(T1, temp_unit)
    T2 = convert_to_celsius(T2, temp_unit)
    T_ambient = convert_to_celsius(T_ambient, temp_unit)
    
    # Convert k based on time unit
    if time_unit == "Minutes":
        time_factor = 1/60
    elif time_unit == "Hours":
        time_factor = 1/3600
    else:  # Seconds
        time_factor = 1

    k = -1 * (np.log((T2 - T_ambient)/(T1 - T_ambient)) / ((t2 - t1) * time_factor))
    return k

def calculate_time(T_t, T_a, T_0, k):
    """Calculate time using T = T_amb + (T_initial - T_amb)e^(-kt)"""
    time = -1/k * np.log((T_t - T_a)/(T_0 - T_a))
    return time

def calculate_temperature(T_initial, T_ambient, k, time):
    """Calculate temperature using T = T_amb + (T_initial - T_amb)e^(-kt)"""
    return T_ambient + (T_initial - T_ambient) * np.exp(-k * time)