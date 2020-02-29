#include <M5StickC.h>
#include <WiFi.h>
#include <ssl_client.h>
#include <WiFiClientSecure.h>
#include "setting.h"

const char* ssid = SSID;
const char* passwd = PASS;

HardwareSerial serial_ext(2);

typedef struct {
  uint32_t length;
  uint8_t *buf;
} jpeg_data_t;

jpeg_data_t jpeg_data;
static const int RX_BUF_SIZE = 20000;
static const uint8_t packet_begin[3] = { 0xFF, 0xD8, 0xEA };

/*
sendLineNotify関数は、以下参照。
https://github.com/anoken/purin_wo_mimamoru_gijutsu/blob/master/2_6_M5Camera_Send_LineNotify/2_6_M5Camera_Send_LineNotify.ino
*/
void sendLineNotify(uint8_t* image_data, size_t image_sz);

void setup() {
  M5.begin();
  M5.Lcd.setRotation(3);
  M5.Lcd.setCursor(0, 30, 4);
  M5.Lcd.println("m5stick_uart_wifi_converter");

  setup_wifi();

  jpeg_data.buf = (uint8_t *) malloc(sizeof(uint8_t) * RX_BUF_SIZE);
  jpeg_data.length = 0;
  if (jpeg_data.buf == NULL) {
    Serial.println("malloc jpeg buffer 1 error");
  }

  serial_ext.begin(115200, SERIAL_8N1, 32, 33);
}

void loop() {
  M5.update();

  if (serial_ext.available()) {
    uint8_t rx_buffer[10];
    int rx_size = serial_ext.readBytes(rx_buffer, 10);
    if (rx_size == 10) {   //packet receive of packet_begin
      if ((rx_buffer[0] == packet_begin[0]) && (rx_buffer[1] == packet_begin[1]) && (rx_buffer[2] == packet_begin[2])) {
        //image size receive of packet_begin
        jpeg_data.length = (uint32_t)(rx_buffer[4] << 16) | (rx_buffer[5] << 8) | rx_buffer[6];
        int rx_size = serial_ext.readBytes(jpeg_data.buf, jpeg_data.length);
        Serial.print("Receive ");
        Serial.print(rx_size);
        Serial.println("byte");
        for (int i = 0; i < rx_size; i++) {
          Serial.print(jpeg_data.buf[i], HEX);
          Serial.print(" ");
          if (i % 16 == 15) {
            Serial.println("");
          }
        }

        //image processing, for example, line notify send image
        //sendLineNotify(jpeg_data.buf, jpeg_data.length);
        //image processing end
      }
    }
  }
  vTaskDelay(10 / portTICK_RATE_MS);
}

void setup_wifi() {
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, passwd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
