import tkinter as tk
from tkinter import ttk

def initiate_fluidics_gui():
    root = tk.Tk()
    root.title("Fluidics Control")

    # Initialize variables
    speeds = {
        "Stripping Solution": 0.0,
        "PBST Short": 0.0,
        "PBS": 0.0,
        "Hybridization": 0.0,
        "Ligation Buffer": 0.0,
        "Ligation Solution": 0.0,
        "PBST Long": 0.0,
        "Imaging Buffer": 0.0,
    }

    time_between_stages = tk.StringVar()
    shaker_duration = tk.StringVar()
    shaker_duration.set("0.075")
    skip_stages = {stage: tk.IntVar() for stage in speeds}

    def start_fluidics():
        user_input = {
            "speeds": {stage: float(speed_vars[stage].get()) * 100 if speed_vars[stage].get() else 0 for stage in speeds},
            "time_between_stages": int(time_between_stages.get()),
            "shaker_duration": float(shaker_duration.get()),
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
        ttk.Label(fluidics_speeds_frame, text=f"{stage} Speed (mL/min):").grid(row=i, column=0, padx=5, pady=5, sticky='e')
        speed_var = tk.StringVar(value=str(speed))  # Create a StringVar for the Entry
        speed_entries[stage] = ttk.Entry(fluidics_speeds_frame, textvariable=speed_var)
        speed_entries[stage].grid(row=i, column=1, padx=5, pady=5)
        speed_vars[stage] = speed_var  # Store the StringVar
        ttk.Checkbutton(fluidics_speeds_frame, text=f"Skip {stage}", variable=skip_stages[stage], command=lambda stage_name=stage: update_speed_entries(stage_name)).grid(row=i, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(root, text="Time Between Stages (seconds):").pack()
    ttk.Entry(root, textvariable=time_between_stages).pack()

    ttk.Label(root, text="Shaker Step Duration (seconds):").pack()
    ttk.Entry(root, textvariable=shaker_duration).pack()

    ttk.Button(root, text="Start Fluidics", command=start_fluidics).pack()

    root.mainloop()

    return {
        "speeds": {stage: float(speed_vars[stage].get()) * 100 if speed_vars[stage].get() else 0 for stage in speeds},  # Multiply by 100 here
        "time_between_stages": int(time_between_stages.get()),
        "shaker_duration": float(shaker_duration.get()),
        "skip_stages": {stage: skip_stages[stage].get() for stage in speeds}
    }
    
    
    """ THIS IS THE EXAMPLE CODE FOR HOW TO ACCESS THE DATA 
if __name__ == "__main__":
    user_data = initiate_fluidics_gui()
    print("Collected User Data:")
    print("Speeds:", user_data["speeds"])
    print("Time Between Stages:", user_data["time_between_stages"])
    print("Shaker Duration:", user_data["shaker_duration"])
    print("Skip Stages:", user_data["skip_stages"])
    
    """
