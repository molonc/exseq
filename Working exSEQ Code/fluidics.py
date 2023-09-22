import time
import mvp
import gsioc
import datetime
import GUI
from pyfirmata import Arduino, SERVO
from threading import Timer
import threading

# MVP3: 1-7 hybridization
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
import serial
import time

# Define the COM port (change this to your specific COM port)
com_port = 'COM5'

# Initialize the serial connection
ser = serial.Serial(com_port, baudrate=9600)  

def set_servo_duration(duration_seconds):
    try:
        # Initialize the serial connection
        # Send the duration command to the Arduino
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
    except serial.SerialException as e:
        # Handle the connection error
        print(f"Serial connection error: {str(e)}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {str(e)}")


def timer_callback_stripping(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print("primer done" + datetime.datetime.now())

def stripping(mvp1, pump, user_data):
    cycle_id = "Stripping Solution"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    current_angle = ser.read()
    on_off == 1

    # starting loop to make angle reach 135 degrees
    while current_angle < 135:
        for current_angle in range (current_angle, 135):
            current_angle = current_angle + 9
            move_servo(current_angle)
            time.sleep(2)

    # setting MVP to correct valve so we have access to stripping fluid
    mvp.change_valve_pos(mvp1, 0, position(7))
    time.sleep(10)
    print("stripping initiated"+ datetime.datetime.now())
    
    timer = Timer(3600, timer_callback_stripping)

    timer.start()

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id]) #starting the pump


    # in the loop below, we push the stripping solution through the pump
    # the fluid flows through the coverslip as the shaker starts shaking it
    while on_off == 1:

        for angle in range (108, 63, -9): #starting the shaking
            move_servo(angle)
            time.sleep(2)


        time.sleep(5)

        for angle in range (63, 108, 9):
            move_servo(angle)
            time.sleep(2)

        time.sleep(5)

    time.sleep(45)
    
def timer_callback_pbst_longwash(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print('Wash done' + datetime.datetime.now())

def pbst_longwash(mvp1, pump, user_data):
    cycle_id = "PBST-Long"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    on_off = 1

    #Moving servo to initial angle of 130
    move_servo(0.75*180)
    time.sleep(2)


    # setting MVP to correct valve so we have access to PBST
    mvp.change_valve_pos(mvp1, 0, position(6))
    time.sleep(10)


    timer = Timer(5400, timer_callback_pbst_longwash)
    print('PBST Long Wash Start' + datetime.datetime.now())


    # in the loop below, we push the PBST wash solution through the pump
    # the fluid flows through the coverslip as the shaker starts shaking it
    while on_off == 1:
        gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])
        timer.start()
        for angle in range (108, 63):
            angle = angle - 9
            move_servo(angle)
            time.sleep(2)

        time.sleep(5)

        for angle in range (63, 108):
            angle = angle + 9
            move_servo(angle)
            time.sleep(2)
        
        time.sleep(5) 

    time.sleep(45)

def timer_callback_PBS_6_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print(('Rinse done' + datetime("now")))

def PBS_6(mvp1, pump, user_data):
    cycle_id = "PBS"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return    
    current_angle = servo.read()
    on_off = 1

    # initializing angle of the shaker
    while current_angle > 45:
        for current_angle in range (current_angle, 45):
            current_angle = current_angle - 9
            move_servo(current_angle)
            time.sleep(2)

    mvp.change_valve_pos(mvp1, 0, position(1))
    time.sleep(10)

    # setting MVP to correct valve so we have access to PBS for rinsing
    timer = Timer(5400, timer_callback_PBS_6_callback)

    print(('PBS Rinse Start' + datetime("now")))

    while on_off == 1:
        gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])
        timer.start()

    time.sleep(45)

def hyb_clean_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print('Hybridization line clean Done' + datetime("now"))

def lig_clean_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print('Ligation line clean Done' + datetime("now"))

