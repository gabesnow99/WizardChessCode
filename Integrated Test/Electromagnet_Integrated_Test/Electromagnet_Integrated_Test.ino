#include <Stepper.h>

// Global Integers
#define BUTTON_THRESHOLD 500
#define DIGITAL_THRESHOLD .5
#define SPR 2038 // steps per revolution
#define SPEED 14 
#define MAP1 250
#define MAP2 750
#define MAP3 250
#define MAP4 750

// Analog Pins
#define outer_pot_pin A4 //VRy on joystick board
#define inner_pot_pin A5 //VRx on joystick board
#define button_pin A3    //SW  on joystick board

// Digital Pins
#define LED_pin 13
#define EM_pin 4

// Limit Switch
#define limit_south 2
#define limit_west 3

// Variables
int outer_pot_val = 0;
int inner_pot_val = 0;
int button_val = 0;
int cycle_speed = 0;
unsigned long time = 0;
Stepper outer_axis = Stepper(SPR, 9, 11, 10, 12);
Stepper inner_axis = Stepper(SPR, 5, 7, 6, 8);
volatile bool toggled = false; 

float last_timestamp = 0;

// Functions
bool isButtonPushed();
void pennyGoHome();
void stepNorth(int steps);
void stepSouth(int steps);
void stepEast(int steps);
void stepWest(int steps);
// void handleInterrupt(); // BUG: LED status seems to be accurate but often button is unreliable


void setup() {
  Serial.begin(9600);
  pinMode(LED_pin, OUTPUT);
  pinMode(outer_pot_pin, INPUT);
  pinMode(inner_pot_pin, INPUT);
  pinMode(button_pin, INPUT_PULLUP);
  pinMode(EM_pin, OUTPUT);
  pinMode(limit_south, INPUT_PULLUP);
  pinMode(limit_west, INPUT_PULLUP);
  outer_axis.setSpeed(SPEED);
  inner_axis.setSpeed(SPEED);

//  pennyGoHome();

  // attachInterrupt(digitalPinToInterrupt(button_pin), handleInterrupt, FALLING); // BUG: LED status seems to be accurate but often button is unreliable
}

void loop() {

  // Cycle Speed Debugger
  cycle_speed = millis() - time;
  time = millis();
  // Serial.print("cycle_speed: ");
  // Serial.print(cycle_speed);

  // // joystick variable debugger
  outer_pot_val = analogRead(outer_pot_pin);
  inner_pot_val = analogRead(inner_pot_pin);
  button_val = analogRead(button_pin);
  // Serial.print(" toggled: ");
  // Serial.print(toggled);
  // Serial.print(" button_val: ");
  // Serial.println(button_val);
  // Serial.print(" outer_pot_val: ");
  // Serial.print(outer_pot_val);
  // Serial.print(" inner_pot_val: ");
  // Serial.println(inner_pot_val);

  // // button test
  // if (isButtonPushed()){
  //   digitalWrite(LED_pin, HIGH);
  //   delay(500);
  //   digitalWrite(LED_pin, LOW);
  //   delay(500);
  // }

  // // button trigger interrupt test
  // if (toggled && (millis() - last_timestamp) > 50){
  //   last_timestamp = millis();
  //   Serial.print("ONCE ");
  //   outer_axis.step(SPR / 100);
  // }

  // LED shows toggle status
  isButtonPushed();
  if (toggled){
    digitalWrite(LED_pin, HIGH);
    digitalWrite(EM_pin, HIGH);
  } 
  if (!toggled) {
    digitalWrite(LED_pin, LOW);
    digitalWrite(EM_pin, LOW);
  }

  Serial.print("limit south: ");
  Serial.print(digitalRead(limit_south));
  Serial.print(" limit west: ");
  Serial.print(digitalRead(limit_west));
  Serial.print("\n");

  // Control Axes
  if (digitalRead(limit_south) || digitalRead(limit_west)) {
    return;
  }
  if (outer_pot_val < MAP1 /*&& !toggled*/) {
    outer_axis.step(5);
  }
  if (outer_pot_val > MAP2 /*&& !toggled*/) {
    outer_axis.step(-5);
  }
  if (inner_pot_val < MAP3 /*&& !toggled*/) {
    inner_axis.step(5);
  }
  if (inner_pot_val > MAP4 /*&& !toggled*/) {
    inner_axis.step(-5);
  }
//   if (outer_pot_val < MAP1 && toggled){
//     outer_axis.step(SPR / 200);
//     delay(200);
//   }
//   if (outer_pot_val > MAP2 && toggled){
//     outer_axis.step(-SPR / 200);
//     delay(200);
//   }
//   if (inner_pot_val < MAP3 && toggled){
//     inner_axis.step(SPR / 200);
//     delay(200);
//   }
//   if (inner_pot_val > MAP4 && toggled){
//     inner_axis.step(-SPR/ 200);
//     delay(200);
//   }
}


// Function Definitions
bool isButtonPushed() {
  if (analogRead(button_pin) <= BUTTON_THRESHOLD) {
    if (toggled == false)
    {
      toggled = true;
    }
    else
    {
      toggled = false;
    }     
    while (analogRead(button_pin) <= BUTTON_THRESHOLD) {}
    return true;
  } else {
    return false;
  }
}

void pennyGoHome() {
  while (!digitalRead(limit_south)) {
    stepSouth(10);
  }
  while (!digitalRead(limit_west)) {
    stepWest(10);
  }
}

void stepNorth(int steps = SPR/50) {
  inner_axis.step(steps);
}

void stepSouth(int steps = SPR/50) {
  inner_axis.step(-steps);
}

void stepEast(int steps = SPR/50) {
  outer_axis.step(steps);
}

void stepWest(int steps = SPR/50) {
  outer_axis.step(-steps);
}

// void handleInterrupt(){ // BUG: LED status seems to be accurate but often button is unreliable 
  // if (toggled == false)
  // {
  //   toggled = true;
  // }
  // else
  // {
  //   toggled = false;
  // } 
// }
