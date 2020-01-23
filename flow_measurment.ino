#define VOLUME (0.0015*0.0015*PI*0.02)

int sensor1Pin = A0; 
int sensor1Value = 0;
int sensor2Pin = A1; 
int sensor2Value = 0;
bool detectedState = 0;
unsigned long sensor1Detect = 0; // the time sensor 1 detects flow
unsigned long sensor2Detect = 0; // the time sensor 2 detects flow
float flowVelocity = 0;
float totalVolume = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  detectedState = 0;
  sensor1Detect = 0;
  sensor2Detect = 0;
  flowVelocity = 0;
  totalVolume = 0;
}

void loop() {

  sensor1Value = analogRead(sensor1Pin);
  Serial.println(sensor1Value);
  sensor2Value = analogRead(sensor2Pin);
  Serial.println(sensor2Value);

  if(sensor1Value <700 && !detectedState) {
    detectedState = true;
    sensor1Detect = millis();
  }

  if(sensor2Value <700 && detectedState) {
    
    sensor2Detect = millis();
    flowVelocity = VOLUME/((sensor2Detect-sensor1Detect)/1000);
    
  }

  if(sensor1Value >750 && detectedState) {
    detectedState = false;
    totalFlowTime = millis() - sensor1Detect;
    totalVolume += flowVelocity*(totalFlowTime/1000);
  }
  
  delay(100);
}
