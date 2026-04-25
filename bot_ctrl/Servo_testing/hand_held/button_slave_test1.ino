const int buttonPin = 2;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int state = digitalRead(buttonPin);

  if (state == LOW) {
    Serial.println("PRESSED");
  } else {
    Serial.println("RELEASED");
  }

  delay(50); // debounce
}