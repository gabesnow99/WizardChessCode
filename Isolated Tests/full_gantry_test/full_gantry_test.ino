#include <Stepper.h>

int led = 13;
int serialData = 0;
int speed = 14;

const int spr = 2038; //spr = stepsPerRevolution

Stepper outer_axis = Stepper(spr, 8, 10, 9, 11);
Stepper inner_axis = Stepper(spr, 4, 6, 5, 7);

void setup() { 
  Serial.begin(9600); //start talking with the computer. 9600 just tells the rate.
  pinMode(led, OUTPUT);
  outer_axis.setSpeed(speed);
  inner_axis.setSpeed(speed);
}

void loop() {
if (Serial.available() > 0) { //Serial.available will tell the board to look at the information being sent to it through the serial port.
  //these 2 lines are not nessecary, but it's cool to see how the ARDUINO thinks.
  serialData = Serial.read(); //The arduino reads this data and writes it as one of our variables.
  Serial.println(serialData); //The arduino prints this data to the serial monitor so we can see what it sees.
  //NOTE: All the data the arduino sends will be converted to ASCII. This is why typing 1 will return a value of 49 (the ASCII value of 1).
  //Also, 10 is typed after every input becasue 10 is the ASCII value for enter.
}

if (serialData == 49) {
  outer_axis.step(spr / 20);
}

if (serialData == 50) {
  outer_axis.step(-spr / 20);
}

if (serialData == 51) {
  inner_axis.step(spr / 20);
}

if (serialData == 52) {
  inner_axis.step(-spr / 20);
}

// if (data > 0) {
//   for (int i=1; i<=5; i++) {
//     digitalWrite(led, HIGH);
//     delay (250); 
//     digitalWrite(led, LOW);
//     delay (250);
//     data = 0;
//   }
// }
}
