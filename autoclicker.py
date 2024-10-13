import tkinter as tk
import threading
import keyboard
import time
import ctypes
import sys

# Access the Windows API via ctypes
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Constants for mouse events
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

clicking = False  # Global flag for clicking
escpress = False  # Emergency stop flag

click_type = 'left'  # Default click type
trigger_key = 'f6'  # Default hotkey
previous_trigger_key = None  # Keep track of previous hotkey

def click():
    """Simulate a mouse click based on selected click type."""
    if click_type == 'left':
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif click_type == 'right':
        user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

def start_clicking(cps):
    """Start the autoclicker loop."""
    global clicking
    while clicking:
        if keyboard.is_pressed('esc'):
            emergency_stop()
            break
        click()
        time.sleep(1 / cps)

def start_click_thread(cps):
    """Start clicking in a separate thread with a 5-second delay."""
    global clicking
    clicking = True
    print("Starting in 2 seconds...")
    time.sleep(2)  # Wait 5 seconds before starting
    thread = threading.Thread(target=start_clicking, args=(cps,))
    thread.start()

def stop_clicking():
    """Stop the clicking loop."""
    global clicking
    clicking = False

def on_start_stop():
    """Toggle start/stop when the chosen function key is pressed."""
    global clicking
    if clicking:
        stop_clicking()
    else:
        try:
            cps = float(cps_entry.get())
            if cps <= 0:
                raise ValueError
            start_click_thread(cps)
        except ValueError:
            print("Invalid CPS value. Please enter a positive number.")

def set_click_type():
    """Set the click type based on user selection (left or right)."""
    global click_type
    click_type = click_var.get()

def set_trigger_key(event):
    """Set the trigger key based on dropdown selection."""
    global trigger_key, previous_trigger_key

    # Remove the previous hotkey only if it was set
    if previous_trigger_key is not None:
        keyboard.remove_hotkey(previous_trigger_key)
    
    trigger_key = trigger_var.get()
    previous_trigger_key = trigger_key

    # Add the new hotkey for start/stop
    keyboard.add_hotkey(trigger_key, on_start_stop)

def emergency_stop():
    """Handle emergency stop (Esc key)."""
    stop_clicking()
    sys.exit("Emergency stop triggered. Program terminated.")

# Create the main GUI window
root = tk.Tk()
root.title("Autoclicker")
root.geometry("500x450")  # Increased the size of the window to ensure enough space
root.configure(bg="#282c34")  # Set background color
root.attributes('-topmost', True)  # Always on top

# Title label
title_label = tk.Label(root, text="Autoclicker", font=("Helvetica", 20), fg="white", bg="#282c34")
title_label.pack(pady=20)

# CPS input label and entry
cps_label = tk.Label(root, text="Clicks per second (CPS):", font=("Helvetica", 14), fg="white", bg="#282c34")
cps_label.pack(pady=10)

cps_entry = tk.Entry(root, font=("Helvetica", 14), width=10)
cps_entry.pack(pady=10)

# Radio buttons for left/right click selection
click_var = tk.StringVar(value='left')  # Default to left click

left_radio = tk.Radiobutton(root, text="Left Click", variable=click_var, value='left', command=set_click_type, font=("Helvetica", 14), bg="#282c34", fg="white", selectcolor="#3f444a")
left_radio.pack(pady=5)

right_radio = tk.Radiobutton(root, text="Right Click", variable=click_var, value='right', command=set_click_type, font=("Helvetica", 14), bg="#282c34", fg="white", selectcolor="#3f444a")
right_radio.pack(pady=5)

# Dropdown for selecting trigger key (F1 to F12)
trigger_var = tk.StringVar(value='f6')
trigger_label = tk.Label(root, text="Select Trigger Key (F1-F12):", font=("Helvetica", 14), fg="white", bg="#282c34")
trigger_label.pack(pady=10)

trigger_dropdown = tk.OptionMenu(root, trigger_var, 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', command=set_trigger_key)
trigger_dropdown.config(font=("Helvetica", 14), bg="#3f444a", fg="white", width=10)
trigger_dropdown.pack(pady=10)

# Start/Stop button
start_stop_button = tk.Button(root, text="Start/Stop", command=on_start_stop, font=("Helvetica", 14), bg="#61afef", fg="black", width=20, height=2)
start_stop_button.pack(pady=20)

# Bind the 'Esc' key to the emergency stop
root.bind('<Escape>', lambda event: emergency_stop())

# Start the Tkinter event loop
root.mainloop()
