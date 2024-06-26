int numbers[2] = {0, 0};
int index = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Setup Complete");

}

void homingSequence() {};

void loop() {
  ReadSerial();

}

void ReadSerial() {
  if (Serial.available() > 0) {
      // Read the incoming byte
      char incomingByte = Serial.read();

      // Check if the received byte is a digit or a '-' sign
      if (isdigit(incomingByte) || incomingByte == '-') {
          // Convert the received byte to an integer and append to the current number
          numbers[index] = numbers[index] * 10 + (incomingByte - '0');
      }
      else if (incomingByte == ',') {
          // Move to the next index in the array
          index++;

          // Check if we have reached the end of the array
          if (index >= 2) {
              // Reset the index for the next input
              index = 0;

              // Optionally, process or use the received numbers here
              // Example: Print the received numbers
              Serial.print("Received numbers: ");
              Serial.print(numbers[0]);
              Serial.print(", ");
              Serial.println(numbers[1]);

              // Clear the array for the next input
              memset(numbers, 0, sizeof(numbers));
          }
      }
  }
}