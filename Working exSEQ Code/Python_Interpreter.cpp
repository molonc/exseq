#include <Servo.h>

Servo myservo;  // Create a servo object
int pos = 90;   // Initial servo position
unsigned long movementStartTime = 0; // Variable to store the start time of the movement
unsigned long durationMillis = 75; // Default duration in milliseconds (0.075 seconds)

void setup() {
  myservo.attach(6);  // Attach the servo to pin 6 (change as needed)
  Serial.begin(9600); // Initialize the serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming command as a string
    
    if (command.startsWith("MOVE")) {
      // Parse the command to extract target position
      int spaceIndex = command.indexOf(' ');
      if (spaceIndex != -1) {
        int targetPosition = command.substring(5).toInt();
        while (myservo.read() != targetPosition) {
          pos = myservo.read(); // Set the initial position
          if (pos > targetPosition) {
            myservo.write(pos - 1);
          } else {
            myservo.write(pos + 1);
          }
          delay(durationMillis);
        }
      }
    } else if (command.startsWith("SET_DURATION")) { 
      // Parse the command to set the duration
      int spaceIndex = command.indexOf(' ');
      if (spaceIndex != -1) {
        durationMillis = (unsigned long)(command.substring(spaceIndex + 1).toFloat() * 1000); // Convert seconds to milliseconds
      }
    }
  }
}
