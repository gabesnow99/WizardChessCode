// NOTE: main.cpp was modified to include homingSequence() {}, therefore if the IDE is updated we may need to modify this file again
// NOTE: having a separate homingSequence() {} overrides the bug that sends the ISR
// NOTE: having an unmodified main.cpp will run but not execute the homingSequence() {} function

#include <AccelStepper.h>

// GLOBAL INTEGERS
#define ANALOG_THRESHOLD 505   // offset from 512 because of joystick calibration
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
int debug_counter = 0;
unsigned long last_time = 0;
bool toggled = false;
volatile bool interruption = false;
AccelStepper EW_motor(MOTOR_INTERFACE, 9, 11, 10, 12);
AccelStepper NS_motor(MOTOR_INTERFACE, 5, 7, 6, 8);

// FUNCTION DECLARATIONS

// SETUP FUNCTIONS
void PinSetup();
void MotorSetup();
void PennyGoHome();

// LOOP FUNCTIONS
void ReadPeripherals();
void UpdateSerial();
void RunByJoystick();
void UpdateElectromagnet();

// AUXILARY FUNCTIONS
void HandleInterrupt();
void CheckInterruptProtocal();

/**************************************************************************************************************/
void setup() {
  delay(1000); // NOTE: (line optional) prevents the setup from running when compiling the code from the computer
  Serial.begin(9600); 
  Serial.println("setup() initiated...");
  PinSetup();
  MotorSetup();
  attachInterrupt(digitalPinToInterrupt(SOUTH_LIMIT_PIN), HandleInterrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(WEST_LIMIT_PIN), HandleInterrupt, RISING);
  Serial.println("setup() completed!");
}

void homingSequence() {
  Serial.println("homingSequence() initiated...");
  PennyGoHome();
  interruption = false;
  Serial.println("homingSequence() completed!");
}

void loop() {
  // if (toggled) {
  //   UpdateSerial();
  // }

  CheckInterruptProtocal();
  ReadPeripherals();
  RunByJoystick();
  UpdateElectromagnet();
  // UpdateSerial();
}

/**************************************************************************************************************/

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
}

void PennyGoHome() {
  Serial.println("Sending Penny Home...");

  // HOME NS_motor
  NS_motor.move(300); // IMPORTANT: this move value should be higher than the next move value and large enough to unclick a limit switch
  NS_motor.setSpeed(SPEED);

  while (!digitalRead(SOUTH_LIMIT_PIN) && NS_motor.distanceToGo() != 0) { // IMPORTANT: the digitalRead(SOUTH_LIMIT_PIN) is to ensure the **North** limit is not triggered. Currently this limit is not wired up. 
    NS_motor.runSpeed(); // TODO: add a safety feature if the North Limit is reached
  }

  while (!digitalRead(SOUTH_LIMIT_PIN)) {
    NS_motor.setSpeed(-SPEED);
    NS_motor.runSpeed();
  }

  NS_motor.move(200);
  NS_motor.setSpeed(SPEED);

  while (NS_motor.distanceToGo() != 0) {
    NS_motor.runSpeed();
  }

  // HOME EW_motor
  EW_motor.move(300); // IMPORTANT: this move value should be higher than the next move value and large enough to unclick a limit switch
  EW_motor.setSpeed(SPEED);

  while (!digitalRead(WEST_LIMIT_PIN) && EW_motor.distanceToGo() != 0) { // IMPORTANT: the digitalRead(WEST_LIMIT_PIN) is to ensure the **East** limit is not triggered. Currently this limit is not wired up.
    EW_motor.runSpeed(); // TODO: add a safety feature if the Easth Limit is reached
  }

  while (!digitalRead(WEST_LIMIT_PIN)) {
    EW_motor.setSpeed(-SPEED);
    EW_motor.runSpeed();
  }

  EW_motor.move(200);
  EW_motor.setSpeed(SPEED);

  while (EW_motor.distanceToGo() != 0) {
    EW_motor.runSpeed();
  }

  // TODO: Set current location as datum point

  Serial.println("Penny went home. Good girl!");
}

