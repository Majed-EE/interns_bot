#include <Servo.h>

Servo indexServo;

void setup() {
  Serial.begin(9600);
  indexServo.attach(3);   // Index servo pin
  Serial.println("Index Servo Ready!");
}

void loop() {
  if (Serial.available()) {

    int indexAngle = Serial.parseInt();  // Read angle

    // Remove leftover newline
    if (Serial.peek() == '\n') Serial.read();

    // Check range (130-150)
    if (indexAngle >= 130 && indexAngle <= 150) {
      indexServo.write(indexAngle);
      Serial.print("Moved Index Servo to: ");
      Serial.println(indexAngle);
    } else {
      Serial.print("Error: Angle out of range (130-150) - received ");
      Serial.println(indexAngle);
    }
  }
}