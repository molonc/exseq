import time
import mvp
import gsioc
import datetime
import GUI
from pyfirmata import Arduino, SERVO
from threading import Timer
import threading
import serial
# MVP1:
#   - 1 1* PBS
#   - 2 Hydrbidization Solution
#   - 3 Ligation Buffer
#   - 4 Ligation Solution
#   - 5 Imaging Buffer
#   - 6 PBST
#   - 7 Stripping Solution

# board = Arduino('/dev/tty.usbserial-14310')

# servo_pin = 4

# servo = board.get_pin(f's:{servo_pin}:s')



# Define the COM port (change this to your specific COM port) using to connect the Arduino board
com_port = 'COM5'

# Initialize the serial connection
ser = serial.Serial(com_port, baudrate=9600)

def set_flowrate(flowrate):
    return round(flowrate*68.571)

def time_remaining(user_data):
    skip_stages = user_data.get("skip_stages",{})
    total_remaining_time = 0
    stage_durations = {
        "Stripping Solution": 3600,
        "PBST Short": 1600,
        "PBS": 120,
        "Hybridization": 400,
        "Ligation Buffer": 500,
        "Ligation Solution": 600,
        "PBST Long": 500,
        "Imaging Buffer": 400,
    }
    for cycle_name, skip_status in skip_stages.items():
        if skip_status == 0:
            stage_duration = stage_durations.get(cycle_name, 0)
            total_remaining_time += stage_duration
    current_time = datetime.datetime.now()
    return current_time + datetime.timedelta(seconds = total_remaining_time)

def set_servo_duration(duration_seconds):
    try:
        # Initialize the serial connection
        # Send the duration command to the Arduino
        print(duration_seconds)
        command = f"SET_DURATION {duration_seconds}\n"
        ser.write(command.encode())
    except serial.SerialException as e:
        # Handle the connection error
        print(f"Serial connection error: {str(e)}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {str(e)}")
    
def move_servo(angle):
    try:
        # Initialize the serial connection
        # Adjust the baud rate as needed
        # Send the angle command to the Arduino
        command = f"MOVE {angle}\n"
        ser.write(command.encode())
        print(angle)
    except serial.SerialException as e:
        # Handle the connection error
        print(f"Serial connection error: {str(e)}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {str(e)}")

def stripping(mvp1, pump, user_data):
    cycle_id = "Stripping Solution"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    #current_angle = ser.read()
    #on_off = 1
    move_servo(45)
    # starting loop to make angle reach 135 degrees
    # The code section below is commented out to as we do not
    # need to adjust the angle of the coverslip to push fluid to it
    """ while current_angle < 135:
        for current_angle in range (current_angle, 135):
            current_angle = current_angle + 9
            move_servo(current_angle)
            time.sleep(2)
 """
    # setting MVP to correct valve so we have access to stripping fluid
    mvp.change_valve_pos(mvp1, 0, 8)
    time.sleep(10)

# Specify the duration in seconds
    duration_seconds = 60*(200/user_data["speeds"][cycle_id])  # Adjust this to the desired duration

    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id])) #starting the pump

    print("Starting flow of stripping solution to coverslip " + str(datetime.datetime.now()))

    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
        
    pump.stop()
    print("Stopping flow of stripping solution to coverslip " + str(datetime.datetime.now()))

    duration_seconds = 30
    start_time = time.time()

    print("Starting to Shake "+ str(datetime.datetime.now()) )
    while True:
        move_servo(135)
        time.sleep(5)
        move_servo(45)
    
        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        
        # Check if the desired duration has been reached
        if elapsed_time >= duration_seconds:
            time.sleep(5)
            break  # Exit the loop when the desired duration is reached
    print("Shaking Completed "+ str(datetime.datetime.now()) )
    move_servo(90)
    time.sleep(5)

def pbst_longwash(mvp1, pump, user_data):
    cycle_id = "PBST Long"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    

    #Moving servo to initial angle of 130
    move_servo(45)
    time.sleep(2)


    # setting MVP to correct valve so we have access to PBST
    mvp.change_valve_pos(mvp1, 0, 6)
    time.sleep(10)


    duration_seconds = 60*(200/user_data["speeds"][cycle_id])

    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id])) #starting the pump

    print('PBST Long Wash Start ' + str(datetime.datetime.now()))
    
    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
        
    pump.stop()
    print('PBST Long Wash Completed ' + str(datetime.datetime.now()))


    # in the loop below, we push the PBST wash solution through the pump
    # the fluid flows through the coverslip as the shaker starts shaking it

    duration_seconds = 30

    start_time = time.time()
    print("Starting to Shake "+ str(datetime.datetime.now()) )
    while True:
        move_servo(135)
        time.sleep(5)
        move_servo(45)
    
        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        
        # Check if the desired duration has been reached
        if elapsed_time >= duration_seconds:
            time.sleep(5)
            break  # Exit the loop when the desired duration is reached
    print("Shaking Completed "+ str(datetime.datetime.now()) )
    move_servo(90)
    time.sleep(5)

