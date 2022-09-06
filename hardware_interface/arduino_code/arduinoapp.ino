#include <Stepper.h>

#define STEPS 200
int stepstomove;
const int turn = 148;
const float val1 = 0.1;
const float val2 = 0.1;
const float val3 = 1-val1*2-val2*2;
int input;
Stepper stepper(STEPS, 8, 9, 10, 11);

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0)
  {
    input = Serial.read();
    Serial.println(input);
    if (input == 49)
    {
      stepstomove = int(turn);
      stepper.setSpeed(30);
      stepper.step(stepstomove*val1);
      stepper.setSpeed(45);
      stepper.step(stepstomove*val2);
      stepper.setSpeed(60);
      stepper.step(stepstomove*val3);
      stepper.setSpeed(50);
      stepper.step(stepstomove*val2);
      stepper.setSpeed(40);
      stepper.step(stepstomove*val1);
      
    }
    if (input == 50)
    {
      stepstomove = int(turn);
      stepper.setSpeed(50);
      stepper.step(-stepstomove*val1);
      stepper.setSpeed(55);
      stepper.step(-stepstomove*val2);
      stepper.setSpeed(60);
      stepper.step(-stepstomove*val3);
      stepper.setSpeed(50);
      stepper.step(-stepstomove*val2);
      stepper.setSpeed(40);
      stepper.step(-stepstomove*val1);
      Serial.print(0);
      
    }
    else if (input == 48)
    {
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
    }
  }
  input = 0;
}