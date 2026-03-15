#include <Servo.h>

Servo indexServo;
Servo middleServo;

void setup() {
  Serial.begin(9600);
  indexServo.attach(3);     // Index servo pin
  middleServo.attach(4);   // Middle servo pin
  Serial.println("Index & Middle Servos Ready!");
}

void loop() {
  if (Serial.available()) {
    // Read Index angle
    int indexAngle = Serial.parseInt();  

    // Consume the comma separator
    if (Serial.peek() == ',') Serial.read(); 

    // Read Middle angle
    int middleAngle = Serial.parseInt();  

    // Consume any leftover newline
    if (Serial.peek() == '\n') Serial.read(); 

    // Move Index servo if in range
    if (indexAngle >= 130 && indexAngle <= 150) {
      indexServo.write(indexAngle);
      Serial.print("Moved Index Servo to: ");
      Serial.println(indexAngle);
    } else {
      Serial.print("Error: Index angle out of range (130-150) - received ");
      Serial.println(indexAngle);
    }

    //Move Middle servo if in range
    if (middleAngle <= 50 && middleAngle >= 30) {
      middleServo.write(middleAngle);
      Serial.print("Moved Middle Servo to: ");
      Serial.println(middleAngle);
    } else {
      Serial.print("Error: Middle angle out of range (30-50) - received ");
      Serial.println(middleAngle);
    }
  }
}