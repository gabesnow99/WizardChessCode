#define BUTTON_THRESHOLD 2.5

// Analog pins
#define outer_pot_pin A4 //VRy on board
#define inner_pot_pin A5 //VRx on board
#define button_pin A3    //SW  on board

// Variables
int outer_pot_val = 0;
int inner_pot_val = 0;
int button_val = 0;

// Functions
bool isButtonPushed();

void setup() {
  Serial.begin(9600);
  pinMode(outer_pot_pin, INPUT);
  pinMode(inner_pot_pin, INPUT);
  pinMode(button_pin, INPUT_PULLUP);
}

void loop() {
  outer_pot_val = analogRead(outer_pot_pin);
  inner_pot_val = analogRead(inner_pot_pin);
  button_val = analogRead(button_pin);

  Serial.print("button_val: ");
  Serial.print(button_val);
  Serial.print(" outer_pot_val: ");
  Serial.print(outer_pot_val);
  Serial.print(" inner_pot_val: ");
  Serial.println(inner_pot_val);
}

// Function Definitions
bool isButtonPushed(){
  if (analogRead(button_val) >= BUTTON_THRESHOLD){
    return true;
  } else {
    return false;
  }
}
