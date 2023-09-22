# hamilton mvp
import time
from serial_com import SerialObject


class MVP(SerialObject):
    def __init__(self, serial=None):
        super().__init__(serial)

    def connect(self, COM_port):
        self.create_serial(COM_port, self.baudrate, 7, 5)
        self.enable_external()

    def initialize(self):
        self.command("aLXR")
        self.check_status()
        time.sleep(2)

    def enable_external(self):
        self.command("1a")
        self.check_status()
        time.sleep(2)

    def turn_clockwise(self, pos):
        self.command("aLP0%sR" % pos)
        self.check_status()
        time.sleep(2)

    def turn_counter_clockwise(self, pos):
        self.command("aLP1%sR" % pos)
        self.check_status()
        time.sleep(2)

    def check_status(self, timeout=10):
        self.command("aFR")
        start_time = time.time()
        resp = self.serial.read(1)
        print(resp)
        while resp.decode() != "Y":
            self.command("aFR")
            resp = self.serial.read(1)
            time.sleep(0.5)
            print(resp)
            if time.time() - start_time > timeout:
                break


# TODO: move the COM ports to a config file
def connect_all(mvp1, mvp2, mvp1_COM, mvp2_COM):
    try:
        mvp1.connect(mvp1_COM)
        mvp2.connect(mvp2_COM)
    except:
        print("Error Connecting to Valve Controllers")


def initialize_all(mvp1, mvp2):
    try:
        mvp1.initialize()
        mvp2.initialize()
        time.sleep(10)
    except:
        print("Function is not enabled, please check valve controller connection..")


def change_valve_pos(mvp, dir, pos):
    try:
        if dir == 0:
            mvp.turn_clockwise(pos)
        elif dir == 1:
            mvp.turn_counter_clockwise(pos)
        else:
            print("Invalid direction!")
    except:
        print("Function is not enabled...")