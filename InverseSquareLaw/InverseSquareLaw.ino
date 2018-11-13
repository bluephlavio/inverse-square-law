int photocellPin = A0;
int triggerPin = 2;
int echoPin = 3;

float speedOfSound = 0.034; // cm / microseconds

void setup() {
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  float t = millis() / 1000.0;
  int photocellValue = analogRead(photocellPin);
  float V = photocellValue * 5.0 / 1023;
  float intensity = V / (5.0 - V);
  digitalWrite(triggerPin, LOW);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  float dt = pulseIn(echoPin, HIGH);
  float distance = speedOfSound * dt / 2;
  if (distance > 3 && distance < 100) {
    Serial.print(t);
    Serial.print(" ");
    Serial.print(distance);
    Serial.print(" ");
    Serial.println(intensity);
  }
  delay(300);
}
