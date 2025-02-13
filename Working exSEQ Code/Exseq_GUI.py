from config.config import setConfig, getConfig
from fluidics import Fluidics,change_valve_pos,Buffer
from mvp import MVP
from shaker import Shaker
from gsioc import GSIOC
import tkinter as tk
from tkinter import ttk
from GUI import DropdownDialog,list_available_com_ports,ExperimentalInfoDialog
from fusionrest import run, get_state,stop,ApiError
from time import sleep
from threading import Thread
from enum import Enum
from requests.exceptions import ConnectionError
from itertools import repeat
'''
    Frame for holding all the values associated with the fluidics system
    Set flowrates which stages to skip etc...
'''
class Fluidics_Frame(ttk.LabelFrame):
    def __init__(self,fluids:Fluidics,root):
        super().__init__(root)
        self['text'] = 'Fluid Settings'


        self.fluids:Fluidics = fluids

        self.speed_frame = tk.Frame(self)


        self.entries = {}
        self.skips = {}
        for i,stage in enumerate(self.fluids.optimal_flowrate.keys()):
            mapping = self.fluids.optimal_flowrate[stage]
            strvar = tk.StringVar(
                value=str(self.fluids.optimal_flowrate[stage]['speed'])
                
             )
            tk.Label(self.speed_frame,text=f"{stage} [0,1,2]").grid(
                row=i,column=0,padx = 5,pady = 5, sticky = 'e'
            )
            cmd = (self.speed_frame.register(self.validate),'%P','%d')
            self.entries[stage] = tk.Entry(
                self.speed_frame,
                textvariable=strvar,validate='all',
                validatecommand=cmd,
            )
            self.entries[stage].grid(
                row=i,column=1,padx = 5,pady = 5
            )
            self.skips[stage] = tk.BooleanVar(value=False)
            tk.Checkbutton(
                self.speed_frame,
                text = "Skip",
                command=self.update_entries,
                variable=self.skips[stage]
            ).grid(row=i,column=3,padx=5)
        tk.Label(self,text = "Flowrate Settings").pack(side=tk.TOP)
        self.speed_frame.pack()


    def validate(self,accept_type,action):
        if action == '1':
            if accept_type not in [str(i) for i in range(len(self.fluids.speeds))]:
                print('invalid')
                return False
        return True

    def update_entries(self):
        for stage in self.fluids.optimal_flowrate.keys():
            if self.skips[stage].get():
                self.entries[stage].config(state = tk.DISABLED)
            else:
                self.entries[stage].config(state = tk.NORMAL)

'''
    Class to handle Serial connection to each device
    Any new devices need driver code then they should be 
    added here
'''  
class DeviceConnection(ttk.LabelFrame):
    def __init__(self,fluidics:Fluidics,root):
        super().__init__(root)
        self['text'] = 'Device Connect'

        self.connection = {
            'pump':False,
            'mvp':False,
            'shaker':False
        }
        self.fluid = fluidics
        self.conn_frame = tk.Frame(self)
        #Draw
        tk.Label(self,text="Connection Settings").pack(side = tk.TOP)
        self.shaker_button = tk.Button(self.conn_frame,text="Connect to Arduino",command=self.connect_shaker)
        self.pump_button = tk.Button(self.conn_frame,text="Connect to pump",command=self.connect_pump)
        self.mvp_button = tk.Button(self.conn_frame,text = 'Connect to Valve',command=self.connect_mvp)
        ports = list_available_com_ports()
        #To Change serial ports
        self.set_shaker = ttk.Combobox(self.conn_frame,values=ports)
        self.set_shaker.set(self.fluid.shaker_port)
        self.set_pump = ttk.Combobox(self.conn_frame,values=ports)
        self.set_pump.set(self.fluid.pump_port)
        self.set_mvp = ttk.Combobox(self.conn_frame,values=ports)
        self.set_mvp.set(self.fluid.mvp_port)

        #Add to frame
        self.shaker_button.grid(row=0,column=0,padx=5)
        self.set_shaker.grid(row=0,column=1,padx=5)
        self.pump_button.grid(row=1,column=0,padx=5)
        self.set_pump.grid(row=1,column=1,padx=5)
        self.mvp_button.grid(row=2,column=0,padx=5)
        self.set_mvp.grid(row=2,column=1,padx=5)
        self.conn_frame.pack()
                                   

    def connect_shaker(self):
        port = self.set_shaker.get()
        self.fluid.shaker_port = port
        self.fluid.shaker.connect(self.fluid.shaker_port)
        self.connection['shaker'] = True
    def connect_pump(self):
        port = self.set_pump.get()
        self.fluid.pump_port = port
        self.fluid.pump.connect(self.fluid.pump_port)
        self.connection['pump'] = True
    def connect_mvp(self):
        port = self.set_mvp.get()
        self.fluid.mvp_port = port
        self.fluid.mvp.connect(self.fluid.mvp_port)
        self.fluid.mvp.initialize()
        self.connection['mvp'] = True


