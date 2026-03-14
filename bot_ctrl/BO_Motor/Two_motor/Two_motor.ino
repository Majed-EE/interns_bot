#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11
#define ENA 5  
#define ENB 6

char currentCommand = 'K';   // default Stop

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  Serial.begin(9600);
}

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 100);
  analogWrite(ENB, 100);
  delay(1000);
  stopMotor();
  currentCommand = 'K';
  
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 100);
  analogWrite(ENB, 100);
  delay(1000);
  stopMotor();
  currentCommand = 'K';
}

void left() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH );
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 100);
  analogWrite(ENB, 100);
  delay(1000);
  stopMotor();
  currentCommand = 'K';

}

void right() {
  digitalWrite(IN1, HIGH); //left wheel 
  digitalWrite(IN2, LOW);  
  digitalWrite(IN3, LOW); 
  digitalWrite(IN4, HIGH); 
  analogWrite(ENA, 100);
  analogWrite(ENB, 100);
  delay(1000);
  stopMotor();
  currentCommand = 'K';
}

void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA,0);
  analogWrite(ENB,0);
}

void loop() {


  if (Serial.available() > 0) {
    currentCommand = Serial.read();
    Serial.println(currentCommand);    // store command
  }

  // Execute continuously
  if (currentCommand == 'W') {
    forward();
    
  }
  else if (currentCommand == 'S') {
    backward();
  }
  else if (currentCommand == 'A') {
    left();
  }
  else if (currentCommand == 'D') {
    right();
  }
  else {
    stopMotor();
  }
}