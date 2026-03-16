#define IN1 8
#define IN2 9
#define ENA 5   

char currentCommand = 'K';   // default Stop

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  Serial.begin(9600);
}

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 100);  
  delay(1000);
  stopMotor();  
  currentCommand = 'K';
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 100);
  delay(1000);
  stopMotor();   
  currentCommand = 'K';
}

void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);   
}

void loop() {

  if (Serial.available() > 0) {
    currentCommand = Serial.read();
    Serial.println(currentCommand);
  }

  if (currentCommand == 'W') {
    forward();
  }
  else if (currentCommand == 'S') {
    backward();
  }
  else {
    stopMotor();
  }
}