#include <SpeedyStepper.h>

// pin assignments

const int LED_PIN = 13;
const int Left_MOTOR_STEP_PIN = 2;
const int Left_MOTOR_DIRECTION_PIN = 5;
const int Right_MOTOR_STEP_PIN = 3;
const int Right_MOTOR_DIRECTION_PIN = 6;
const int STEPPERS_ENABLE_PIN = 8;

SpeedyStepper stepperLeft;
SpeedyStepper stepperRight;

String command;
float turnAmount=45;
int turnConstant=1;
float leftMotorAdjust=1;
float rightMotorAdjust=1;

void right(float turnAmount);
void moveRobot(String dir);
int i = 0; 
void setup() {
 
  pinMode(LED_PIN, OUTPUT); 
  pinMode(STEPPERS_ENABLE_PIN, OUTPUT);  
  Serial.begin(9600);

  digitalWrite(STEPPERS_ENABLE_PIN, LOW);
  
  // connect and configure the stepper motors to their IO pins
  stepperLeft.connectToPins(Left_MOTOR_STEP_PIN, Left_MOTOR_DIRECTION_PIN);
  stepperRight.connectToPins(Right_MOTOR_STEP_PIN, Right_MOTOR_DIRECTION_PIN);
}

void loop() {
  // Left Stepper settings
  stepperLeft.setSpeedInStepsPerSecond(100);
  stepperLeft.setAccelerationInStepsPerSecondPerSecond(100);
  // Left Stepper settings
  stepperRight.setSpeedInStepsPerSecond(100);
  stepperRight.setAccelerationInStepsPerSecondPerSecond(100);  

    if (Serial.available()) {
        char ch = Serial.read();
        // carriage return means a command has finished sending, so parse it and
        // reset the string
        if (ch != '\r') {
            command += ch;
        } else {
            Serial.print(command);
            moveRobot(command);
            
            command = "";
        }
    }
//    forward(1);
//    delay(5000);
//    right(200);
//    delay(5000);
//    left(200);
//    delay(5000);
//  }else if(turnAmount>-20){
//    forward();
//  }else{
//    left(turnAmount);
//  }
  
}

void moveRobot(String dir) {
//  Serial.println(dir);
  if (dir == "forward")
      right(1);
  
}

void left(float turnAmount){
  stepperRight.moveRelativeInSteps(200*turnAmount*turnConstant*leftMotorAdjust);
}
void right(float turnAmount){
  stepperLeft.moveRelativeInSteps(200*turnAmount*turnConstant*rightMotorAdjust);
}
void forward(int rotations){
  stepperLeft.setupMoveInSteps(200*leftMotorAdjust*rotations);
  stepperRight.setupMoveInSteps(200*rightMotorAdjust*rotations);

  while(!stepperLeft.motionComplete())
  {
    stepperLeft.processMovement();       // this call moves the motor
    stepperRight.processMovement();
    
    // check if motor has moved past position 400, if so turn On the LED

    if (stepperLeft.getCurrentPositionInSteps() == 400)
      digitalWrite(LED_PIN, HIGH);
  }
}
