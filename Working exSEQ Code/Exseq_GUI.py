from config.config import setConfig, getConfig
from fluidics import Fluidics,change_valve_pos,Buffer
from mvp import MVP
from shaker import Shaker
from gsioc import GSIOC
import tkinter as tk
from tkinter import ttk
from GUI import DropdownDialog,list_available_com_ports,ExperimentalInfoDialog
from fusionrest import run, get_state
from time import sleep
from threading import Thread
'''
    Frame for holding all the values associated with the fluidics system
    Set flowrates which stages to skip etc...
'''
class Fluidics_Frame(tk.Frame):
    def __init__(self,fluids:Fluidics):
        super().__init__()
        self.fluids:Fluidics = fluids

        self.speed_frame = tk.Frame(self)


        self.entries = {}
        self.skips = {}
        for i,stage in enumerate(self.fluids.optimal_flowrate.keys()):
            strvar = tk.StringVar(value=str(self.fluids.optimal_flowrate[stage]))
            tk.Label(self.speed_frame,text=f"{stage} (ml/min)").grid(
                row=i,column=0,padx = 5,pady = 5, sticky = 'e'
            )
            self.entries[stage] = tk.Entry(self.speed_frame,textvariable=strvar)
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
class DeviceConnection(tk.Frame):
    def __init__(self,fluidics,root):
        super().__init__(root)

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
    def connect_pump(self):
        port = self.set_pump.get()
        self.fluid.pump_port = port
        self.fluid.pump.connect(self.fluid.pump_port)
    def connect_mvp(self):
        port = self.set_mvp.get()
        self.fluid.mvp_port = port
        self.fluid.mvp.connect(self.fluid.mvp_port)
        


    
class DeviceControl:
    def __init__(self,fluids):
        pass

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
        self.protocol = ttk.Combobox(self,values = self.protocols)
        self.protocol.set(self.protocols[0] if len(self.protocols) > 0 else 'No Protocol')
        self.protocol.pack(padx=5)
    def run(self):
        protocol = self.protocol.get()
        run(protocol)
    def is_running(self):
        return get_state() == 'running'

class Exseq_GUI():
    def __init__(self,root,*,config_path = './config/config.yaml'):
        self.root = root
        self.shape = (650,400)
        self.root.geometry(f'{self.shape[0]}x{self.shape[1]}')
        self.fluidics = Fluidics(config_path=config_path)
        self.exseq_thread = Thread(target=self.__run,args=(None,None))
        self.stop = False
        #User Interface
        self.fluid_frame = Fluidics_Frame(self.fluidics)
        self.connection = DeviceConnection(self.fluidics,root)
        self.run_frame = tk.Frame(self.root)
        self.protocol = Protocol(self.fluidics._config,self.run_frame)
        self.fluid_frame.grid(
            row=0,
            column=0
        )
        self.connection.grid(
            row = 1,
            column = 0,
            pady = 10
        )
        self.protocol.pack(
            side=tk.TOP
        )

        self.run = tk.Button(self.run_frame,text="Run Exseq",command=self.run_exseq,bg="#26ad0a")
        self.run.pack(
            side=tk.LEFT,
            pady = 5,
        )
        self.kill = tk.Button(self.run_frame,text="Stop Exseq",command=self.cancel,bg="#d11a17")
        self.kill.pack(side=tk.LEFT,pady=5)
        self.run_frame.grid(row=1,column=1,padx=10)
    def cancel(self):
        self.stop = True
    def __run(self,speeds,skips):
        if speeds and skips:
            for i,(speed,skip,stage) in \
                enumerate(zip(speeds,skips,self.fluidics.max_flowrate.keys())):
                if not self.stop:
                #Imaging
                #run protocol
                
                #while protocol.is_running sleep
                
                #Fluidics
                    if not skip:
                        print(stage,self.fluidics.id_valve[stage],i,speed)
                    sleep(10/7) #for testing remove later!!!
        self.run["state"] = tk.NORMAL
        self.run["text"] = "Run Exseq"
        self.root.update()
        self.stop = False


    #TODO FIll in protocol
    def run_exseq(self):
        info = ExperimentalInfoDialog(self.root,"Experimental info").result
        speeds = [float(self.fluid_frame.entries[var].get()) for var in self.fluid_frame.entries]
        skips = [bool(self.fluid_frame.skips[var].get()) for var in self.fluid_frame.skips] 
        self.run["state"] = tk.DISABLED
        self.run.config(text="Running...")
        self.root.update()
        self.exseq_thread = Thread(target=self.__run,args=(speeds,skips))
        self.exseq_thread.start()

   

if  __name__ == "__main__":
    root = tk.Tk()
    exseq = Exseq_GUI(root)
    exseq.root.mainloop()