'''
    Wrapper Class to control devices through Exseq GUI
'''
class DeviceControl(ttk.LabelFrame):
    def __init__(self,fluids:Fluidics,connection:DeviceConnection,root):
        super().__init__(root)
        self['text'] = 'Device Control'


        self.fluidics = fluids
        self.connections = connection
        self.valves = list(set(self.fluidics.cycle_id.keys()))
        self.flowrate = tk.StringVar(value=str(0.33))
        self.angle = tk.StringVar(value=str(45))
        self.duration = tk.StringVar(value=str(0.075))
        #Draw
        # MVP
        tk.Label(self,text="Control Devices").pack()
        self.control_grid = tk.Frame(self)
        tk.Label(self.control_grid,text="Control MVP:").grid(
            row=0,column=0,sticky='w'
        )
        self.choose_valve = ttk.Combobox(self.control_grid,values=self.valves,width=5)
        self.choose_valve.set(self.valves[0])
        self.choose_valve.grid(row=0,column=1)
        tk.Button(self.control_grid,text='Change',command=self.change_valve).grid(
            row=0,column=2,pady=2
        )
        # Pump
        tk.Label(self.control_grid,text="Control Pump:").grid(
            row=1,column=0,sticky='w',pady=5
        )
        tk.Entry(self.control_grid,textvariable=self.flowrate,width=6).grid(
            row=1,column=1,pady=2
        )
        tk.Label(self.control_grid,text='(ml/min)').grid(
            row=1,column=2,pady=2
        )
        tk.Button(self.control_grid,text="Pump",command=self.push).grid(
            row=2,column=1,sticky='e',pady=2
        )
        tk.Button(self.control_grid,text="Stop",command=self.stop_pump).grid(
            row=2,column=2,pady=2
        )
        #Shaker
        tk.Label(self.control_grid,text="Control Shaker:").grid(
            row=3,column=0,sticky='w',pady=5
        )
        tk.Entry(self.control_grid,textvariable=self.duration,width=6).grid(
            row=3,column=1,pady=2
        )
        tk.Label(self.control_grid,text="(s/degree)").grid(
            row=3,column=2,sticky='w',pady=2
        )
        tk.Entry(self.control_grid,textvariable=self.angle,width=5).grid(
            row=4,column=1,pady=2
        )
        tk.Label(self.control_grid,text="(degrees)").grid(
            row=4,column=2, sticky='w',pady=2
        )
        tk.Button(self.control_grid,text="Go to",command=self.goto_angle).grid(
            row=4,column=0,sticky='e',pady=2
        )
        self.control_grid.pack()

    def change_valve(self):
        if self.connections.connection['mvp']:
            valve = int(self.choose_valve.get())
            change_valve_pos(
                self.fluidics.mvp,
                0,valve
            )
        else:
            print('mvp not connected')
    def push(self):
        if self.connections.connection['pump']:
            flowrate = float(self.flowrate.get())
            self.fluidics.pump.set_speed(
                self.fluidics.set_flowrate(flowrate=flowrate)
            )
            self.fluidics.pump.push()
        else:
            print('pump not connected')
    def stop_pump(self):
        if self.connections.connection['pump']:
            self.fluidics.pump.stop()
        else:
            print('pump not connected unplug to stop')
    def goto_angle(self):
        if self.connections.connection['shaker']:
            duration = float(self.duration.get())
            angle = float(self.angle.get())
            self.fluidics.shaker.set_servo_duration(duration)
            self.fluidics.shaker.move_servo(angle)
        else:
            print('shaker not connected')


        

