import tkinter as tk
from tkinter import ttk, simpledialog
import mvp
import gsioc
import serial
from serial.tools import list_ports

# this is so we can pass these back into our fluidics code 


def list_available_com_ports():
    com_ports = [port.device for port in serial.tools.list_ports.comports()]
    return com_ports

class DropdownDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="Select a COM Port:").grid(row=0, column=0)
        self.combobox = ttk.Combobox(master, values=list_available_com_ports())
        self.combobox.grid(row=0, column=1)
        self.combobox.set(list_available_com_ports()[0])
        return self.combobox

    def apply(self):
        self.result = self.combobox.get()
    
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
        print("User Input - Fluid Controls:")
        print(user_input)
        root.destroy()
        # Implement the fluidics control logic here

    def update_speed_entries(stage_name):
        if skip_stages[stage_name].get() == 1:
            speed_entries[stage_name].delete(0, tk.END)
            speed_entries[stage_name].config(state=tk.DISABLED)
        else:
            speed_entries[stage_name].config(state=tk.NORMAL)

    def control_arduino():
        dialog = DropdownDialog(root, "Select COM Port")
        selected_port = dialog.result
        if selected_port:
            global ser
            print(f"Connecting to Arduino on COM Port: {selected_port}")
            try:
                ser = serial.Serial(selected_port, baudrate=9600)
                print("Successful Connection to Arduino")
            except serial.SerialException as e:
                print(f"Serial connection error: {e}")

    # TODO: Make mvp throw an error when trying to connect
    def control_valve_positioner():
        dialog = DropdownDialog(root, "Select COM Port")
        selected_port = dialog.result
        if selected_port:
            global mvp1
            print(f"Connecting to Valve Positioner on COM Port: {selected_port}")
            mvp1 = mvp.MVP()
            try:
                mvp1.connect(selected_port)
                print("Successful Connection to Valve Positioner")
            except Exception as e:
                print(f"Failed to connect: {e}")

    def control_pump():
        dialog = DropdownDialog(root, "Select COM Port")
        selected_port = dialog.result
        if selected_port:
            global pump
            print(f"Connecting to Pump on COM Port: {selected_port}")
            pump = gsioc.GSIOC()
            try:
                pump.connect(selected_port)
                print("Successful Connection to Pump")
            except Exception as e:
                print(f"Failed to connect: {e}")



    def set_servo_angle():
        angle = simpledialog.askfloat("Set Servo Angle", "Enter Servo Angle:")
        if angle is not None:
            # Implement sending angle to the servo control logic here
            print(f"Set Servo Angle: {angle}")
            try:
                # Initialize the serial connection
                # Adjust the baud rate as needed
                # Send the angle command to the Arduino
                command = f"MOVE {angle}\n"
                ser.write(command.encode())
                """this code waits until "True" is recieved from the arduino code"""
                while True:
                    completion_message = (ser.readline().decode().strip())
                    if(completion_message):
                        break
            except serial.SerialException as e:
                # Handle the connection error
                print(f"Serial connection error: {str(e)}")
            except Exception as e:
                # Handle other exceptions
                print(f"Error: {str(e)}")


    # Create and lay out the GUI components
    fluid_controls_frame = ttk.LabelFrame(root, text="Fluid Controls")
    fluid_controls_frame.pack(padx=10, pady=10, fill='both', expand=True)

    fluidics_speeds_frame = ttk.Frame(fluid_controls_frame)
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

    ttk.Label(fluid_controls_frame, text="Time Between Stages (seconds):").pack()
    ttk.Entry(fluid_controls_frame, textvariable=time_between_stages).pack()

    # "Start Fluidics" button
    ttk.Button(fluid_controls_frame, text="Start Fluidics", command=start_fluidics).pack()

    # Create the "Connect" section
    connect_frame = ttk.LabelFrame(root, text="Connect")
    connect_frame.pack(side='left', padx=10, pady=10, fill='y')

    # Buttons for connecting and controlling instruments
    ttk.Button(connect_frame, text="Connect to Arduino", command=control_arduino).pack()
    ttk.Button(connect_frame, text="Connect to Pump", command=control_pump).pack()
    ttk.Button(connect_frame, text="Connect to Valve Positioner", command=control_valve_positioner).pack()

    # Create the "Shaker Controls" section
    shaker_controls_frame = ttk.LabelFrame(root, text="Shaker Controls")
    shaker_controls_frame.pack(side='right', padx=10, pady=10, fill='y')

    ttk.Label(shaker_controls_frame, text="Set Shaker Duration Step (seconds):").pack()
    ttk.Entry(shaker_controls_frame, textvariable=shaker_duration).pack()
    ttk.Button(shaker_controls_frame, text="Set Servo Angle", command=set_servo_angle).pack()

    root.mainloop()

    return {
        "speeds": {stage: float(speed_vars[stage].get()) * 100 if speed_vars[stage].get() else 0 for stage in speeds},  # Multiply by 100 here
        "time_between_stages": int(time_between_stages.get()),
        "shaker_duration": float(shaker_duration.get()),
        "skip_stages": {stage: skip_stages[stage].get() for stage in speeds},
        "pump" : pump,
        "mvp" : mvp1,
        "servo" : ser
    }

# Example code for accessing user data
if __name__ == "__main__":
    user_data = initiate_fluidics_gui()
    print("Collected User Data:")
    print("Speeds:", user_data["speeds"])
    print("Time Between Stages:", user_data["time_between_stages"])
    print("Shaker Duration:", user_data["shaker_duration"])
    print("Skip Stages:", user_data["skip_stages"])
