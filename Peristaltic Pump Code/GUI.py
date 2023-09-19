import tkinter as tk
from tkinter import ttk
import time

# Initialize variables
"""
OLD CODE FOR THE GUI THAT WASN"T WORKING USED FOR REFERENCE


speeds = {
    "Stripping Solution": 0,
    "PBST Short": 0,
    "PBS": 0,
    "Hybridization": 0,
    "Ligation Buffer": 0,
    "Ligation Solution": 0,
    "PBST Long": 0,
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
        if(speed_value == None):
            print("None")
        print(f"{stage_name} Speed: {speed_value} m/s")
        
        
    # Implement your fluidics control logic here
    # You can access speeds["StageName"] to get the speed for each stage
    # You can access time_between_stages, shaker_duration, and skip_stages
    
    time.sleep(2)  # Simulate fluidics operation for 2 seconds
    
    status_label.config(text="Fluidics process complete.")

# Returns stage speed 
def get_speed_for_stage(stage_name, speeds):
    # Check if the stage name exists in the speeds dictionary
    if stage_name in speeds:
        return speeds[stage_name]
    else:
        # Return a default speed (e.g., 0) if the stage name is not found
        return 0

# Function to disable speed input fields for skipped stages
def update_speed_entries(stage_name):
    if stage_vars[stage_name].get() == 1:
        speed_entries[stage_name].delete(0, tk.END)
        speed_entries[stage_name].config(state=tk.DISABLED)
    else:
        speed_entries[stage_name].config(state=tk.NORMAL)
        """

# Create the main application window


import tkinter as tk
from tkinter import ttk

def initiate_fluidics_gui():
    root = tk.Tk()
    root.title("Fluidics Control")

    # Initialize variables
    speeds = {
        "Stripping Solution": 0,
        "PBST Short": 0,
        "PBS": 0,
        "Hybridization": 0,
        "Ligation Buffer": 0,
        "Ligation Solution": 0,
        "PBST Long": 0,
        "Imaging Buffer": 0,
    }

    time_between_stages = tk.StringVar()
    shaker_duration = tk.StringVar()
    skip_stages = {stage: tk.IntVar() for stage in speeds}

    def start_fluidics():
        user_input = {
            "speeds": {stage: speed_vars[stage].get() for stage in speeds},
            "time_between_stages": int(time_between_stages.get()),
            "shaker_duration": int(shaker_duration.get()),
            "skip_stages": {stage: skip_stages[stage].get() for stage in speeds}
        }
        print("User Input:")
        print(user_input)
        root.destroy()

    def update_speed_entries(stage_name):
        if skip_stages[stage_name].get() == 1:
            speed_entries[stage_name].delete(0, tk.END)
            speed_entries[stage_name].config(state=tk.DISABLED)
        else:
            speed_entries[stage_name].config(state=tk.NORMAL)

    # Create and lay out the GUI components
    fluidics_speeds_frame = ttk.Frame(root)
    fluidics_speeds_frame.pack()

    speed_entries = {}
    speed_vars = {}  # Store StringVar objects for Entry widgets
    for i, (stage, speed) in enumerate(speeds.items()):
        ttk.Label(fluidics_speeds_frame, text=f"{stage} Speed (mL/s):").grid(row=i, column=0, padx=5, pady=5, sticky='e')
        speed_var = tk.StringVar(value=str(speed))  # Create a StringVar for the Entry
        speed_entries[stage] = ttk.Entry(fluidics_speeds_frame, textvariable=speed_var)
        speed_entries[stage].grid(row=i, column=1, padx=5, pady=5)
        speed_vars[stage] = speed_var  # Store the StringVar
        ttk.Checkbutton(fluidics_speeds_frame, text=f"Skip {stage}", variable=skip_stages[stage], command=lambda stage_name=stage: update_speed_entries(stage_name)).grid(row=i, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(root, text="Time Between Stages (seconds):").pack()
    ttk.Entry(root, textvariable=time_between_stages).pack()

    ttk.Label(root, text="Shaker Duration (seconds):").pack()
    ttk.Entry(root, textvariable=shaker_duration).pack()

    ttk.Button(root, text="Start Fluidics", command=start_fluidics).pack()

    root.mainloop()

    return {
        "speeds": {stage: speed_vars[stage].get() for stage in speeds},
        "time_between_stages": int(time_between_stages.get()),
        "shaker_duration": int(shaker_duration.get()),
        "skip_stages": {stage: skip_stages[stage].get() for stage in speeds}
    }

#initiate_fluidics_gui()



# Example of how to use the GUI function and access the collected data
"""
if __name__ == "__main__":
    user_data = initiate_fluidics_gui()
    print("Collected User Data:")
    print("Speeds:", user_data["speeds"])
    print("Time Between Stages:", user_data["time_between_stages"])
    print("Shaker Duration:", user_data["shaker_duration"])
    print("Skip Stages:", user_data["skip_stages"])
"""