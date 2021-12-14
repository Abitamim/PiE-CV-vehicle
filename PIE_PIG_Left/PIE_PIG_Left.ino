#include <SpeedyStepper.h>

// pin assignments

const int LED_PIN = 13;
const int LEFT_MOTOR_STEP_PIN = 2;
const int LEFT_MOTOR_DIRECTION_PIN = 5;
const int RIGHT_MOTOR_STEP_PIN = 3;
const int RIGHT_MOTOR_DIRECTION_PIN = 6;
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
  stepperLeft.connectToPins(LEFT_MOTOR_STEP_PIN, LEFT_MOTOR_DIRECTION_PIN);
  stepperRight.connectToPins(RIGHT_MOTOR_STEP_PIN, RIGHT_MOTOR_DIRECTION_PIN);
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
  if (dir == "forward"){
      forward(1);
  }
  else if (dir == "left"){
      left(.3);
  }
  else if (dir == "right"){
      right(.3);
  }
}

void left(double rotations){
  int steps = int(200*rotations);
  int rightSteps = steps * .5;
  int leftSteps = steps * 1.5;
  float scaler = (float) leftSteps / (float) rightSteps;
  float speedLeft = 100 * scaler;
  float accelerationLeft = 100 * scaler;
  float speedRight = 100 / scaler;
  float accelerationRight = 100 / scaler;
  stepperLeft.setSpeedInStepsPerSecond(speedLeft);
  stepperLeft.setAccelerationInStepsPerSecondPerSecond(speedRight);
  stepperLeft.setupRelativeMoveInSteps(leftSteps);


  //
  // setup the motion for the Y motor
  //
  stepperRight.setSpeedInStepsPerSecond(speedRight);
  stepperRight.setAccelerationInStepsPerSecondPerSecond(accelerationRight);
  stepperRight.setupRelativeMoveInSteps(-rightSteps);

  while(!stepperLeft.motionComplete() && !stepperRight.motionComplete())
  {
    stepperLeft.processMovement();       // this call moves the motor
    stepperRight.processMovement();
    
    // check if motor has moved past position 400, if so turn On the LED

    if (stepperLeft.getCurrentPositionInSteps() == 400)
      digitalWrite(LED_PIN, HIGH);
  }
}
void right(double rotations){
  int steps = int(200*rotations);
  int rightSteps = steps * 1.5;
  int leftSteps = steps * .5;
  float scaler = (float) leftSteps / (float) rightSteps;
  float speedLeft = 100 * scaler;
  float accelerationLeft = 100 * scaler;
  float speedRight = 100 / scaler;
  float accelerationRight = 100 / scaler;
  stepperLeft.setSpeedInStepsPerSecond(speedLeft);
  stepperLeft.setAccelerationInStepsPerSecondPerSecond(speedRight);
  stepperLeft.setupRelativeMoveInSteps(leftSteps);


  //
  // setup the motion for the Y motor
  //
  stepperRight.setSpeedInStepsPerSecond(speedRight);
  stepperRight.setAccelerationInStepsPerSecondPerSecond(accelerationRight);
  stepperRight.setupRelativeMoveInSteps(-rightSteps);

  while(!stepperLeft.motionComplete() && !stepperRight.motionComplete())
  {
    stepperLeft.processMovement();       // this call moves the motor
    stepperRight.processMovement();
    
    // check if motor has moved past position 400, if so turn On the LED

    if (stepperLeft.getCurrentPositionInSteps() == 400)
      digitalWrite(LED_PIN, HIGH);
  }
}
void forward(int rotations){
  stepperLeft.setSpeedInStepsPerSecond(100);
  stepperLeft.setAccelerationInStepsPerSecondPerSecond(100);
  stepperLeft.setupRelativeMoveInSteps(200*rotations);


  //
  // setup the motion for the Y motor
  //
  stepperRight.setSpeedInStepsPerSecond(100);
  stepperRight.setAccelerationInStepsPerSecondPerSecond(100);
  stepperRight.setupRelativeMoveInSteps(-200*rotations);

  while(!stepperLeft.motionComplete())
  {
    stepperLeft.processMovement();       // this call moves the motor
    stepperRight.processMovement();
    
    // check if motor has moved past position 400, if so turn On the LED

    if (stepperLeft.getCurrentPositionInSteps() == 400)
      digitalWrite(LED_PIN, HIGH);
  }
}
