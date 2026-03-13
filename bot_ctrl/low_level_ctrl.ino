#include <Servo.h>

Servo indexServo;
Servo middleServo;

// Motor Pins
int IN1 = 8;
int IN2 = 9;
int IN3 = 10;
int IN4 = 11;
int ENA = 5;
int ENB = 6;

void setup() {
  Serial.begin(9600);
  indexServo.attach(3);
  middleServo.attach(4);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  analogWrite(ENA, 100);
  analogWrite(ENB, 100);
  indexServo.write(150);
  middleServo.write(30);
  Serial.println("Send: indexAngle,middleAngle,Direction");
}

// function description
void forward(){
  digitalWrite(IN1,HIGH); digitalWrite(IN2,LOW);
  digitalWrite(IN3,HIGH); digitalWrite(IN4,LOW);
}

void backward(){
      digitalWrite(IN1,LOW); digitalWrite(IN2,HIGH);
      digitalWrite(IN3,LOW); digitalWrite(IN4,HIGH);

}

void left(){
  digitalWrite(IN1,LOW); digitalWrite(IN2,HIGH);
  digitalWrite(IN3,HIGH); digitalWrite(IN4,LOW);
}

void right(){
  digitalWrite(IN1,HIGH); digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW); digitalWrite(IN4,HIGH);
}

void stop(){
  digitalWrite(IN1,LOW); digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW); digitalWrite(IN4,LOW);
}


void loop(){
  if (Serial.available()) {

    String input = Serial.readStringUntil('\n');   // read full line
    int firstComma,secondComma, middleAngle, indexAngle;
    char direction;
    firstComma = input.indexOf(',');
    String topic=input.substring(0,firstComma); // topic name

    if (topic =="arm"){
    secondComma = input.indexOf(",",firstComma + 1);
    indexAngle = input.substring(firstComma + 1, secondComma).toInt();
    middleAngle = input.substring(secondComma+1).toInt();
    Serial.print(" Index: "); Serial.print(indexAngle);
    Serial.print("  Middle: "); Serial.println(middleAngle);    
    // 150 open
    if (indexAngle >= 130 && indexAngle <= 150){  
      Serial.print("sending Index: "); Serial.println(indexAngle);
      indexServo.write(indexAngle);}
    // 30 open
    if (middleAngle >= 30 && middleAngle <= 50){
      Serial.print("sending  Middle: "); Serial.println(middleAngle);
      middleServo.write(middleAngle);}


    }

    else if (topic=="wheel"){
      direction = input.substring(",",firstComma+1).charAt(0);
      Serial.print("  Direction: "); Serial.println(direction);
        if (direction == 'W') {
    Serial.println("sending W");
    forward();
    delay(1000);
    stop();
  }
  else if (direction == 'S') {
    Serial.println("sending S");
    backward();
    delay(1000);
    stop();
  }
  else if (direction == 'A') {
    Serial.println("sending A");
    left();
    delay(1000);
    stop();
  }
  else if (direction == 'D') {
    Serial.println("sending D");
    right();
    delay(1000);
    stop();
  }
  else if (direction=="K") {
    Serial.println(direction);
    Serial.println(" sending Stop");
    stop();
  }
      
    }

    else{ 
      Serial.println("invalid format");
      }
    //130(index),50(middle) -> close
    // 150,30
    

    // Wheels
    // Execute continuously


  }