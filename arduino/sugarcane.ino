#include <Stepper.h>
#include <Servo.h>


// --- Stepper Configuration ---
// Steps Per Revolution (2048 for common 28BYJ-48 motor in full-step mode)
const int spr = 2048;
// Stepper motor instance (Pins must match your driver board IN1, IN2, IN3, IN4 connections)
Stepper myStepper(spr, 9, 11, 8, 10);


// --- Servo Configuration ---
Servo servo1;
const int servoPin = 2;


// --- Control Variables ---
// Flag to control the stepper's running state
bool runStepper = true;
// Delay (in milliseconds) to pace the stepper motor movement
// Lower value = faster motor, but risk of stalling/vibration. 5-10ms is a good starting point.
const int stepDelayMs = 5; 


void setup() {
  // Initialize the serial port for communication
  Serial.begin(9600);
  Serial.println("System Initialized. Enter '1' to activate servo sequence.");
  
  // Stepper Speed Setting (only sets the theoretical max speed/internal timing)
  myStepper.setSpeed(10); 
  
  // Attach the servo to its pin
  servo1.attach(servoPin);
  // Set the servo to the initial position (0 degrees)
  servo1.write(0);
}


void loop() {
  // Check if a command is available from the Serial Monitor
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    
    // Command '1' starts the servo sequence
    if (cmd == '1') {
      Serial.println("Command '1' received. Stopping Stepper and moving Servo.");
      
      // 1. STOP the stepper motor
      runStepper = false;
      
      // 2. Perform Servo movement
      servo1.write(90);  // Move servo to 90 degrees
      delay(2000);       // Wait 1 second
      servo1.write(0);   // Return servo to 0 degrees
      
      // 3. Wait for a few seconds before resuming stepper
      delay(2000);
      
      // 4. RESUME the stepper motor
      runStepper = true;
      Serial.println("Servo sequence complete. Resuming Stepper.");
    }
  }
  
  // Continuous Stepper Movement Block
  if (runStepper) {
    // Take ONE step in REVERSE direction (negative value)
    myStepper.step(-1);
    
    // Add a delay to slow down the overall speed and prevent vibration (STALLING)
    // This delay is what fixes the issue from your original code.
    delay(stepDelayMs); 
  }
}