def PBS_6(mvp1, pump, user_data):
    cycle_id = "PBS"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return    
    #current_angle = ser.read()
    #on_off = 1
    move_servo(45)
    # initializing angle of the shaker
    """ while current_angle > 45:
        for current_angle in range (current_angle, 45):
            current_angle = current_angle - 9
            move_servo(current_angle)
            time.sleep(2) """

    mvp.change_valve_pos(mvp1, 0, 1)
    time.sleep(10)

    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    
    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id]))
    print("PBS_6 Rinse Start "+ str(datetime.datetime.now()))
    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
        
    pump.stop()
    print("PBS_6 Rinse Completed "+ str(datetime.datetime.now()))
    time.sleep(5)

def hyb_lig_clean(mvp1, pump, user_data): # DO THE FOLLWING 3 FUNCTIONS NEED TO BE CALLED AND WHEN AND AT WHAT SPEED
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    on_off = 1
    """ for angle in range(90, 135): 
        angle = angle + 45
        move_servo(angle)
        time.sleep(2)
 """
    move_servo(45)
    mvp.change_valve_pos(mvp1,0, 2)
    time.sleep(10)

    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    
    start_time = time.time()

    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id]))

    print('Hybridization line clean start' + str(datetime.datetime.now()))

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached

    pump.stop()
    print('Hybridization line clean stopped' + str(datetime.datetime.now()))
    time.sleep(5)

    mvp.change_valve_pos(mvp1,0, 4)
    time.sleep(10)

    start_time = time.time()

    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id]))

    print('Ligation line clean start' + str(datetime.datetime.now()))

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached

    pump.stop()
    print('Ligation line clean stopped' + str(datetime.datetime.now()))
    time.sleep(45)

def hyb_lig_rinse(mvp1, pump, user_data):
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return

    move_servo(45)
    time.sleep(2)

    mvp.change_valve_pos(mvp1, 0, 2)
    time.sleep(10)
    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    
    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id]))

    print('Hybridization line rinse start ' + str(datetime.datetime.now()))

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
    print('Hybridization line rinse completed ' + str(datetime.datetime.now()))       
    pump.stop()


    mvp.change_valve_pos(mvp1, 0, 4)
    time.sleep(10)

    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id]))

    print('Ligation line rinse start ' + str(datetime.datetime.now()))

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
    print('Ligation line rinse completed ' + str(datetime.datetime.now()))
    pump.stop()
        
    time.sleep(5)

def hyb_lig_clear(mvp1, pump, user_data):
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return

    mvp.change_valve_pos(mvp1, 0, 2)
    time.sleep(2)
    move_servo(45)
    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    
    start_time = time.time()
    print('Hybridization line clear start ' + str(datetime.datetime.now()))
    pump.push(user_data["speeds"][cycle_id])  

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
    print('Hybridization line clear completed ' + str(datetime.datetime.now()))
    pump.stop()    

    time.sleep(5)


    mvp.change_valve_pos(mvp1, 0, 4)
    time.sleep(10)

    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id]))

    print('Ligation line clear start ' + str(datetime.datetime.now()))

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
    print('Ligation line clear completed ' + str(datetime.datetime.now()))
    pump.stop()  
        
    time.sleep(5)

def lig(mvp1, pump, user_data):#*** what are these two functions for ?
 
    cycle_id = "Ligation Buffer"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return

    mvp.change_valve_pos(mvp1, 0, 3)
    time.sleep(2) 

    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    move_servo(45)
    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id]))

    print('Ligation solution input start ' + str(datetime.datetime.now()))

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
    print('Ligation solution input completed ' + str(datetime.datetime.now()))
    pump.stop()   
    
    time.sleep(5)

    # time.sleep(900)
    
def img(mvp1, pump, user_data):
    cycle_id = "Imaging Buffer"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    move_servo(45)

    mvp.change_valve_pos(mvp1, 0, 6)
    time.sleep(2)

    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    
    start_time = time.time()

    pump.push(user_data["speeds"][cycle_id])

    print('Imaging buffer timing start ' + str(datetime.datetime.now()))

    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
    print('Imaging buffer timing completed ' + str(datetime.datetime.now()))
    pump.stop()   

