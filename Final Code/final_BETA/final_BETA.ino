// NOTE: main.cpp was modified to include homingSequence() {}, therefore if the IDE is updated we may need to modify this file again
// NOTE: having a separate homingSequence() {} overrides the bug that triggers the ISR prematurely immediately following setup(), caused by homing the carriage
// NOTE: having an unmodified main.cpp may run but not execute the homingSequence() {} function

#include <AccelStepper.h>
#include <MultiStepper.h>

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
#define EAST_MOTOR_LIMIT 3672  // Testing the EW limit 5 times we reached these step counts (3988, 3979, 3946, 3975, 3971)
#define NORTH_MOTOR_LIMIT 4637 // Testing the EW limit 5 times we reached these step counts (4917, 4980, 4916 ... larger than EAST_MOTOR_LIMIT) NOTE: These tests where approximated, the switch was not wired up
#define RELATIVE_BOARD_DATUM_EW -192
#define RELATIVE_BOARD_DATUM_NS -232

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
char received[15] = {' '};
char codes[4] = {' '};
long coordinates[2] = {0};
unsigned long last_time = 0;
bool toggled = false;
bool availableMove = false;
bool status = false;
volatile bool interruption = false;
AccelStepper EW_motor(MOTOR_INTERFACE, 9, 11, 10, 12);
AccelStepper NS_motor(MOTOR_INTERFACE, 5, 7, 6, 8);
MultiStepper carriage;

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
void CheckInterruptProtocal();
void GoToCoordinates();
void ReadSerial2();
void CarriageMove();

// AUXILARY FUNCTIONS
void HandleInterrupt();
void GoNorth();
void GoSouth();
void GoEast();
void GoWest();
void ReadSerial();
void CarriageMoveTo(long x, long y);
void StarWithin3500();
void ContinuousTest();
void WaitForPress();

/**************************************************************************************************************/
void setup() {
  delay(1000); // NOTE: (line optional) prevents the setup from running when compiling the code from the computer
  Serial.begin(115200); 
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
  ReadSerial2();
  CarriageMove();
  ReadPeripherals();
  RunByJoystick();
  if (toggled) {
    UpdateSerial();
    toggled = false;
  }
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

  carriage.addStepper(EW_motor);
  carriage.addStepper(NS_motor);
}

void PennyGoHome() {
  Serial.println("Sending Penny Home...");

  // HOME NS_motor
  NS_motor.move(300); // IMPORTANT: this move value should be large enough to unclick a limit switch
  NS_motor.setSpeed(SPEED);

  while (!digitalRead(SOUTH_LIMIT_PIN) && NS_motor.distanceToGo() != 0) { // IMPORTANT: the digitalRead(SOUTH_LIMIT_PIN) is to ensure the **North** limit is not triggered. Currently this limit is not wired up. 
    NS_motor.runSpeed(); // TODO: add a safety feature if the North Limit is reached
  }

  while (!digitalRead(SOUTH_LIMIT_PIN)) {
    NS_motor.setSpeed(-SPEED);
    NS_motor.runSpeed();
  }

  NS_motor.move(300 + RELATIVE_BOARD_DATUM_NS);
  NS_motor.setSpeed(SPEED);

  while (NS_motor.distanceToGo() != 0) {
    NS_motor.runSpeed();
  }

  Serial.println("... almost there, Penny!");

  // HOME EW_motor
  EW_motor.move(300); // IMPORTANT: this move value should be large enough to unclick a limit switch
  EW_motor.setSpeed(SPEED);

  while (!digitalRead(WEST_LIMIT_PIN) && EW_motor.distanceToGo() != 0) { // IMPORTANT: the digitalRead(WEST_LIMIT_PIN) is to ensure the **East** limit is not triggered. Currently this limit is not wired up.
    EW_motor.runSpeed(); // TODO: add a safety feature if the Easth Limit is reached
  }

  while (!digitalRead(WEST_LIMIT_PIN)) {
    EW_motor.setSpeed(-SPEED);
    EW_motor.runSpeed();
  }

  EW_motor.move(300 + RELATIVE_BOARD_DATUM_EW);
  EW_motor.setSpeed(SPEED);

  while (EW_motor.distanceToGo() != 0) {
    EW_motor.runSpeed();
  }

  NS_motor.setCurrentPosition(0);
  EW_motor.setCurrentPosition(0);

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
  // Serial.print("Cycle Speed: ");
  // Serial.print(millis() - last_time);
  // Serial.print(" toggled: ");
  // Serial.print(toggled);
  Serial.print(" EW_motor.currentPosition: ");
  Serial.print(EW_motor.currentPosition());
  Serial.print(" NS_motor.currentPosition: ");
  Serial.print(NS_motor.currentPosition());
  // Serial.print(" interruption: ");
  // Serial.print(interruption);

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
    CheckInterruptProtocal();
    EW_motor.runSpeed();
  }

  if (NS_pot > ANALOG_THRESHOLD + DEADZONE_VAL || NS_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
    NS_speed = map(NS_pot, 0, 1023, SPEED, -SPEED);
    NS_motor.setSpeed(NS_speed);
    CheckInterruptProtocal();
    NS_motor.runSpeed();
  }
}

