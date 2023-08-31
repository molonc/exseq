import time
from pyfirmata import Arduino, SERVO

# Connect to Arduino
board = Arduino('/dev/tty.usbmodem143101')  # Replace with the appropriate port name

# Attach servo to pin D4
servo_pin = board.get_pin('d:4:s')

t0 = time.time()
while time.time() - t0 < 30:
    print(time.ctime())
    for angle in range(25, 76, 25):  # angles of servo: 25, 50, 75
        angle_normalized = angle / 180.0
        servo_pin.write(angle_normalized)
        current_pos_normalized = servo_pin.read()
        current_pos_deg = current_pos_normalized * 180.0
        print(f'Current motor position is {current_pos_deg:.2f} degrees')
        time.sleep(2)

# Detach and close
board.exit()