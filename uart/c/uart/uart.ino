#include <M5StickC.h>

void setup() {
  Serial.begin(115200);
  //Serial2.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 32, 33);

  Serial.println("ESP32 : Hello World");
}
/*
void loop() {
  // read from port 1, send to port 0:
  if (Serial2.available()) {
    int inByte = Serial2.read();
    Serial.write(inByte);
    Serial2.write(inByte);
  }
//  delay(1000);
}
*/
void loop() {
  Serial2.write("hello");
  delay(1000);
}
