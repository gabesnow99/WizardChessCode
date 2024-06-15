#include <AccelStepper.h>

// GLOBAL INTEGERS
#define ANALOG_THRESHOLD 505   // offset from 512 because of joystick calibration
#define DIGITAL_THRESHOLD .5
#define SPR 2038               // steps per revolution
#define SPEED 500
#define NORTH 250              // N,S,E,W vals tell us which direction the pots are oriented from ~512
#define SOUTH 750
#define EAST 250
#define WEST 750
#define MOTOR_INTERFACE 4
#define DEADZONE_VAL 10
#define INTERRUPT_OFFEST 100

// ANALOG PINS
#define EW_PIN A4              // VRy on joystick board
#define NS_PIN A5              // VRx on joystick board
#define BUTTON_PIN A3          // SW  on joystick board

// DIGITAL PINS
#define LED_PIN 13
#define EM_PIN 4               // Electromagnet
#define SOUTH_LIMIT_PIN 2
#define WEST_LIMIT_PIN 3

// VARIABLES
int EW_pot = 0;
int NS_pot = 0;
int button_val = 0;
int cycle_speed = 0;
int EW_speed = 0;
int NS_speed = 0;
unsigned long time = 0;
unsigned long last_time = 0;
volatile bool limit_pressed = false;
bool toggled = false;
AccelStepper EW_motor(MOTOR_INTERFACE, 9, 11, 10, 12);
AccelStepper NS_motor(MOTOR_INTERFACE, 5, 7, 6, 8);

// FUNCTION DECLARATIONS
void PinSetup();
void MotorSetup();
void Home();
void ReadPeripherals();
void UpdateSerial();
void HandleInterrupt(); // BUG: fix delays !!!! also THIS IS HIGHLY INNAPROPRIATE INTERRUPT HANDLING CODE
void ToggleRunByJoystick();
void RunByJoystick();

/*******************************************************************************/
void setup() {
  PinSetup();
  MotorSetup();
  Home();
  attachInterrupt(digitalPinToInterrupt(SOUTH_LIMIT_PIN), HandleInterrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(WEST_LIMIT_PIN), HandleInterrupt, RISING);
  Serial.begin(9600);
}