void ReadPeripherals() {
  EW_pot = analogRead(EW_PIN);
  NS_pot = analogRead(NS_PIN);
  button_val = analogRead(BUTTON_PIN);
  
  if (analogRead(BUTTON_PIN) < ANALOG_THRESHOLD){
    toggled = !toggled;
    while (analogRead(BUTTON_PIN) < ANALOG_THRESHOLD) {}
  }
}

void UpdateSerial() {
  // VARIABLES
  Serial.print("Cycle Speed: ");
  Serial.print(millis() - last_time);
  Serial.print(" toggled: ");
  Serial.print(toggled);
  // Serial.print(" EW_motor.currentPosition: ");
  // Serial.print(EW_motor.currentPosition());
  Serial.print(" interruption: ");
  Serial.print(interruption);

  // INPUTS
  // Serial.print(" NS_pot: ");
  // Serial.print(NS_pot);
  // Serial.print(" EW_pot: ");
  // Serial.print(EW_pot);
  // Serial.print(" button_val: ");
  // Serial.print(button_val);
  
  // LIMIT SWITCHES
  // Serial.print(" SOUTH_LIMIT_PIN digitalRead: ");
  // Serial.print(digitalRead(SOUTH_LIMIT_PIN));
  // Serial.print( " WEST_LIMIT)PIN digitalRead: ");
  // Serial.print(digitalRead(WEST_LIMIT_PIN));

  // NEW LINE
  Serial.print("\n");
  last_time = millis();
}

void HandleInterrupt() {
  interruption = true;
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

void UpdateElectromagnet() {
  if (toggled) {
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(EM_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(EM_PIN, LOW);
  }
}

void CheckInterruptProtocal() {
  if (interruption) {
    Serial.println("INTERRUPTION DETECTED");

    // STOP POWER
    EW_motor.stop();
    NS_motor.stop();
    digitalWrite(EM_PIN, LOW);

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
      delay(175);
      digitalWrite(LED_PIN, LOW);
      delay(175);
      ReadPeripherals();

      // TODO: add safety feature in case user gives wrong input (for loop ~300 the ask again for input)

      // WEST
      if (EW_pot > ANALOG_THRESHOLD + DEADZONE_VAL) {
        while (digitalRead(WEST_LIMIT_PIN)) {
          EW_motor.setSpeed(-SPEED / 4);
          EW_motor.runSpeed();
        }
        for (int i = 0; i < INTERRUPT_OFFEST; i++) {
          EW_motor.setSpeed(-SPEED);
          EW_motor.runSpeed();
          delay(10);
        }
        break;

      // EAST
      } else if (EW_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
        while (digitalRead(WEST_LIMIT_PIN)) {
          EW_motor.setSpeed(SPEED / 4);
          EW_motor.runSpeed();
        }
        for (int i = 0; i < INTERRUPT_OFFEST; i++) {
          EW_motor.setSpeed(SPEED);
          EW_motor.runSpeed();
          delay(10);
        }
        break;

      // SOUTH
      } else if (NS_pot > ANALOG_THRESHOLD + DEADZONE_VAL) {
        while (digitalRead(SOUTH_LIMIT_PIN)) {
          NS_motor.setSpeed(-SPEED / 4);
          NS_motor.runSpeed();
        }
        for (int i = 0; i < INTERRUPT_OFFEST; i++) {
          NS_motor.setSpeed(-SPEED);
          NS_motor.runSpeed();
          delay(10);
        }
        break;

      // NORTH
      } else if (NS_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
        while (digitalRead(SOUTH_LIMIT_PIN)) {
          NS_motor.setSpeed(SPEED / 4);
          NS_motor.runSpeed();
        }
        for (int i = 0; i < INTERRUPT_OFFEST; i++) {
          NS_motor.setSpeed(SPEED);
          NS_motor.runSpeed();
          delay(10);
        }
        break;
      } 
    }

    interruption = false;
  }
}