def hyb_lig_clean(mvp1, pump, user_data):
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    on_off = 1
    for angle in range(90, 135): 
        angle = angle + 45
        move_servo(angle)
        time.sleep(2)

    mvp.change_valve_pos(mvp1, position(2))
    time.sleep(10)

    timer = Timer(167, hyb_clean_callback)
    print('Hybridization line clean start' + datetime("now"))

    timer.start()

    while on_off == 1:
        gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])

    time.sleep(45)

    mvp.change_valve_pos(mvp1, position(4))
    time.sleep(10)

    timer2 = Timer(167, lig_clean_callback)
    print('Ligation line clean start' + datetime("now"))

    timer2.start()


    while on_off == 1:
        gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])

    time.sleep(45)

def hyb_rinse_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print('Hybridization line rinse Done' + datetime("now"))

def hyb_lig_rinse_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print('Ligation line rinse Done' + datetime("now"))

def hyb_lig_rinse(mvp1, pump, user_data):
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        #print(cycle_id + " was skipped")
        return
    move_servo(135)
    time.sleep(2)

    mvp.change_valve_pos(mvp1, 0, position(2))
    on_off = 1
    angles = [90, 135]

    mvp.change_valve_pos(mvp1, 0, position(2))
    time.sleep(10)

    timer = Timer(167, hyb_rinse_callback)

    timer.start()

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])


    while on_off == 1:
        print("Rinsing")

    time.sleep(45)


    mvp.change_valve_pos(mvp1, 0, position(4))
    time.sleep(10)
    on_off = 1

    timer2 = Timer(167, hyb_rinse_callback)

    timer2.start()

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])


    while on_off == 1:
        print("Rinsing")
        
    time.sleep(45)

def hyb_lig_clear_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)

def hyb_lig_clear(mvp1, pump, user_data):
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        #print(cycle_id + " was skipped")
        return
    for angle in range(135, 45):
        angle = angle + 18
        move_servo(angle)

    mvp.change_valve_pos(mvp1, 0, position(2))
    time.sleep(2)

    on_off = 1
    angles = [90, 135]

    timer = Timer(190, hyb_lig_clear_callback, args = ('Hybridization line clear Done' + datetime("now")))

    timer.start()

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])


    while on_off == 1:
        print("Clearing")

    time.sleep(45)


    mvp.change_valve_pos(mvp1, 0, position(4))
    time.sleep(10)
    on_off = 1

    timer2 = Timer(190, hyb_lig_rinse_callback, args = ('Ligation line clear Done' + datetime("now")))

    timer2.start()

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])


    while on_off == 1:
        print("Clearing")
        
    time.sleep(45)

def lig_callback(pump): #***
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)

def lig(mvp1, pump, user_data):#*** what are these two functions for ?
    for angle in range(45, 135):
        angle = angle + 18
        move_servo(angle)
    mvp.change_valve_pos(mvp1, 0, 3)
    time.sleep(2)

    on_off = 1
    timer = Timer(200, lig_callback, args = ('Ligation buffer done' + datetime("now")))


    timer.start()

    gsioc.GSIOC.push(pump, 300)

    while on_off == 1:
        print("ligation buffer going")
    
    time.sleep(45)

    time.sleep(900)

def img_callback(mvp1, pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    
def img(mvp1, pump, user_data):
    cycle_id = "Imaging Buffer"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    on_off = 1

    for angle in range(45, 135):
        angle = angle + 18
        move_servo(angle)
        time.sleep(2)

    mvp.change_valve_pos(mvp1, 0, position(6))
    time.sleep(2)

    timer = Timer(240, lig_callback, args = ('Imaging Buffer Priming Done' + datetime("now")))

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])

    timer.start()

    while on_off ==1:
        print("imaging buffer setting up")

def img8hr_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print('Imaging Done' + datetime("now"))

def img8hr(mvp1,pump):
    cycle_id = "Imaging Buffer"
    if user_data["skip_stages"][cycle_id] == 1:
        #print(cycle_id + " was skipped")
        return
    on_off = 1

    mvp.change_valve_pos(mvp1, 0, position(6))

    timer = Timer(14400, lig_callback)
    print("Imaging starting"+ datetime.datetime.now)

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])

    timer.start()

    while on_off ==1:
        pass