void UpdateElectromagnet(bool val) {
  if (val) {
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(EM_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(EM_PIN, LOW);
  }
}

void CheckInterruptProtocal() {
  if (interruption) {
    UpdateSerial();
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

    NS_motor.moveTo(NS_motor.currentPosition());
    EW_motor.moveTo(EW_motor.currentPosition());
    
    interruption = false;
  }
}

void GoNorth() {
    NS_motor.setSpeed(SPEED);
    NS_motor.runSpeed();
}

void GoSouth() {
    NS_motor.setSpeed(-SPEED);
    NS_motor.runSpeed();
}

void GoEast() {
    EW_motor.setSpeed(SPEED);
    EW_motor.runSpeed();
}

void GoWest() {
    EW_motor.setSpeed(-SPEED);
    EW_motor.runSpeed();
}

void GoToCoordinates() {
  Serial.print("COORDINATES x: ");
  Serial.print(coordinates[0]);
  Serial.print(", y: ");
  Serial.println(coordinates[1]);
  Serial.println("Go to these coordinates?");
  Serial.println("North == Yes || South == No");
  toggled = false;
  while (true) {
    ReadPeripherals();
    if (NS_pot > ANALOG_THRESHOLD + DEADZONE_VAL) {
      Serial.println("Will not go. (Delay 1 second)");
      status = false;
      delay(1000);
      return;
    }
    if (NS_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
      Serial.println("Moving...");
      status = true;
      break;
    }
    digitalWrite(LED_PIN, HIGH);
    delay(125);
    digitalWrite(LED_PIN, LOW);
    delay(125);
  }

  carriage.moveTo(coordinates);
  while (NS_motor.distanceToGo() != 0 || EW_motor.distanceToGo() != 0) {
    CheckInterruptProtocal();
    carriage.run();
  }
  Serial.println("Arrived!");
}

void ReadSerial2() {
  if (Serial.available() <= 0) {
    return;
  }

  //<^0000,0000_00>  <(Open) >(Close) 0000,0000(Coordinate destination format) ^(EM  on) _(EM off) 00(instruction code. 01=1 02=2 21=21... for pythong to verify a step wasn't missed)
  delay(50);
  while (Serial.available() > 0) {
    for (int i = 0; i < 15; i++) {
      received[i] = Serial.read();
    }
  }
  while (Serial.available() > 0) {
    Serial.read();
  }

  if (received[0] == '<' && received[6] == ',' && received[14] == '>') {
    availableMove = true;

    coordinates[0] = 0;
    coordinates[1] = 0;
    codes[0] = codes[1] = codes[2] = codes[3] = ' ';

    int j = 1000;
    for (int i = 2; i < 6; i++) {
      coordinates[0] += (received[i] - '0') * j;
      coordinates[1] += (received[i + 5] - '0') * j;
      j /= 10;
    }
    codes[0] = char(received[1]);   // UDATE ELECTROMAGNET BEFORE MOVE
    codes[1] = char(received[11]);  // UDATE ELECTROMAGNET AFTER MOVE
    codes[2] = char(received[12]);  // FIRST PYTHON CODE DIGIT
    codes[3] = char(received[13]);  // SECOND PYTHON CODE DIGIT

    for (int i; i < 15; i++) {
      received[i] = ' '; //<^0000,0000_AA>  <(Open) >(Close) 0000,0000(Coordinate destination format) ^(EM  on) _(EM off) AA(instruction code. AA=1 AB=2 AC3... for pythong to verify a step wasn't missed)
    }

  } else {
    Serial.println("INVALID DATA RECEIVED");
    for (int i = 0; i < 15; i++) {
      received[i] = ' ';
    }
  }
  return;
}

void ReadSerial() {
  int index = 0;
  int count = 0;
  int serial[9] = {0};

  Serial.println("reading in serial...");
  while (Serial.available() > 0) {
    serial[index] = Serial.read() - '0';
    index += 1;
    count += 1;
    if (count >= 9) { break; }
  }
  while (Serial.available() > 0) {Serial.read();}

  status = (serial[4] == ',' - '0') ? true : false; // CHECKS FOR ',' at index 4
  switch (status) {
    case true:
      Serial.println("printing serial data...");
      serial[4] = ',';
      coordinates[0] = serial[0] * 1000 + serial[1] * 100 + serial[2] * 10 + serial[3];
      coordinates[1] = serial[5] * 1000 + serial[6] * 100 + serial[7] * 10 + serial[8];
      Serial.print(coordinates[0]);
      Serial.print(", ");
      Serial.println(coordinates[1]);

      index = 0;
      count = 0;
      for (int i = 0; i < 9; i++) {
        serial[i] = 0;
      }
      break;
    case false:
      Serial.println("INVALID COORDINATE FORMAT");
      index = 0;
      count = 0;
      for (int i = 0; i < 9; i++) {
        serial[i] = 0;
      }
      break;
  }
}

void CarriageMove() {
  if (!availableMove) {
    return;
  }

  UpdateElectromagnet((codes[0] == '^') ? true : false);
  // Serial.print("EM:");
  // Serial.print(codes[0]);
  // Serial.print(" Moving to x:");
  // Serial.print(coordinates[0]);
  // Serial.print(" y:");
  // Serial.print(coordinates[1]);
  // Serial.print("... ");
  carriage.moveTo(coordinates);
  while (NS_motor.distanceToGo() != 0 || EW_motor.distanceToGo() != 0) {
    CheckInterruptProtocal();
    carriage.run();
  }
  // Serial.print("Arrived! EM:");
  // Serial.print(codes[1]);
  // Serial.print(" Waypoint code:");
  // Serial.print(codes[2]);
  // Serial.println(codes[3]);
  UpdateElectromagnet((codes[1] == '^') ? true : false);
  Serial.print(codes[2]);
  Serial.println(codes[3]);

  availableMove = false;
  return;
}

void StarWithin3500() {
  int wait = 5000;
  CarriageMoveTo(3500, 1750);
  delay(wait);
  CarriageMoveTo(2895, 2582);
  delay(wait);
  CarriageMoveTo(2290, 3414);
  delay(wait);
  CarriageMoveTo(1312, 3096);
  delay(wait);
  CarriageMoveTo(334, 2778);
  delay(wait);
  CarriageMoveTo(334, 1750);
  delay(wait);
  CarriageMoveTo(334, 721);
  delay(wait);
  CarriageMoveTo(1312, 402);
  delay(wait);
  CarriageMoveTo(2290, 85);
  delay(wait);
  CarriageMoveTo(2895, 917);
  delay(wait);
}

void ContinuousTest() {
  long mid[2] = {EAST_MOTOR_LIMIT / 2, NORTH_MOTOR_LIMIT / 2};
  CarriageMoveTo(0, 0);
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(EAST_MOTOR_LIMIT, 0);
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(EAST_MOTOR_LIMIT, NORTH_MOTOR_LIMIT);
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(NORTH_MOTOR_LIMIT, 0);
  CarriageMoveTo(mid[0], mid[1]);
}

void WaitForPress() {
  toggled = false;
  while (!toggled) {
    digitalWrite(LED_PIN, HIGH);
    delay(150);
    digitalWrite(LED_PIN, LOW);
    delay(150);
    ReadPeripherals();
  }
}
