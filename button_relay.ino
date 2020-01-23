// power relay pin is controlled with D8. The active wire is connected to Normally open and common
int powerOnPin = 8;
int vacIncPin = 9;
int vacDecPin = 10;
int speedIncPin = 11;
int speedDecPin = 12;
int letDown = 13;

// vacuum state from 1-12
volatile byte vacState = 5;

// pump power status
volatile byte pumpStatus = 0;

void setup() {
  // Pin for device power 
  pinMode(powerOnPin, OUTPUT);
  // HIGH -> off   Low-> on
  digitalWrite(powerOnPin, HIGH);
  
  // Pin for increasing vacuum power
  pinMode(vacIncPin, OUTPUT);
  digitalWrite(vacIncPin, HIGH);
  
  // Pin for decreasing vacuum power
  pinMode(vacDecPin, OUTPUT);
  digitalWrite(vacDecPin, HIGH);

  // Pin for increasing speed power
  pinMode(speedIncPin, OUTPUT);
  digitalWrite(speedIncPin, HIGH);

  // Pin for decreasing speed power
  pinMode(speedDecPin, OUTPUT);
  digitalWrite(speedDecPin, HIGH);

  // Pin for triggering letdown
  pinMode(letDown, OUTPUT);
  digitalWrite(letDown, HIGH);
  
  // Serial communication for debugging purposes
  Serial.begin(9600);
}

void loop() {
  pumpPower();
  delay(5000);
  
  increaseVac();
  delay(3000);
  increaseVac();
  delay(3000);
  increaseVac();
  delay(3000);
 
  decreaseVac();
  delay(3000);
  decreaseVac();
  delay(3000);
  decreaseVac();
  delay(3000);
  
  pumpPower();
  delay(10000);
}

void buttonPress(int buttonPin) {
  digitalWrite(buttonPin, LOW);
  delay(100);
  digitalWrite(buttonPin, HIGH);
}

void pumpPower() {
  Serial.println("Turn pump on/off");
  if(pumpStatus)
    pumpStatus = 0;
  else
    pumpStatus = 1;

  buttonPress(powerOnPin);
}

void increaseVac() {
  Serial.println("vacuum increased to ");
  Serial.println(vacState);
  if(vacState < 12)
  {
    buttonPress(vacIncPin);
    vacState++;
  }
}

void decreaseVac() {
  Serial.println("vacuum decreased to ");
  Serial.println(vacState);
  if(vacState > 1)
  {
    buttonPress(vacDecPin);
    vacState--;
  }
}
