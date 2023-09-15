import tkinter as tk
from tkinter import ttk
import time

# Initialize variables
speeds = {
    "Stripping Solution": 0,
    "PBST-Short": 0,
    "PBS": 0,
    "Hybridization": 0,
    "Ligation Buffer": 0,
    "Ligation Solution": 0,
    "PBST-Long": 0,
    "Imaging Buffer": 0,
}

time_between_stages = 0
shaker_duration = 0
skip_stages = []

# Function to start the fluidics process
def start_fluidics():
    global speeds, time_between_stages, shaker_duration, skip_stages
    time_between_stages = int(time_between_stages_entry.get())
    shaker_duration = int(shaker_duration_entry.get())
    skip_stages = [stage_name for stage_name, stage_var in stage_vars.items() if stage_var.get() == 1]
    
    status_label.config(text="Fluidics process started...")
    
    # Print the speed values
    for stage_name, speed_entry in speed_entries.items():
        speed_value = speed_entry.get()
        print(f"{stage_name} Speed: {speed_value} m/s")
    # Implement your fluidics control logic here
    # You can access speeds["StageName"] to get the speed for each stage
    # You can access time_between_stages, shaker_duration, and skip_stages
    
    time.sleep(2)  # Simulate fluidics operation for 2 seconds
    
    status_label.config(text="Fluidics process complete.")

# Function to disable speed input fields for skipped stages
def update_speed_entries(stage_name):
    if stage_vars[stage_name].get() == 1:
        speed_entries[stage_name].delete(0, tk.END)
        speed_entries[stage_name].config(state=tk.DISABLED)
    else:
        speed_entries[stage_name].config(state=tk.NORMAL)

# Create the main application window
root = tk.Tk()
root.title("Fluidics Control")

# Fluidics Speeds Table
fluidics_speeds_frame = ttk.Frame(root)
fluidics_speeds_frame.pack()

stage_vars = {}
speed_entries = {}

for i, (stage, speed) in enumerate(speeds.items()):
    ttk.Label(fluidics_speeds_frame, text=f"{stage} Speed (m/s):").grid(row=i, column=0, padx=5, pady=5, sticky='e')
    
    stage_vars[stage] = tk.IntVar()
    skip_checkbox = ttk.Checkbutton(fluidics_speeds_frame, text=f"Skip {stage}", variable=stage_vars[stage],
                                   command=lambda stage_name=stage: update_speed_entries(stage_name))
    skip_checkbox.grid(row=i, column=1, padx=5, pady=5, sticky='w')
    
    speed_entries[stage] = ttk.Entry(fluidics_speeds_frame, state=tk.NORMAL)
    speed_entries[stage].grid(row=i, column=2, padx=5, pady=5)

# Time Between Stages Label and Entry
time_between_stages_label = ttk.Label(root, text="Time Between Stages (seconds):")
time_between_stages_label.pack()

time_between_stages_entry = ttk.Entry(root)
time_between_stages_entry.pack()

# Shaker Duration Label and Entry
shaker_duration_label = ttk.Label(root, text="Shaker Duration (seconds):")
shaker_duration_label.pack()

shaker_duration_entry = ttk.Entry(root)
shaker_duration_entry.pack()

# Start Button
start_button = ttk.Button(root, text="Start Fluidics", command=start_fluidics)
start_button.pack()

# Status Label
status_label = ttk.Label(root, text="")
status_label.pack()

# Run the GUI application
root.mainloop()
