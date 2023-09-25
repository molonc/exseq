#include <Servo.h>

Servo myservo; // Create a servo object
int pos = 135; // Initial servo position
unsigned long movementStartTime = 0; // Variable to store the start time of the movement
unsigned long durationMillis = 0; // Variable to store the duration in milliseconds

void setup() {
  myservo.attach(6); // Attach the servo to pin 5
  Serial.begin(9600); // Initialize the serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming command as a string
    
    if (command.startsWith("MOVE")) {
      // Parse the command to extract target position 
      int spaceIndex = command.indexOf(' ');
      if (spaceIndex != -1) {
        int targetPosition = command.substring(spaceIndex + 1).toInt();
        pos = targetPosition; // Set the initial position
        myservo.write(pos); // Move to the initial position
      }
    } else if (command.startsWith("SET_DURATION")) {
      // Parse the command to set the duration
      int spaceIndex = command.indexOf(' ');
      if (spaceIndex != -1) {
        durationMillis = (unsigned long)(command.substring(spaceIndex + 1).toFloat() * 1000); // Convert seconds to milliseconds
        movementStartTime = millis(); // Record the start time of the movement
      } 

   }  

  } 
  // Check if it's time to stop the servo movement based on the duration
    if (durationMillis > 0 && millis() - movementStartTime >= durationMillis) {
      durationMillis = 0; // Reset the duration
      // You can take additional actions here if needed
    }
}
