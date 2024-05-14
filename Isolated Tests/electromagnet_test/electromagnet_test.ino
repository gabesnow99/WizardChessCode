void setup() {
  pinMode(3, OUTPUT);
  pinMode(13, OUTPUT);

}

void loop() {
  digitalWrite(3, HIGH);
  digitalWrite(13, HIGH);
  delay(125);
  digitalWrite(13, LOW);
  digitalWrite(3, LOW);
  delay(125);
}
