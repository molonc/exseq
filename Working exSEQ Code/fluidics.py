from time import sleep, time
from mvp import change_valve_pos, MVP
from config.config import  getConfig
from gsioc import GSIOC
from shaker import Shaker
from enum import IntEnum

# MVP1:
#   - 1 1* PBS
#   - 2 Hydrbidization Solution
#   - 3 Ligation Buffer
#   - 4 Ligation Solution
#   - 5 Imaging Buffer
#   - 6 PBST
#   - 7 Stripping Solution




'''
Small enumeration for all of our buffers
'''
class Buffer(IntEnum):
    TDT_PRE = 1
    TDT_REACT = 2
    PBS = 3
    HYBRIDIZATION = 4
    SSC = 5
    PR2 = 6
    ISS = 7
    ZW_PR = 8
    IMAGING = 9
    CLEAVAGE = 10
    DAPI = 11

class Speed(IntEnum):
    SLOW = 0
    MEDIUM = 1
    FAST = 2

'''
    Encapsulates  Fluidics functions for Exseq Experiment: 
    @params config_path = path to config file
    @process
    - set_flowrate: flowrate -> rpm mapping
    - run_fluidics_round -> runs all buffers 
'''
class Fluidics:
    def __init__(self,*, config_path = './config/config.yaml',optimal_volume = -1) -> None:
        
        self._config = getConfig(path = config_path)
        self.pump = GSIOC()
        self.mvp = MVP()
        self.shaker = Shaker()

 
        self.pump_port = self._config['pump port']
        self.mvp_port = self._config['mvp port']
        self.shaker_port = self._config['shaker port']

        self.optimal_volume = self._config['optimal volume'] if optimal_volume == -1 else optimal_volume # optimal volume to clear chamber
        self.sys_vol = self._config['system volume']
        self.speeds = self._config['speeds']

        self.optimal_flowrate = self._config['buffer']

        self.stage_durations =  self._config['stage durations']
        self.shaker_duration = self._config['shaker duration']

    #Connect to fluidics devices all at once
    def connect(self):
        self.pump.connect(self.pump_port)
        self.shaker.connect(self.shaker_port)
        self.mvp.connect(self.mvp_port)
        self.mvp.initialize()
        sleep(5) #wait for pump *protocol doesn't awk*


    #@param flowrate: in ml/min
    def rpm2flowrate(self,rpm,m,b):
        return m*rpm + b 
    
    '''
        Pushes 1 buffer through chamber then pushes air right after
        @params: 
        - buffer: buffer id or mvp valve position - 1;  best to use Buffer enum
        - shake: whether the chamber should be shaken after fluidics rounds
        - duration: How long to push + incubate for before draining
        - speed: which [0,1,2] speed to push at use speed enum to improve readability
        - air_valve: which position on the mvp is connected to air
    '''
    def push_buffer_bench(self,buffer:Buffer,duration:int,speed:int=2,*
                           ,air_valve:int = 0):
        
        #tilt so buffer enters through lower side of chamber
        self.shaker.move_servo(45)
        change_valve_pos(self.mvp,0, (buffer.value % 8)) # out of bounds protection valve goes from 1-8

        #Use pre-calculated Linear Regression of rpm -> flowrate to calculate flowrate for buffer  
        slope = self.optimal_flowrate[buffer.name.lower()]['m'] 
        intercept = self.optimal_flowrate[buffer.name.lower()]['b']
        flowrate = self.rpm2flowrate(self.speeds[speed],slope,intercept)

        #volume is in 10* ul and flowrate is in 10* ul/min * 100)
        #Calculates how long to push for to fill system at speed
        push_duration = self.sys_vol / flowrate
        incubate_duration = duration - push_duration
        if incubate_duration < 0: print("Warning: Not enough time to fill chamber with this speed")
        sleep(2)
        start = time()
        self.pump.push(self.speeds[speed] *100)
        sleep(push_duration)
        #System should be full
        sleep(2)

        #shake while pushing to avoid bubbles
        while time() - start < duration:
            self.shaker.move_servo(135)
            sleep(2)
            self.shaker.move_servo(45)
            sleep(2)
        self.shaker.move_servo(90)
        self.pump.stop()

        # drain with air
        self.shaker.move_servo(135)
        change_valve_pos(self.mvp,0, (air_valve % 8)) # out of bounds protection valve goes from 1-8
        self.pump.push(flowrate *100)
        sleep(push_duration)
        self.pump.stop()

    def push_buffer_scope(self,buffer:Buffer,duration:int,speed:int = 2):
        change_valve_pos(self.mvp,0, (buffer.value % 8)) # out of bounds protection valve goes from 1-8

        #Calculate flowrate from speed and rpm map
        slope = self.optimal_flowrate[buffer.name.lower()]['m'] 
        intercept = self.optimal_flowrate[buffer.name.lower()]['b']
        flowrate = self.rpm2flowrate(self.speeds[speed],slope,intercept)

        push_duration = self.optimal_volume / flowrate
        incubate_duration = duration - push_duration
        if incubate_duration < 0: print("Warning: Not enough time to fill chamber with this speed")
        sleep(2)
        start = time()
        self.pump.push(self.speeds[speed] *100)
        sleep(push_duration)
        #System should be full
        sleep(2)
        self.pump.stop()
        sleep(incubate_duration)
        


            
        


        
    

        

    
    

