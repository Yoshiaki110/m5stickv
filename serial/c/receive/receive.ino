HardwareSerial serial_ext(2);

void setup() {
  Serial.begin(115200);
  serial_ext.begin(115200, SERIAL_8N1, 32, 33);
  Serial.println("start");
}
/*
void loop() {
  //Serial.println("loop");
  uint8_t rx_buffer[10];
  if (serial_ext.available()>0) {
    int rx_size = serial_ext.readBytes(rx_buffer, 1);
    char buff[64];
    sprintf(buff, "%d - %x", rx_size, rx_buffer[0]);
    Serial.println(buff);
  }
  //delay(1000);
}
*/
void loop() {
  int rx_size = 0;
  uint8_t rx_buffer[10];
  if (serial_ext.available()>0) {
    rx_size = serial_ext.readBytes(rx_buffer, 1);
    if (rx_buffer[0] == 0xFF) {
      if (serial_ext.available()>0) {
        rx_size = serial_ext.readBytes(rx_buffer, 1);
        if (rx_buffer[0] == 0xAA) {
          if (serial_ext.available()>0) {
            rx_size = serial_ext.readBytes(rx_buffer, 1);
            char buff[64];
            sprintf(buff, "%d - %x", rx_size, rx_buffer[0]);
            Serial.println(buff);
          }
        }
      }
    }
  }
  //delay(1000);
}
