#Class for controlling Arduino shaker 
'''
Supported commands
- READ: Get angle
- SET_DURATION: set shaker duration
- MOVE: move servo to given angle
'''
import serial


class Shaker:

    def __init__(self, port:str = 'COM3',*,shaker_duration:int = 3,baud:int = 9600) -> None:
        self.ser = serial.Serial(port=port,baudrate=baud)
        self.duration = shaker_duration
        self.port = port

    def _write(self,cmd:str = 'Read\n'):
        try:
            self.ser.write(cmd.encode())
        except serial.SerialException as e:
            raise Exception(f"Serial connection error: {str(e)}")
        except Exception as e:
            raise Exception(f'Exception: {str(e)}')
    
    #read angle from shaker
    def get_angle(self) -> int:
        self.ser.write(b'READ\n') # Send 'READ' command to request the angle
        current_angle = self.ser.readline().decode().strip() #reading the incoming message from the arduino 
        return int(current_angle)
    
    def set_servo_duration(self,duration_seconds:int):

            # Initialize the serial connection
            # Send the duration command to the Arduino        
            command = f"SET_DURATION {duration_seconds}\n"
            self._write(command)

    #Generic function to move servo to given degree
    #Heavily copied from @benrob13
    def move_servo(self,angle):
            # Initialize the serial connection
            # Adjust the baud rate as needed
            # Send the angle command to the Arduino
            command = f"MOVE {angle}\n"
            self._write(command)
            """this code waits until "True" is recieved from the arduino code"""
            while True:
                completion_message = (self.ser.readline().decode().strip())
                if(completion_message):
                    break        
 

    