## ADDITION BY BEN:
def timer_callback_pbst_short(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print("Wash Done " + str(datetime.datetime.now()))

def pbst_short(mvp1, pump, user_data):
    cycle_id = "PBST-Short"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    global on_off
    
    # Set servo angle
    """ In the Boyden Lab code they had a loop to set the angle and here I just set it
    - this is basically a note for debugging (refer to; https://github.com/molonc/exseq/blob/main/Boyden%20Lab%20Code/S05_PBST_short.m )"""
    move_servo(0.75*180)
    
    # Set valve and pump for PBST washing
    mvp.change_valve_pos(mvp1, 0, position(6))  # Replace with the appropriate valve position
    print("Wash Start " + str(datetime.datetime.now()))
    
    # Set up timer for 10 minutes (600 seconds)
    timer = Timer(600, timer_callback_pbst_short, args=(pump,))
    timer.start()
    
    on_off = 1
    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id]) # Adjust as needed
    
    while on_off == 1:
        # Implement servo angle changes for shaking here
        for angle in range(60*180, 35*180, -5*180):
            move_servo(angle/100)
            time.sleep(2)
        
        time.sleep(5)
        
        for angle in range(35*180, 60*180, 5*180):
            move_servo(angle/100)
            time.sleep(2)
        
        time.sleep(5)
    
    time.sleep(45)       
    
def timer_callback_PBS_10_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print("PBS_10 Rinse Complete" + str(datetime.datetime.now()))    


def PBS_10(mvp1,pump, user_data):
    cycle_id = "PBS"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    """I think this implementation of directly changing the angle should work"""
    #setting angle 
    on_off = 1

    for angle in range(135, 45):
        angle = angle - 18
        move_servo(angle)
        time.sleep(2)
    
    #Setting the Valve and Pump for PBS RINSE
    mvp.change_valve_pos(mvp1, 0 , position(1)) #change to the appropriate valve postion
    time.sleep(10)# pause for 10 to calibrate 
        
    #Set timer for 435 seconds
    timer = Timer(435, timer_callback_PBS_10_callback)
    print("PBS_10 Rinse Start"+ str(datetime.datetime.now()))


    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id]) #change as needed 

    timer.start()
    
    while on_off == 1:
        pass
    
    time.sleep(45)

def timer_callback_Hybridization_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print("Hybridization Set " + str(datetime.datetime.now()))
    
def hybridization(mvp1, pump, user_data):
    #Reference: https://github.com/molonc/exseq/blob/main/Boyden%20Lab%20Code/S08_Hybridization.m
    cycle_id = "Hybridization"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    
    for angle in range(.25*180,.75*180,.1*180):
        move_servo(angle)
        time.sleep(2)
    # Valve and Pump Stuff 
    mvp.change_valve_pos(mvp1,0,position(2)) #change witht the correct valves
    time.sleep(10)

    print("Hybridization initiated " + str(datetime.datetime.now()))
    
    # set timer for 3 minutes 
    timer = Timer(177, timer_callback_Hybridization_callback, args = (pump,))
    
    on_off = 1
    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id]) #change as needed
    timer.start()

    while on_off == 1:
        pass
    
    gsioc.GSIOC.stop(pump) #not sure this is neccessary but the matlab stopped the pump with their timer and at the end of their program 
    
    time.sleep(2700)

def timer_callback_ligation_callback(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print("Ligation Buffer Completed " + str(datetime.datetime.now()))
    
def ligation_buffer(mvp1,pump, user_data): 
    cycle_id = "Ligation Buffer"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    #setting the angle 
    for angle in range(.25*180,.75*180,.1*180):
        move_servo(angle)
        time.sleep(2)
    
    #valve and pump 
    mvp.change_valve_pos(mvp1,0,position(3))
    time.sleep(10)

    print("Ligation Buffer Started " + str(datetime.datetime.now()))
    timer = Timer(200, timer_callback_ligation_callback)
    
    on_off = 1
    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id])

    timer.start()
    
    while on_off == 1:
        pass

    time.sleep(500)
    
