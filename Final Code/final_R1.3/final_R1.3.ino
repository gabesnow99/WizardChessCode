// NOTE: main.cpp was modified to include homingSequence() {}, therefore if the IDE is updated we may need to modify this file again
// NOTE: having a separate homingSequence() {} overrides the bug that triggers the ISR prematurely immediately following setup(), caused by homing the carriage
// NOTE: having an unmodified main.cpp may run but not execute the homingSequence() {} function
// NOTE: Board Height is edited in the Definitions.h header file
// NOTE: PIECE CREATION must be declared globally, and initialized in setup(). I could not figure out another way

#include <AccelStepper.h>
#include <MultiStepper.h>
#include "C:\Users\joshu\Documents\Personal\Projects worth doing\Chess\WizardChessCode\Final Code\final_R1.3\Chess.h"

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
long coordinates[2] = {0};
unsigned long last_time = 0;
bool toggled = false;
bool switch_val = false;
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

// AUXILARY FUNCTIONS
void HandleInterrupt();
void GoNorth();
void GoSouth();
void GoEast();
void GoWest();
void ReadSerial();
void CarriageMoveTo(long x, long y);
void StarWithin3500();
void ContinuousTest(int msec);
void WaitForPress();
void AccuracyTest();

// PIECE CREATION
Piece* pieces[NUM_PIECES];

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
  delay(1000);

  // PIECE CREATION
  for (int i = 0; i < NUM_PIECES; i++) {
    char file, rank;
    if (i < 8) {
        file = 'A' + i;
        rank = '1';
    } else if (i >= 8 && i < 16) {
        file = 'A' + (i - 8);
        rank = '2';
    } else if (i >= 16 && i < 24) {
        file = 'A' + (i - 16);
        rank = '7';
    } else {
        file = 'A' + (i - 24);
        rank = '8';
    }
    pieces[i] = new Piece(file, rank);
  }

  // CHEKCING PIECE CREATION
  // for (int i = 0; i < NUM_PIECES; i++) {
  //   Serial.print("Pieces numer ");
  //   Serial.print(i);
  //   Serial.print(": ");
  //   Serial.println(StoI(pieces[i]->getSquare()));
  // }  

  // int piece = BP7;
  // Serial.print(pieces[piece]->getSquare().file);
  // Serial.println(pieces[piece]->getSquare().rank);
  // END CHECK
}


void homingSequence() {
  Serial.println("homingSequence() initiated...");
  PennyGoHome();
  interruption = false;
  Serial.println("homingSequence() completed!");
}

void loop() {
  ReadPeripherals();
  // if (toggled) {
  //   toggled = !toggled;
  //   Square a = UserInputSquare();
  //   Serial.print("User input Square: ");
  //   Serial.print(a.file);
  //   Serial.print(" ");
  //   Serial.print(a.rank);
  //   Serial.print(" ");
  //   Serial.print(a.x);
  //   Serial.print(" ");
  //   Serial.println(a.y);
  //   Serial.print("Square to index: ");
  //   int index = StoI(a);
  //   Serial.println(index);
  //   Serial.print("Index to Square: ");
  //   Square b = ItoS(index);
  //   Serial.print(b.file);
  //   Serial.print(" ");
  //   Serial.print(b.rank);
  //   Serial.print(" ");
  //   Serial.print(b.x);
  //   Serial.print(" ");
  //   Serial.println(b.y);
  // }

  if (toggled) {
    toggled = !toggled;
    int piece = BK;
    Square newSquare = UserInputSquare();
    Serial.print("User moved piece from: ");
    Serial.print(pieces[piece]->getSquare().file);
    Serial.print(" ");
    Serial.print(pieces[piece]->getSquare().rank);
    Serial.print(" ");
    Serial.print(pieces[piece]->getSquare().x);
    Serial.print(" ");
    Serial.println(pieces[piece]->getSquare().y);
    CarriageMoveTo(pieces[piece]->getSquare().x, pieces[piece]->getSquare().y);
    UpdateElectromagnet(true);
    delay(1000);
    Serial.print("And moved it to: ");
    pieces[piece]->moveTo(newSquare);
    Serial.print(pieces[piece]->getSquare().file);
    Serial.print(" ");
    Serial.print(pieces[piece]->getSquare().rank);
    Serial.print(" ");
    Serial.print(pieces[piece]->getSquare().x);
    Serial.print(" ");
    Serial.println(pieces[piece]->getSquare().y);
    CarriageMoveTo(pieces[piece]->getSquare().x, pieces[piece]->getSquare().y);
    UpdateElectromagnet(false);
    Serial.println("Sending Penny home once more...");
    CarriageMoveTo(-200, -200);
    Serial.print("Well done, everyone!!  .... oops going a bit too far...");
    CarriageMoveTo(0, -300);
  }
  RunByJoystick();
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

  NS_motor.move(300);
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

  EW_motor.move(300);
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
  Serial.print("Cycle Speed: ");
  Serial.print(millis() - last_time);
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
  // TEMPORARY BUG SOLUTION (DOESN'T WORK)
  // Serial.println("INTERRUPTION DETECTED! Must restart arduino.");
  // while (true) {}
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

void UpdateElectromagnet(bool value) {
  if (value) {
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
      switch_val = false;
      delay(1000);
      return;
    }
    if (NS_pot < ANALOG_THRESHOLD - DEADZONE_VAL) {
      Serial.println("Moving...");
      switch_val = true;
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

  switch_val = (serial[4] == ',' - '0') ? true : false; // CHECKS FOR ',' at index 4
  switch (switch_val) {
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

void CarriageMoveTo(long x, long y) {
  long coordinates[2] = {x, y};
  Serial.print("moving to x:");
  Serial.print(coordinates[0]);
  Serial.print(" y:");
  Serial.print(coordinates[1]);
  Serial.print("... ");
  carriage.moveTo(coordinates);
  while (NS_motor.distanceToGo() != 0 || EW_motor.distanceToGo() != 0) {
    CheckInterruptProtocal();
    carriage.run();
  }
  Serial.println("Arrived!");
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

void ContinuousTest(int msec) {
  long mid[2] = {EAST_MOTOR_LIMIT / 2, NORTH_MOTOR_LIMIT / 2};
  CarriageMoveTo(0, 0);
  delay(msec);
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(EAST_MOTOR_LIMIT, 0);
  delay(msec);
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(EAST_MOTOR_LIMIT, NORTH_MOTOR_LIMIT - 500);
  delay(msec);
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(0, NORTH_MOTOR_LIMIT - 500);
  delay(msec);
  CarriageMoveTo(mid[0], mid[1]);
  delay(msec);
}

void WaitForPress() {
  toggled = false;
  while (!toggled) {
    digitalWrite(LED_PIN, HIGH);
    delay(125);
    digitalWrite(LED_PIN, LOW);
    delay(125);
    ReadPeripherals();
  }
  toggled = false;
}

void AccuracyTest() {
  long mid[2] = {EAST_MOTOR_LIMIT / 2, NORTH_MOTOR_LIMIT / 2};
  CarriageMoveTo(0, 0);
  WaitForPress();
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(EAST_MOTOR_LIMIT, 0);
  WaitForPress();
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(EAST_MOTOR_LIMIT, NORTH_MOTOR_LIMIT - 500);
  WaitForPress();
  CarriageMoveTo(mid[0], mid[1]);
  CarriageMoveTo(0, NORTH_MOTOR_LIMIT - 500);
  WaitForPress();
  CarriageMoveTo(mid[0], mid[1]);
  WaitForPress();
}
