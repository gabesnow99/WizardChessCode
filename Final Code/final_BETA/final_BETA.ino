// NOTE: main.cpp was modified to include homingSequence() {}, therefore if the IDE is updated we may need to modify this file again
// NOTE: having a separate homingSequence() {} overrides the bug that triggers the ISR prematurely immediately following setup(), caused by homing the carriage
// NOTE: having an unmodified main.cpp may run but not execute the homingSequence() {} function
// NOTE: FOR PYTHON's SAKE please leave fun Serial.print() formatting for the homing sequence and then only send codes via Serial.write()
// -----   this may prevent rare unpredictable behavior and is standard practice for byte serial sharing. Further fun formatting can happen in python  

#include <AccelStepper.h>
#include <MultiStepper.h>

// GLOBAL INTEGERS
#define ANALOG_THRESHOLD 505   // offset from 512 because of joystick calibration
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
int EW_speed = 0;
int NS_speed = 0;
long coordinates[9][2] = {0};
char codes[9][4] = {' '};

unsigned long last_time = 0;
bool toggled = false;
bool availableMove = false;
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
void ReadInSerial();
void MoveCarriage();

// AUXILARY FUNCTIONS
void HandleInterrupt();
void CheckInterruptProtocal();
void UpdateElectromagnet();
void GoNorth();
void GoSouth();
void GoEast();
void GoWest();
void HandleReceived(char* waypoint, int code1);
void MoveToCoordinate(long* coordArray, char* codeArray);

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
  Serial.write("\n@"); // CODE FOR PYTHON
}

void loop() {
  ReadInSerial();
  MoveCarriage();
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

void ReadInSerial() {
  if (Serial.available() <= 0) {
    return;
  }

  //<^0000,0000_##>  <(Open) >(Close) 0000,0000(Coordinate destination format) ^(EM  on) _(EM off) ##(instruction code. first # is current waypoint. second # is final waypoint. for python to verify a step wasn't missed)
  delay(75);
  char received[15] = {' '};
  for (int i = 0; i < 15; i++) {
      received[i] = Serial.read();
  }
  
  int code1 = received[12] - '0' - 1;
  int code2 = received[13] - '0' - 1;
  HandleReceived(received, code1);
  while (code1 < code2) {
    while (Serial.available() > 0) {
      for (int i = 0; i < 15; i++) {
        received[i] = Serial.read();
      }
      code1 = received[12] - '0';
    }
    HandleReceived(received, code1);
  }

  while (Serial.available() > 0) {
    Serial.read();
  }

  availableMove = true;
  Serial.write('@');
  return;
}

void MoveCarriage() {
  if (!availableMove) {
    return;
  }

  int numMoves = codes[0][3] - '0';
  for (int i = 0; i < numMoves; i++) {
    MoveToCoordinate(coordinates[i], codes[i]);
  }

  availableMove = false;
}

void MoveToCoordinate(long* coordArray, char* codeArray) {
  UpdateElectromagnet((codeArray[0] == '^') ? true : false);
  carriage.moveTo(coordArray);
  while (NS_motor.distanceToGo() != 0 || EW_motor.distanceToGo() != 0) {
    CheckInterruptProtocal();
    carriage.run();
  }
  UpdateElectromagnet((codeArray[1] == '^') ? true : false);
  Serial.write(codeArray[2]);
}

void HandleReceived(char* received, int code1) {
  Serial.print("code1:"); Serial.print(code1); // BUG WHY IS THIS VALUE NOT CHANGING
  if (received[0] == '<' && received[6] == ',' && received[14] == '>') {
    coordinates[code1][0] = 0;
    coordinates[code1][1] = 0;
    int j = 1000;
    for (int i = 2; i < 6; i++) {
      coordinates[code1][0] += (received[i] - '0') * j;
      coordinates[code1][1] += (received[i + 5] - '0') * j;
      j /= 10;
    }
    codes[code1][0] = received[1];   // UDATE ELECTROMAGNET BEFORE MOVE
    codes[code1][1] = received[11];  // UDATE ELECTROMAGNET AFTER MOVE
    codes[code1][2] = received[12];  // FIRST PYTHON CODE CODE
    codes[code1][3] = received[13];  // SECOND PYTHON CODE CODE
    // Serial.print("code1:");Serial.print(code1);

  } else {
    Serial.println("INVALID DATA RECEIVED. CARRIAGE NOT MOVED");
    availableMove = false;
  }
}
