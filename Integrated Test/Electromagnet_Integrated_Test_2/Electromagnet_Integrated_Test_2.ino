#include <AccelStepper.h>

// GLOBAL INTEGERS
#define BUTTON_THRESHOLD 512
#define DIGITAL_THRESHOLD .5
#define SPR 2038               // steps per revolution
#define SPEED 14 
#define NORTH 250
#define SOUTH 750
#define EAST 250
#define WEST 750
#define MOTOR_INTERFACE 4
#define SPEED 14

// ANALOG PINS
#define EW_PIN A4              //VRy on joystick board
#define NS_PIN A5              //VRx on joystick board
#define BUTTON_PIN A3          //SW  on joystick board

// DIGITAL PINS
#define LED_PIN 13
#define EM_PIN 4               //Electromagnet
#define SOUTH_LIMIT_PIN 2
#define WEST_LIMIT_PIN 3

// VARIABLES
int EW_pot = 0;
int NS_pot = 0;
int button_val = 0;
int cycle_speed = 0;
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
void HandleInterrupt();

/*******************************************************************************/
void setup() {
  PinSetup();
  MotorSetup();
  attachInterrupt(digitalPinToInterrupt(SOUTH_LIMIT_PIN), HandleInterrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(WEST_LIMIT_PIN), HandleInterrupt, RISING);
  Serial.begin(9600);
  Home();
}

void loop() {
  ReadPeripherals();
  UpdateSerial();
}

/*******************************************************************************/

// FUNCTION DEFINITIONS
void PinSetup() {
  pinMode(EW_PIN, INPUT);
  pinMode(NS_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(SOUTH_LIMIT_PIN, INPUT_PULLUP);
  pinMode(WEST_LIMIT_PIN, INPUT_PULLUP);

  pinMode(EM_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void MotorSetup() {
  EW_motor.setSpeed(SPEED);
  NS_motor.setSpeed(SPEED);
  // EW_motor.setMaxSpeed();
  // NS_motor.setMaxSpeed();
  // EW_motor.setAcceleration();
  // NS_motor.setAcceleration();
}

void Home() {
}

void ReadPeripherals() {
  EW_pot = analogRead(EW_PIN);
  NS_pot = analogRead(NS_PIN);
  button_val = analogRead(BUTTON_PIN);
  time = millis();
}

void UpdateSerial() {
  Serial.print("Cycle Speed: ");
  Serial.print(millis() - last_time);
  Serial.print(" NS_pot: ");
  Serial.print(NS_pot);
  Serial.print(" EW_pot: ");
  Serial.print(EW_pot);
  Serial.print(" button_val: ");
  Serial.print(button_val);

  Serial.print()

  Serial.print("\n");
  last_time = millis();
}

void HandleInterrupt() {
  digitalWrite(LED_PIN, HIGH);
  EW_motor.stop();
  NS_motor.stop();
  // add the electromagnet turning off
  while(1) {} //put a read user input funtion here that moves the motor in the right direction
}