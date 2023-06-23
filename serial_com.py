import serial
import binascii
import time


class SerialObject:
    def __init__(self, serial=None):
        self.serial = serial
        self.baudrate = 9600

    def create_serial(self, port, baudrate, bytesize, timeout=None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize

        # Initiate serial connection
        s = serial.Serial(port)
        s.port = port
        s.timeout = timeout
        s.baudrate = baudrate
        s.bytesize = bytesize
        s.parity = serial.PARITY_ODD if bytesize % 2 != 0 else serial.PARITY_EVEN
        s.stopbits = 1

        self.serial = s

        try:
            self.serial.open()
            print(s)
        except:
            print(s)

    def close_serial(self):
        self.serial.close()

    def command(self, commandstring):
        s = self.serial
        data = binascii.a2b_qp("\n" + commandstring + "\r")
        time.sleep(0.5)

        s.flushInput()
        print(f"command: {data}")
        for i in range(1, len(data)):
            s.write(data[i : i + 1])
            print(s.read(1))
        s.flushOutput()
        print("sent command")
        com = s.read(1).decode("ascii")

        # Checking if the command's been received
        if com == "\x06":
            print("command received")
        else:
            print("negative acknowledgement: something went wrong")

    def buffered_command(self, commandstring):
        s = self.serial
        data = binascii.a2b_qp("\n" + commandstring + "\r")

        s.flushInput()

        resp = bytearray(0)

        # begin buffered command
        firstErrorPrinted = False

        # begin loop
        while True:
            s.write(data[0:1])
            resp_raw = s.read(1)
            readySig = resp_raw[0]
            print(resp_raw)

            if len(resp_raw) == 0:
                raise Exception("No response from device")

            if readySig == 10:
                print("Starting Buffered Command")
                break
            elif readySig == 35 or readySig == 163:  # hex 23 -> 35 + 128 = 163 = \xa3
                if not firstErrorPrinted:
                    print("Device busy...")
                    time.sleep(0.5)
                    firstErrorPrinted = True
            else:
                raise Exception("Did not receieve response!")

        resp.append(readySig)

        # Send buffered data
        for i in range(1, len(data)):
            s.write(data[i : i + 1])

            resp_raw = s.read(1)  # Will return empty array after timeout
            print(resp_raw)
            if len(resp_raw) == 0:
                raise Exception("No response from device")

            resp.append(resp_raw[0])

            if resp[i] != data[i]:
                raise Exception(
                    "Recieved "
                    + str(resp, "ascii")
                    + " instead of "
                    + str(data[i : i + 1])
                )

            if resp[i] == 13:
                print("Buffered command complete")
                return resp

        # for fail command
        print("Buffered Command FAILED")

        resp_no_whitespace = resp[1 : len(resp) - 2]

        s.flushOutput()
        return resp_no_whitespace.decode("ascii")
