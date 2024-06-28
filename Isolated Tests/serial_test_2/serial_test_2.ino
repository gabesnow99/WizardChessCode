#define BUTTON_PIN A3
#define ANALOG_THRESHOLD 505

int serial[11] = {0};
int numbers[2] = {0};
int index = 0;
int count = 0;
bool toggled = false;
bool switch_val = false;

void setup() {
  Serial.begin(9600);
  Serial.println("Setup Complete");
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void homingSequence() {};

void loop() {
  ReadPeripherals();
  if (toggled) {
    MyReadSerial();
    toggled = false;
    delay(300);
  }
}

void MyReadSerial() {
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
      numbers[0] = serial[0] * 1000 + serial[1] * 100 + serial[2] * 10 + serial[3];
      numbers[1] = serial[5] * 1000 + serial[6] * 100 + serial[7] * 10 + serial[8];
      Serial.print(numbers[0]);
      Serial.print(", ");
      Serial.print(numbers[1]);

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

void ReadPeripherals() {
  if (analogRead(BUTTON_PIN) < ANALOG_THRESHOLD){
    toggled = !toggled;
    while (analogRead(BUTTON_PIN) < ANALOG_THRESHOLD) {}
  }
}