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
  float t = millis() / 1000.0; // secondi dall'avvio del programma
  int photocellValue = analogRead(photocellPin); // lettura della fotoresistenza
  float V = photocellValue * 5.0 / 1023.0; // conversione in tensione
  float intensity = V / (5.0 - V); // conversione in intensità adimensionale
  float intensity_err = 0.024 / ((5.0 - V) * (5.0 - V)); // incertezza
  digitalWrite(triggerPin, LOW);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  float dt = pulseIn(echoPin, HIGH); // lettura del tempo di andata e ritorno
  float distance = speedOfSound * dt / 2; // calcolo della distanza
  float distance_err = 0.3; // incertezza
   // controlla che il valore sia nel range di sensibilità, quindi stampa le misure
  if (distance > 2 && distance < 400) {
    Serial.print(t);
    Serial.print(" ");
    Serial.print(distance, 1);
    Serial.print(" ");
    Serial.print(distance_err, 1);
    Serial.print(" ");
    Serial.print(intensity, 4);
    Serial.print(" ");
    Serial.println(intensity_err, 4);
  }
  delay(300);
}