def img8hr(mvp1,pump,user_data):
    cycle_id = "Imaging Buffer"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped") #COME BACK TO THIS MAYBE CREATE A NEW FLOW RATE 
        return

    mvp.change_valve_pos(mvp1, 0, 6)
    move_servo(45)
    print("Imaging starting "+ str(datetime.datetime.now))

    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    
    start_time = time.time()

    pump.push(set_flowrate(user_data["speeds"][cycle_id]))


    while True:

        elapsed_time = time.time() - start_time

        if elapsed_time >= duration_seconds:
            break  # Exit the loop when the desired duration is reached
    print("Imaging completed "+ str(datetime.datetime.now))
    pump.stop()   

## ADDITION BY BEN:

def pbst_short(mvp1, pump, user_data):
    cycle_id = "PBST Short"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    move_servo(45)
    
    # Set servo angle
    """ In the Boyden Lab code they had a loop to set the angle and here I just set it
    - this is basically a note for debugging (refer to; https://github.com/molonc/exseq/blob/main/Boyden%20Lab%20Code/S05_PBST_short.m )"""
    # Set valve and pump for PBST washing
    mvp.change_valve_pos(mvp1, 0, 6)  # Replace with the appropriate valve position
    print("Wash Start " + str(datetime.datetime.now()))
    
    # Set up timer for 10 minutes (600 seconds)
    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    start_time = time.time()
    print("waiting for PBST solution to fill up " + str(datetime.datetime.now()))
    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id])) # Adjust as needed
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration_seconds:
            break

    pump.stop()
    print("PBST solution has filled up " + str(datetime.datetime.now()))        


    duration_seconds = 30
    start_time = time.time()
    print("Shaking Started "+ str(datetime.datetime.now()) )
    while True:
        move_servo(135)
        time.sleep(5)
        move_servo(45)
    
        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        
        # Check if the desired duration has been reached
        if elapsed_time >= duration_seconds:
            time.sleep(5)
            break  # Exit the loop when the desired duration is reached
    print("Shaking Completed "+ str(datetime.datetime.now()) )
    move_servo(90)
    time.sleep(5)       
    
def PBS_10(mvp1,pump, user_data):
    cycle_id = "PBS"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    #Setting the Valve and Pump for PBS RINSE
    mvp.change_valve_pos(mvp1, 0 , 1) #change to the appropriate valve postion
    time.sleep(10)# pause for 10 to calibrate 
    move_servo(45)   
    
    
    print("PBS_10 Rinse Start "+ str(datetime.datetime.now()))
    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id])) #change as needed 
   
    #Set timer for 435 seconds
    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    start_time = time.time()
    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id])) # Adjust as needed
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration_seconds:
            break   
    print("PBS_10 Rinse Completed "+ str(datetime.datetime.now()))
    pump.stop()
    time.sleep(5)
    
def hybridization(mvp1, pump, user_data):
    #Reference: https://github.com/molonc/exseq/blob/main/Boyden%20Lab%20Code/S08_Hybridization.m
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    move_servo(45)
    mvp.change_valve_pos(mvp1,0,2) #change witht the correct valves
    time.sleep(10)

    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id])) #change as needed
    # set timer for 3 minutes  
    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    start_time = time.time()
    print("Hybridization initiated " + str(datetime.datetime.now()))    
    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id])) # Adjust as needed
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration_seconds:
            break
    pump.stop()
    print("Hybridization Completed " + str(datetime.datetime.now()))
         
    time.sleep(5)
    
def ligation_buffer(mvp1,pump, user_data): 
    cycle_id = "Ligation Buffer"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    move_servo(45)
    #valve and pump 
    mvp.change_valve_pos(mvp1,0,3)
    time.sleep(10)

    print("Ligation Buffer Started " + str(datetime.datetime.now()))
    
    duration_seconds =60*(200/user_data["speeds"][cycle_id])
    start_time = time.time()
    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id]))
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration_seconds:
            break
    pump.stop()
    print("Ligation Buffer Completed " + str(datetime.datetime.now()))
    time.sleep(5)
    
def ligation_solution(mvp1,pump, user_data):
    """The code for this lab from boyden lab says incomplete,
    it also is unclear why there needs to be two call back functions but we still implemented it 
    Reference: https://github.com/molonc/exseq/blob/main/Boyden%20Lab%20Code/S13_Ligation.m"""
    
    cycle_id = "Ligation Solution"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return

    move_servo(45)
    
    time.sleep(2)  # Pause for calibration
    # Set valve and pump for ligation solution
    mvp.change_valve_pos(mvp1, 0, 4)  # Replace with the appropriate valve position
    time.sleep(10)  # Pause for calibration
    # Wait for the angle change timer to complete
    gsioc.GSIOC.push(pump, set_flowrate(user_data["speeds"][cycle_id])) # change as needed 
    duration_seconds = 60*(200/user_data["speeds"][cycle_id])
    start_time = time.time()
    print("Ligation Solution Input Start " + str(datetime.datetime.now()))
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration_seconds:
            break
    pump.stop()
    print("Ligation Solution Input Completed "+ str(datetime.datetime.now()))
    time.sleep(5)