'''
    Class to Choose Imaging Protocol
    just input string protocol names from the Fusion App
'''
class Protocol(tk.Frame):
    def __init__(self,config,root):
        super().__init__(root)


        self.protocols = config['protocols']
        # #draw
        tk.Label(self,text="Choose Protocol").pack(padx=5)
        self.protocol = ttk.Combobox(self,values = self.protocols,width=20)
        self.protocol.set(self.protocols[0] if len(self.protocols) > 0 else 'No Protocol')
        self.protocol.pack(padx=5)
    def run(self):
        protocol = self.protocol.get()
        run(protocol)
    def is_running(self):
        return get_state() == 'running'
    def stop(self):
        stop()
    def is_connected(self):
        try:
            s = self.is_running() 
        except (ConnectionError,ApiError) as e:
            return False
        return True

class Exseq_GUI():
    def __init__(self,root,*,config_path = './config/config.yaml',simulate:bool = False):
        self.root = root
        self.shape = (750,500)
        self.root.geometry(f'{self.shape[0]}x{self.shape[1]}')
        self.root.title('Exseq Control')
        self.fluidics = Fluidics(config_path=config_path)
        self.speed_setpoints = None
        self.skips = None
        self.exseq_thread = None
        self.stop = True
        self.sim = simulate
        #User Interface
        self.fluid_frame = Fluidics_Frame(self.fluidics,root)
        self.connection = DeviceConnection(self.fluidics,root)
        self.run_frame = tk.Frame(self.root)
        self.protocol = Protocol(self.fluidics._config,self.run_frame)
        self.control = DeviceControl(self.fluidics,self.connection,self.root)
        self.fluid_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )
        self.connection.grid(
            row = 1,
            column = 0,
            pady = 5,
            sticky='nsew',
            padx=5
        )
        self.protocol.pack(
            side=tk.TOP
        )
        self.control.grid(row=0,column=1,padx=5,pady=5,sticky='nsew')
        self.run = tk.Button(self.run_frame,text="Run Exseq",command=self.run_exseq,bg="#26ad0a")
        self.run.pack(
            side=tk.LEFT,
            pady = 5,
        )
        self.kill = tk.Button(self.run_frame,text="Stop Exseq",command=self.cancel,bg="#d11a17")
        self.kill.pack(side=tk.LEFT,pady=5)
        self.bench = tk.Button(self.run_frame,text="On Bench",command=self.on_bench,bg="#26ad0a")
        self.bench.pack(side=tk.LEFT,padx=5)
        self.run_frame.grid(row=1,column=1,padx=10,pady=10,sticky='s')

    '''
        E-stop function:
        will kill any thread executing the imaging or fluidics protocol
        will also stop the pump if it is running 
        will stop imaging if it is running
    '''
    def cancel(self):
        #Will kill code executing
        self.stop = True
        if self.connection.connection['pump']:
            self.control.stop_pump()
        #If running imaging kill imaging
        if self.protocol.is_connected() and \
            self.protocol.is_running(): self.protocol.stop()
    def get_speed(self,buffer:Buffer) -> int:
        speed = 0
        try: speed = self.fluid_frame.entries[buffer.name.lower()].get()
        except KeyError: 
            print(f"{buffer.name.lower()} not in speed entries")
            return -2

        try: speed = int(speed)
        except ValueError: 
            print(f"{buffer.name.lower()} speed entry is empty!")
            return -1

        return speed
        
    '''
        These functions interact with the fluidics object to run different fluidics rounds
        They are protected and should not be called outside this class
    ''' 

    '''
        on bench runs Steps 9 and 10 of exseq.
        it pushes each buffer and then air
    '''
    def __on_bench(self):
        #bench protocol defined in https://docs.google.com/presentation/d/17UVYqIIF_az_IiftN8ygVcyMJdWzFXmNhw3-oyN88vs/edit#slide=id.g32b88c2b297_0_0
        # slide 2
        
        buffers = [
            Buffer.TDT_PRE,Buffer.TDT_REACT,Buffer.PBS,
            Buffer.HYBRIDIZATION,Buffer.SSC,Buffer.PR2
        ]
        repeats = [1,1,3,1,3,3]
        durations = [
            20*60,90*60,10*60,
            60*60,10*60,10*60
        ]
        print("hello bench")
        for i,buffer in enumerate(buffers):
            if not self.stop:
                for _ in range(repeats[i]):
                    speed = self.get_speed(buffer)
                    if speed < 0: self.cancel()
                    if not self.sim:
                        self.fluidics.push_buffer_bench(
                            buffer.value,durations[i],speed=speed
                        )


                    print(buffer.name,durations[i],speed)
                    sleep(0.1)
        self.bench['state'] = tk.NORMAL
        self.bench.config(text="On Bench")
        self.root.update()
        self.stop = True
    '''
        on scope runs optionally step 14 and then step 12,13
        it pushes each buffer back to back
    '''
    def __on_scope(self,cleavage = False):
        #on scope defined in https://docs.google.com/presentation/d/17UVYqIIF_az_IiftN8ygVcyMJdWzFXmNhw3-oyN88vs/edit#slide=id.g32b88c2b297_0_0
        # slide 3 on
        print('running fluidics')

        #buffers used for fluidics round
        buffers = [
            Buffer.ISS,Buffer.ISS,Buffer.ZW_PR,Buffer.DAPI,Buffer.PR2, #step 12
            Buffer.IMAGING #Step 13
        ]
        repeats = [2,1,2,1,1,2]
        durations = [15*60,25*60,15*60,15*60,15*60,15*60]

        
        if cleavage:
            #Cleavage data
            cms_buffers = [
                Buffer.PR2,Buffer.CLEAVAGE,Buffer.CLEAVAGE,Buffer.PR2,Buffer.PR2
            ]
            cms_repeats = [2,2,1,2,2]
            cms_durations = [10*60,10*60,20*60,10*60,10*60]
            #update buffers with cleavage data
            buffers = cms_buffers + buffers
            repeats = cms_repeats + repeats
            durations = cms_durations + durations
        
        for i, buffer in enumerate(buffers):
            if not self.stop:
                for _ in range(repeats[i]):
                    speed = self.get_speed(buffer)
                    if speed < 0: self.cancel()  
                    print(buffer.name,durations[i],speed)
                    sleep(0.1)

                    if not self.sim:
                        self.fluidics.push_buffer_scope(buffer.value,durations[i],speed=speed)



    '''
        Functions to run all rounds of exseq
    '''
    def __exseq(self,rounds):
        print("running")
        #prepare for imaging
        self.__on_scope(cleavage=False)
        for i in range(rounds):
            if not self.stop:
                # Imaging
                if not self.sim:
                    assert self.protocol.is_connected() and  "Protocol is not\
                        connected!"
                    self.protocol.run()
                    sleep(2)
                    while self.protocol.is_running():
                        sleep(5)
                else:
                    
                    print(f"Imaging {self.protocol.protocol.get()}")
                    sleep(1)
                    
                #Fluidics
                self.__on_scope(cleavage=True)


        self.run["state"] = tk.NORMAL
        self.run["text"] = "Run Exseq"
        self.root.update()
        self.stop = True

    #Kick off exseq thread so gui remains responsive
    def on_bench(self):
        self.bench["state"] = tk.DISABLED
        self.bench.config(text = "Running...")   
        self.root.update()
        if self.stop:
            self.exseq_thread = Thread(target=self.__on_bench)
            self.stop = False
            self.exseq_thread.start()
        else:
            print("Thread is running command already Please Stop thread!")
    def run_exseq(self):
        info = ExperimentalInfoDialog(self.root,"Experimental info").result
        self.run["state"] = tk.DISABLED
        self.run.config(text="Running...")
        self.root.update()
        if self.stop:
            self.stop = False
            self.exseq_thread = Thread(target=self.__exseq,args=[8])
            self.exseq_thread.start()
        else:
            print("Thread is already running make sure to stop thread!")

   

if  __name__ == "__main__":
    import os
    os.chdir('Working exSEQ Code')
    root = tk.Tk()
    exseq = Exseq_GUI(root,simulate=True)
    exseq.root.mainloop()
    os.chdir('..')