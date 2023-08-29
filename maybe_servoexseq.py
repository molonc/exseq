from pyfirmata import Arduino, SERVO
import time

# Define the board's serial port
# Modify this to match your specific serial port
board = Arduino('/dev/tty.usbmodem143101')

# Define the servo pin
servo_pin = 4

# Create a servo instance
servo = board.get_pin(f's:{servo_pin}:s')

def move_servo(angle):
    servo.write(angle)
    time.sleep(0.25)  # Pause for a second between movements

try:
    start_time = time.time()  # Get the starting time
    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= 2700:  # Stop after 30 seconds
            print("Stopping rotation after 10 seconds.")
            break

        angles = [45, 135]
        for angle in angles:
            move_servo(angle)
            print(f"Set servo angle to {angle} degrees")

except KeyboardInterrupt:
    board.exit()