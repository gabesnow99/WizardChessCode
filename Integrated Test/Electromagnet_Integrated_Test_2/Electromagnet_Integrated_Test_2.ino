#include <AccelStepper.h>

// GLOBAL INTEGERS
#define BUTTON_THRESHOLD 500
#define DIGITAL_THRESHOLD .5
#define SPR 2038               // steps per revolution
#define SPEED 14 
#define NORTH 250
#define SOUTH 750
#define EAST 250
#define WEST 750
#define MOTOR_INTERFACE 4

// ANALOG PINS
#define EW_PIN A4              //VRy on joystick board
#define NS_PIN A5              //VRx on joystick board
#define BUTTON_PIN A3          //SW  on joystick board

// DIGITAL PINS
#define LED_PIN 13
#define EM_PIN 3               //Electromagnet
#define SOUTH_LIMIT_PIN 2
#define WEST_LIMIT_PIN 12

// VARIABLES
int NS_pot = 0;
int EW_pot = 0;
int button_val = 0;
int cycle_speed = 0;
unsigned long time = 0;
volatile bool limit_pressed = false;
bool toggled = false;
AccelStepper east_west(MOTOR_INTERFACE, 8, 10, 9, 11);
AccelStepper north_south(MOTOR_INTERFACE, 4, 6, 5, 7);

// FUNCTION DECLARATIONS
void home();

void setup() {
  home();
}

void loop() {
}

// FUNCTION DEFINITIONS
void home() {
}