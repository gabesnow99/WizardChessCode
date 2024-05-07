#include <Stepper.h>

// Global Integers
#define BUTTON_THRESHOLD 500
#define SPR 2038 // steps per revolution
#define SPEED 14 
#define MAP1 250
#define MAP2
#define MAP3
#define MAP4

// Analog Pins
#define outer_pot_pin A4 //VRy on joystick board
#define inner_pot_pin A5 //VRx on joystick board
#define button_pin 2    //SW  on joystick board

// Digital Pins
#define LED_pin 13

// Variables
int outer_pot_val = 0;
int inner_pot_val = 0;
int button_val = 0;
int cycle_speed = 0;
unsigned long time = 0;
Stepper outer_axis = Stepper(SPR, 8, 10, 9, 11);
Stepper inner_axis = Stepper(SPR, 4, 6, 5, 7);
volatile bool triggered = false;

float last_timestamp = 0;

// Functions
bool isButtonPushed();


void setup() {
  Serial.begin(9600);
  pinMode(LED_pin, OUTPUT);
  pinMode(outer_pot_pin, INPUT);
  pinMode(inner_pot_pin, INPUT);
  pinMode(button_pin, INPUT_PULLUP);
  outer_axis.setSpeed(SPEED);
  inner_axis.setSpeed(SPEED);

  attachInterrupt(digitalPinToInterrupt(button_pin), handleInterrupt, FALLING);
}

void loop() {
  // // Cycle Speed Debugger
  // cycle_speed = millis() - time;
  // time = millis();
  // Serial.print("cycle_speed: ");
  // // Serial.print(cycle_speed); // switch if last debugger
  // Serial.println(cycle_speed); // switch if not last debugger


  // // joystick debugger
  // outer_pot_val = analogRead(outer_pot_pin);
  // inner_pot_val = analogRead(inner_pot_pin);
  // button_val = analogRead(button_pin);
  // Serial.print(" button_val: ");
  // Serial.print(button_val);
  // Serial.print(" outer_pot_val: ");
  // Serial.print(outer_pot_val);
  // Serial.print(" inner_pot_val: ");
  // Serial.println(inner_pot_val);

  // // button test
  // if (isButtonPushed()){ //bug: I don't think enough current is going to the LED. Why?
  //   digitalWrite(LED_pin, HIGH);
  //   delay(500);
  //   digitalWrite(LED_pin, LOW);
  //   delay(500);
  // }

  if (triggered && (millis() - last_timestamp) > 50){
    last_timestamp = millis();
    Serial.print("ONCE ");
    outer_axis.step(SPR / 20);
    triggered = false;
  }
}


// Function Definitions
bool isButtonPushed(){
  if (analogRead(button_pin) <= BUTTON_THRESHOLD){
    return true;
  } else {
    return false;
  }
}

void handleInterrupt(){
  int sensorValue = analogRead(button_pin);
  if (sensorValue < BUTTON_THRESHOLD){
    triggered = true;
  }
}
