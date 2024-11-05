from config.config import setConfig, getConfig
from fluidics import Fluidics,change_valve_pos,Buffer
from mvp import MVP
from shaker import Shaker
from gsioc import GSIOC
import tkinter as tk
from tkinter import ttk
from GUI import DropdownDialog,list_available_com_ports,ExperimentalInfoDialog


'''
    Frame for holding all the values associated with the fluidics system
    Set flowrates which stages to skip etc...
'''
class Fluidics_Frame(tk.Frame):
    def __init__(self,fluids):
        super().__init__()
        self.fluids = fluids

        self.speed_frame = tk.Frame(self)


        self.entries = {}
        
        for i,stage in enumerate(self.fluids.optimal_flowrate.keys()):
            strvar = tk.StringVar(value=str(self.fluids.optimal_flowrate[stage]))
            tk.Label(self.speed_frame,text=f"{stage} (ml/min)").grid(
                row=i,column=0,padx = 5,pady = 5, sticky = 'e'
            )
            self.entries[stage] = tk.Entry(self.speed_frame,textvariable=strvar)
            self.entries[stage].grid(
                row=i,column=1,padx = 5,pady = 5
            )
        tk.Label(self,text = "Flowrate Settings").pack(side=tk.TOP)
        self.speed_frame.pack()



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
    just input string protocol names from the Fusion Appp
'''
class Protocol(tk.Frame):
    def __init__(self,config):
        super().__init__()

        self.protocols = config['protocols']
        # #draw
        tk.Label(self,text="Choose Protocol").pack(padx=5)
        self.protocol = ttk.Combobox(self,values = self.protocols)
        self.protocol.set(self.protocols[0] if len(self.protocols) > 0 else 'No Protocol')
        self.protocol.pack(padx=5)

class Exseq_GUI():
    def __init__(self,root,*,config_path = './config/config.yaml'):
        self.root = root
        self.shape = (600,400)
        self.root.geometry(f'{self.shape[0]}x{self.shape[1]}')
        self.fluidics = Fluidics(config_path=config_path)

        #User Interface
        self.fluid_frame = Fluidics_Frame(self.fluidics)
        self.connection = DeviceConnection(self.fluidics,root)
        self.protocol = Protocol(self.fluidics._config)
        self.fluid_frame.place(
            x=0,
            y=50
        )
        self.connection.place(
            x=0,
            y = 300
        )
        self.protocol.place(
            x=400,
            y = 50
        )

        self.run = tk.Button(self.root,text="Run Exseq",command=self.run_exseq)
        self.run.place(
            x= 425,
            y = 100
        )

    #TODO FIll in protocol
    def run_exseq(self):
        info = ExperimentalInfoDialog(self.root,"Experimental info").result
        speeds = [float(self.fluid_frame.entries[var].get()) for var in self.fluid_frame.entries]
        print(speeds)
        
if  __name__ == "__main__":
    root = tk.Tk()
    exseq = Exseq_GUI(root)
    exseq.root.mainloop()