def timer_callback_angle_change(pump):
    global angle
    angle = 0.75
    move_servo(0.75)
    print("Angle change " + str(datetime.datetime.now()))
    
def timer_callback_ligation_start(pump):
    global on_off
    on_off = 3
    gsioc.GSIOC.stop(pump)
    print("Ligation Completed " + str(datetime.datetime.now()))
    
def ligation_solution(mvp1,pump, user_data):
    """The code for this lab from boyden lab says incomplete,
    it also is unclear why there needs to be two call back functions but we still implemented it 
    Reference: https://github.com/molonc/exseq/blob/main/Boyden%20Lab%20Code/S13_Ligation.m"""
    
    cycle_id = "Ligation Solution"
    if user_data["skip_stages"][cycle_id] == 1:
        print(cycle_id + " was skipped")
        return
    
    # Set servo angle to 0.25 (stay at one angle for ligation)
    angle = 0.25
    move_servo(angle*180)
    
    time.sleep(2)  # Pause for calibration
    # Set valve and pump for ligation solution
    mvp.change_valve_pos(mvp1, 0, position(4))  # Replace with the appropriate valve position
    time.sleep(10)  # Pause for calibration
    
    # Set up the speed and timer for about 1 minute to change angle
    
    angle_change_timer = Timer(90, timer_callback_angle_change)

    print("Ligation Solution Input Start " + str(datetime.datetime.now()))

    angle_change_timer.start()

    # Wait for the angle change timer to complete

    gsioc.GSIOC.push(pump, user_data["speeds"][cycle_id]) # change as needed 

    while angle == 0.25:
        pass

      # Start the ligation timer 
    timer = Timer(100, timer_callback_ligation_start)
    timer.start()
    
# Wait for the ligation process to complete
    while on_off == 1:
        pass

    time.sleep(45)

def position(idx): 
    if(idx>8 or idx<1):
        raise Exception("Invalid Position")
    valv_position = [5,6,7,8,1,2,3,4]
    return valv_position[idx-1] 

def tester_function(mvp1,pump):
    # print("first test the servo motor")
    # move_servo(.25*180)
    # time.sleep(2)
    # move_servo(.75*180)
    # time.sleep(2)
    # print("testing the valve postioner")
    # for i in range(1, 9):
    #     mvp.change_valve_pos(mvp1,0,position(i))
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
        mvp.change_valve_pos(mvp1,0,position(i))
        print("The Valve is now at position: "+ str(i))
        time.sleep(1)
    pump.stop()

def fluidics_test(mvp1,pump,user_data,t_between):
    #testing each cycle 
    print("testing the Fluidics Rounds: ")
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

if __name__ == "__main__":
    # set all the variables
    gsioc_COM = "COM4" # important: choose correct communitcation port
    mvp1_COM = "COM3"
    #mvp2_COM = "COM13"
    mvp1 = mvp.MVP()
    mvp1.connect(mvp1_COM)
    #mvp2 = mvp.MVP()
    # user_data = GUI.initiate_fluidics_gui()
    # stripping_solution_speed = user_data["speeds"]["Stripping Solution"]
    # print(f"Stripping Solution Speed: {stripping_solution_speed} mL/s")
    # if user_data["skip_stages"]['Stripping Solution']== 1:
    #     print("Stage was skipped")
        
    #This Code Tests the system
    # t_between = user_data["time_between_stages"]
    
    
    # connect the pump
    pump = gsioc.GSIOC()
    pump.connect(gsioc_COM)
    # pump.push(500) # CW direction; 500 means 5 mL/min on display
    # time.sleep(10) #pump for 10 s
    # #pump.draw(14) CCW direction
    # pump.stop()
    tester_function(mvp1,pump)