def tester_function(mvp1,pump):
    # print("first test the servo motor")
    # move_servo(.25*180)
    # time.sleep(2)
    # move_servo(.75*180)
    # time.sleep(2)
    # print("testing the valve postioner")
    # for i in range(1, 9):
    #     mvp.change_valve_pos(mvp1,0,i)
    #     print("The Valve is now at position: "+ str(i))
    #     time.sleep(1)
    # print("testing the pump")
    # pump.push(500) # CW direction; 500 means 5 mL/min on display
    # time.sleep(10) #pump for 10 s
    # pump.draw(14) #CCW direction
    # time.sleep(2)
    # pump.stop()
    print("Testing all of it running at the same time")
    pump.push(500)
    for i in range(1, 9):
        if i%2 == 0:
            move_servo(.25*180)
        else:
            move_servo(.75*180)
        mvp.change_valve_pos(mvp1,0,i)
        print("The Valve is now at position: "+ str(i))
        time.sleep(1)
    pump.stop()

def fluidics_test(mvp1,pump,user_data,t_between):
    #testing each cycle 
    print("Testing the Fluidics Rounds: ")
    hyb_lig_clean(mvp1,pump,user_data)
    time.sleep(t_between)
    hyb_lig_rinse(mvp1,pump,user_data)
    time.sleep(t_between)
    hyb_lig_clear(mvp1,pump,user_data)
    time.sleep(t_between)
    stripping(mvp1,pump,user_data)
    time.sleep(t_between)
    pbst_short(mvp1,pump,user_data)
    time.sleep(t_between)
    PBS_6(mvp1,pump,user_data)
    time.sleep(t_between)
    hybridization(mvp1,pump,user_data)
    time.sleep(t_between)
    pbst_short(mvp1,pump,user_data)
    time.sleep(t_between)
    PBS_10(mvp1,pump,user_data)
    time.sleep(t_between)
    ligation_buffer(mvp1,pump,user_data)
    time.sleep(t_between)
    ligation_solution(mvp1,pump,user_data)
    time.sleep(t_between)
    pbst_longwash(mvp1,pump,user_data)
    time.sleep(t_between)
    img(mvp1,pump,user_data)
    time.sleep(t_between)
    img8hr(mvp1,pump,user_data)

if __name__ == "__main__":
    # set all the variables
    gsioc_COM = "COM3" # important: choose correct communitcation port
    mvp1_COM = "COM4"
    # #mvp2_COM = "COM13"
    
    #mvp2 = mvp.MVP()
    # set_servo_duration(0.03)
    # time.sleep(3)
    # move_servo(45)
    # time.sleep(5)
    # stripping_solution_speed = user_data["speeds"]["Stripping Solution"]
    # print(f"Stripping Solution Speed: {stripping_solution_speed} mL/s")
    # if user_data["skip_stages"]['Stripping Solution']== 1:
    #     print("Stage was skipped")
    
    
    """Code to test: """
    user_data = GUI.initiate_fluidics_gui()    
    # This Code Tests the system
    t_between = user_data["time_between_stages"]
    set_servo_duration(user_data["shaker_duration"])
    # connect the pump
    mvp1 = mvp.MVP()
    mvp1.connect(mvp1_COM)
    pump = gsioc.GSIOC()
    pump.connect(gsioc_COM)
    fluidics_test(mvp1,pump,user_data,t_between)
    
    # print("Testing at 0.6")
    # pump.push(set_flowrate(.6*100))
    # time.sleep(4)
    # print("Testing at 0.35")
    # pump.push(set_flowrate(.35*100))
    # time.sleep(4)
    # print("Testing at 0.22")
    # pump.push(set_flowrate(.22*100))
    # time.sleep(4)
    # print("Testing at 0.13")
    # pump.push(set_flowrate(.13*100))
    # time.sleep(4)
    # pump.stop()
    # pump.push(500) # CW direction; 500 means 5 mL/min on display
    # time.sleep(10) #pump for 10 s
    # #pump.draw(14) CCW direction
    # pump.stop()
    
    # hyb_lig_clean(mvp1,pump,user_data)
    # hyb_lig_rinse(mvp1,pump,user_data)
    # hyb_lig_clear(mvp1,pump,user_data)
    ser.close()