void loop() {
  ReadPeripherals();
  // UpdateSerial();
  RunByJoystick();
  
  // TOGGLE JOYSTICK
  // if (toggled){
  //   ToggleRunByJoystick();
  // }

  // TOGGLE ELECTROMAGNET
  if (toggled){
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(EM_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(EM_PIN, LOW);
  }

}

/*******************************************************************************/

// FUNCTION DEFINITIONS
void PinSetup() {
  // INPUTS
  pinMode(EW_PIN, INPUT);
  pinMode(NS_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(SOUTH_LIMIT_PIN, INPUT_PULLUP);
  pinMode(WEST_LIMIT_PIN, INPUT_PULLUP);

  // OUTPUTS
  pinMode(EM_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void MotorSetup() {
  EW_motor.setSpeed(SPEED);
  NS_motor.setSpeed(SPEED);
  EW_motor.setMaxSpeed(SPEED);
  NS_motor.setMaxSpeed(SPEED);
  // EW_motor.setAcceleration();
  // NS_motor.setAcceleration();
}

void Home() {
}

void ReadPeripherals() {
  EW_pot = analogRead(EW_PIN);
  NS_pot = analogRead(NS_PIN);
  button_val = analogRead(BUTTON_PIN);
  
  if (analogRead(BUTTON_PIN) < ANALOG_THRESHOLD){
    if (toggled == true){
      toggled = false;
    } else {
      toggled = true;
    }
    while (analogRead(BUTTON_PIN) < ANALOG_THRESHOLD) {}
  }

  time = millis();
}

void UpdateSerial() {
  // VARIABLES
  Serial.print("Cycle Speed: ");
  Serial.print(millis() - last_time);
  // Serial.print(" toggled: ");
  // Serial.print(toggled);
  // Serial.print(" EW_motor.currentPosition: ");
  // Serial.print(EW_motor.currentPosition());

  // INPUTS
  Serial.print(" NS_pot: ");
  Serial.print(NS_pot);
  Serial.print(" EW_pot: ");
  Serial.print(EW_pot);
  Serial.print(" button_val: ");
  Serial.print(button_val);

  // NEW LINE
  Serial.print("\n");
  last_time = millis();
}

void HandleInterrupt() { // BUG: fix delays !!!! also THIS IS HIGHLY INNAPROPRIATE INTERRUPT HANDLING CODE
  // STOP POWER
  EW_motor.stop();
  NS_motor.stop();
  // add the electromagnet turning off

  // WAIT FOR USER INPUT
  while (analogRead(BUTTON_PIN) > ANALOG_THRESHOLD) {
    digitalWrite(LED_PIN, HIGH);
    delay(63);
    digitalWrite(LED_PIN, LOW);
    delay(62);
  }

  // INDICATE USER IS READY
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(125);
    digitalWrite(LED_PIN, LOW);
    delay(725);
  }

  // USER CHOOSES DIRECTION TO GO
  while (1) {
    digitalWrite(LED_PIN, HIGH);
    // delay(63);    // TODO: Switch to PWM funciton (you will need to move all the pins too ... TAKE A PICTURE FIRST lol)
    digitalWrite(LED_PIN, LOW);
    // delay(59);
    ReadPeripherals();

    // WEST
    if (EW_pot > ANALOG_THRESHOLD + DEADZONE_VAL) {
      while (WEST_LIMIT_PIN > DIGITAL_THRESHOLD) {
        EW_motor.setSpeed(-SPEED / 4);
        EW_motor.runSpeed();
      }
      for (int i = 0; i < INTERRUPT_OFFEST; i++) {
        EW_motor.setSpeed(-SPEED);
        EW_motor.runSpeed();
      }

    // EAST
    } else if (EW_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
      while (WEST_LIMIT_PIN > DIGITAL_THRESHOLD) {
        EW_motor.setSpeed(SPEED / 4);
        EW_motor.runSpeed();
      }
      for (int i = 0; i < INTERRUPT_OFFEST; i++) {
        EW_motor.setSpeed(SPEED);
        EW_motor.runSpeed();
      }

    // SOUTH
    } else if (NS_pot > ANALOG_THRESHOLD + DEADZONE_VAL) {
      while (SOUTH_LIMIT_PIN > DIGITAL_THRESHOLD) {
        NS_motor.setSpeed(-SPEED / 4);
        NS_motor.runSpeed();
      }
      for (int i = 0; i < INTERRUPT_OFFEST; i++) {
        NS_motor.setSpeed(-SPEED);
        NS_motor.runSpeed();
      }

    // NORTH
    } else if (NS_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
      while (SOUTH_LIMIT_PIN > DIGITAL_THRESHOLD) {
        NS_motor.setSpeed(SPEED / 4);
        NS_motor.runSpeed();
      }
      for (int i = 0; i < INTERRUPT_OFFEST; i++) {
        NS_motor.setSpeed(SPEED);
        NS_motor.runSpeed();
      }
    } 
  }
}

void ToggleRunByJoystick() {
  ReadPeripherals();
  digitalWrite(LED_PIN, HIGH);

    while (toggled) {
      if (EW_pot > ANALOG_THRESHOLD + DEADZONE_VAL || EW_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
        EW_speed = map(EW_pot, 0, 1023, SPEED, -SPEED);
        EW_motor.setSpeed(EW_speed);
        EW_motor.runSpeed();
      }

      if (NS_pot > ANALOG_THRESHOLD + DEADZONE_VAL || NS_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
        NS_speed = map(NS_pot, 0, 1023, SPEED, -SPEED);
        NS_motor.setSpeed(NS_speed);
        NS_motor.runSpeed();
      }

      ReadPeripherals();
  }
  digitalWrite(LED_PIN, LOW);
  UpdateSerial();
}

void RunByJoystick() {
  if (EW_pot > ANALOG_THRESHOLD + DEADZONE_VAL || EW_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
    EW_speed = map(EW_pot, 0, 1023, SPEED, -SPEED);
    EW_motor.setSpeed(EW_speed);
    EW_motor.runSpeed();
  }

  if (NS_pot > ANALOG_THRESHOLD + DEADZONE_VAL || NS_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
    NS_speed = map(NS_pot, 0, 1023, SPEED, -SPEED);
    NS_motor.setSpeed(NS_speed);
    NS_motor.runSpeed();
  }
}
