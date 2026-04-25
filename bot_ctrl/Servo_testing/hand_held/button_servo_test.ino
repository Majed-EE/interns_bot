#include <Servo.h>
// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2;  // the number of the pushbutton pin
const int ledPin = 13;    // the number of the LED pin
const int indServoPin=9, thServoPin=10;

Servo index_servo, thumb_servo;  // create Servo object to control a servo
// twelve Servo objects can be created on most boards

int index_pos, index_pos_close= 110, index_pos_open = 160;
int thumb_pos, thumb_pos_close= 100,thumb_pos_open = 50; 
// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status
int lastButtonState =0;
int buttonPushCounter=0;

// int crnt_state =0; 
void setup() {
  // initialize the LED pin as an output:
  index_servo.attach(indServoPin); 
  // thumb_servo.attach(10);
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  index_servo.write(index_pos_open);
  Serial.begin(9600);
  thumb_pos=thumb_pos_open;


}

void loop() {
  // read the state of the pushbutton value:
   // Read the current button state
  buttonState = digitalRead(buttonPin);
  thumb_servo.detach();
  
  // Check if state has CHANGED
  if (buttonState != lastButtonState) {
    // If state changed from LOW to HIGH (button pressed)
    if (buttonState == HIGH) {
      buttonPushCounter++;      // Increment the counter
      
      Serial.println("****************before button press command**************************");
      Serial.print("Button presses: ");
      Serial.println(buttonPushCounter);
      Serial.print("Index Servo angle: ");
      Serial.println(index_pos);

      Serial.print("Thumb Servo angle: ");
      Serial.println(thumb_pos);
      
      index_pos--; //increment servo postion
      thumb_pos++;

      if (thumb_pos >=thumb_pos_close){
      
      thumb_pos=thumb_pos_open;
      thumb_servo.attach(thServoPin);
      thumb_servo.write(thumb_pos);
      }
      else{
        thumb_servo.attach(thServoPin);
        thumb_servo.write(thumb_pos);
      }

      
      if (index_pos<=index_pos_close){
        
        index_pos=index_pos_open;
        index_servo.write(index_pos);
  
      }
      else{ index_servo.write(index_pos);}
      // Optional: Blink LED to confirm
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      thumb_servo.detach();

      Serial.println("****************After button Press**************************");
      Serial.print("Index Servo angle: ");
      Serial.println(index_pos);

      Serial.print("Thumb Servo angle: ");
      Serial.println(thumb_pos);

      Serial.println("*****************************end**************************************");

    }
    delay(50);  // Small delay to handle button bounce
  }
  
  // Save current state for next comparison
  // lastButtonState = buttonState;
}