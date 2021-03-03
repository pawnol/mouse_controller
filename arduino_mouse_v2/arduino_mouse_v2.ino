
const int BUTTON_PIN = 2;

bool startWrite = false;

void setup() {
  pinMode(BUTTON_PIN, INPUT);
  Serial.begin(9600);
}

void loop() {
  byte startByte = Serial.read();
  if (startByte == 83) {
    startWrite = true;
    Serial.println("S");
  }
  if (startWrite) {
    int buttonState = digitalRead(BUTTON_PIN);
    int x = analogRead(A0);
    int y = analogRead(A1);
    Serial.println((String) x + "," + (String) y + "," + (String) buttonState);
  }
}
