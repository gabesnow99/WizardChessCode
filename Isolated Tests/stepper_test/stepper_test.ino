#include <Stepper.h>

int led = 13;

const int stepsPerRevolution = 2038;
Stepper step_son = Stepper(stepsPerRevolution, 8, 10, 9, 11); //this order is not intuitive or explained but will fix the backwards motion

void setup() {
  pinMode(led, OUTPUT);
  step_son.setSpeed(10);
}

void loop() {
  digitalWrite(led, LOW);
  step_son.step(.5*stepsPerRevolution);

  digitalWrite(led, HIGH);
  step_son.step(-.5*stepsPerRevolution);
}