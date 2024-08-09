from gsioc import GSIOC
from mvp import MVP
from time import sleep, time
from GUI import list_available_com_ports
from fluidics import set_flowrate
from shaker import Shaker
RPM = 38

def test_flowrate(pump:GSIOC,speed, *, wait = 10 ): #test pump for 10 minutes
    print(f'Testing {speed}')
    pump.push(speed*100) # constant unit for minipuls is Revolutions/100 per Minute
    sleep(wait*60) # time in minutes -> seconds
    pump.stop()
    print(f"finished testing {speed} for {wait}")

'''
Params: 
- pump: Pump serial object defined in gsioc.py
- shaker: Shaker serial object defined in shaker.py
- flowrate: in ml/min
- volume: in ul (microlitres idk why floating point error?)


'''
def dye_test(pump:GSIOC,shaker:Shaker,mvp:MVP,*,flowrate:float = 0.333,volume:float = 650, wait=10):
    
    rpm = set_flowrate(flowrate) 
    duration_seconds = 60*(volume/(flowrate*100)) # time to push 6.5ml

    shaker.move_servo(45)
    sleep(2) 
    mvp.turn_clockwise(3) #push dye
    pump.push(rpm*100)
    sleep(duration_seconds)
    pump.stop()
    sleep(2)

    mvp.turn_clockwise(3) #push imaging
    pump.push(rpm*100)
    sleep(duration_seconds)
    pump.stop()
    sleep(2)


    





if __name__ == '__main__':
    pump = GSIOC()
    pump_port  = '/dev/ttyUSB0' # known
    mvp_port = '/dev/ttyUSB1'
    arduino_port = '/dev/ttyACM0'
    mvp = MVP()
    shaker = Shaker(arduino_port)

    pump.connect(pump_port)
    mvp.connect(mvp_port)
    mvp.initialize()

    # test_flowrate(pump,RPM,wait=2)
    dye_test(pump,shaker,mvp,flowrate=0.333) #nikon flowrate
    pump.close_serial()
    mvp.close_serial()