import time
from serial_com import SerialObject


class GSIOC(SerialObject):
    def __init__(self, serial=None):
        super().__init__(serial)

    def connect(self, COM_port):
        try:
            self.create_serial(COM_port, 19200, 8, 0.5)
            s = self.serial

            # Conect to device 30 (device number can be change on Minipuls 3)
            ID = 30 + 128

            s.flushInput()
            s.write(bytes.fromhex("ff"))
            time.sleep(self.timeout)
            s.write(ID.to_bytes(1, byteorder="big"))

            resp = s.read(1)  # return empty array when timeout
            if len(resp) == 0:
                raise Exception("No response from minipuls_3")
            time.sleep(1.5)
            self._enable_external()
            self.set_speed(3600)
            print("Connected to minipuls_3")
        except Exception as e:
            #  now our code throws an error instead of just printing one and continuing
            raise ConnectionError(f"Error connecting to Minipuls 3: {e}")

    def _enable_external(self):
        self.buffered_command("SR")

    def _run(self, speed, direction):
        self.set_speed(speed)
        if direction == 0:
            self.buffered_command("K>") # CW
        else:
            self.buffered_command("K<") # CCW

    def set_speed(self, speed):
        try:
            print("set speed")
            self.buffered_command("R%d" % speed)
        except Exception as e:
            raise ConnectionError(f"Function is not enabled, please check pump connection: {e}")


    def stop(self):
        try:
            print("stop")
            self.buffered_command("KH")
        except Exception as e:
            raise ConnectionError(f"Function is not enabled, please check pump connection: {e}")

    def push(self, speed):
        try:
            print("push")
            self._run(speed, 0) #CW direction - backwards
        except Exception as e:
            raise ConnectionError(f"Function is not enabled, please check pump connection: {e}")

    def draw(self, speed):
        try:
            self._run(speed, 1) #CCW direction - forwards
        except Exception as e:
            raise ConnectionError(f"Function is not enabled, please check pump connection: {e}")