#if 0
#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <M5StickC.h>
#include "setting.h"

const char* ssid = SSID;
const char* password = PASS;
 
WebServer server(80);
 
typedef struct {
  uint32_t length;
  uint8_t *buf;
} jpeg_data_t;
 
jpeg_data_t jpeg_data;
static const int RX_BUF_SIZE = 100000;
 
static const uint8_t packet_begin[7] = { 0xFF, 0xD8, 0xEA, 0x01, 0x00, 0x00, 0x00 };

uint32_t readHeader() {
  uint32_t ret = 0;
  uint8_t rx_buffer;
  Serial.println("readHeader start");

  for ( int i = 0; i < 7; i++) {
    if (Serial2.available()) {
      int rx_size = Serial2.readBytes(&rx_buffer, 1);    
      if (rx_size != 1) {
        Serial.print("readHeader cannot read ");
        Serial.println(i);
        return 0;
      }
      if (rx_buffer != packet_begin[i]) {
        Serial.print("readHeader not header ");
        Serial.print(i);
        Serial.print(" ");
        Serial.print(rx_buffer);
        Serial.print("-");
        Serial.print(packet_begin[i]);
        Serial.println("");
        return 0;
      }
    } else {
      Serial.print("readHeader not available ");
      Serial.println(i);
      return 0;
    }
  }
  if (Serial2.available()) {
    int rx_size = Serial2.readBytes(&rx_buffer, 1);    
    if (rx_size != 1) {
      Serial.print("readHeader cannot read size(1)");
      return 0;
    }
    Serial.println(rx_buffer);
    ret = (uint32_t)(rx_buffer << 16);
  } else {
    Serial.println("readHeader not available size(1)");
    return 0;
  }
  if (Serial2.available()) {
    int rx_size = Serial2.readBytes(&rx_buffer, 1);    
    if (rx_size != 1) {
      Serial.print("readHeader cannot read size(2)");
      return 0;
    }
    Serial.println(rx_buffer);
    ret += (uint32_t)(rx_buffer << 8);
  } else {
    Serial.println("readHeader not available size(2)");
    return 0;
  }
  if (Serial2.available()) {
    int rx_size = Serial2.readBytes(&rx_buffer, 1);    
    if (rx_size != 1) {
      Serial.print("readHeader cannot read size(3)");
      return 0;
    }
    Serial.println(rx_buffer);
    ret += (uint32_t)(rx_buffer);
  } else {
    Serial.println("readHeader not available size(3)");
    return 0;
  }
  return ret;
}

void prn1(int i, int rx_size) {
  Serial.print(i+1);
  Serial.print(" / ");
  Serial.print(rx_size);
  Serial.print(" ");
  Serial.print(jpeg_data.length);
  Serial.print(" ");
  Serial.print(jpeg_data.buf[i], HEX);
  Serial.println("");
}

void sendPic() {
  int state = 1;
  WiFiClient client = server.client();
  Serial.println("sendPic start");

  while(state){
    if (Serial2.available()) {
      digitalWrite(10, LOW);
      uint32_t len = readHeader();
      if (len != 0) {
        jpeg_data.length = len;
        Serial.print(jpeg_data.length);
        Serial.println("-");

        int rx_size = 0;
        uint32_t l = jpeg_data.length;
        uint8_t *p = jpeg_data.buf;
        int i = 0;
        for (;;) {
          int rs = l > 100 ? 100 : l;
          int r = Serial2.readBytes(p, rs);
          for (int j = 0; j < r; j++) {
            prn1(i, rx_size);
            ++i;
          }
          rx_size += r;
          p += r;
          l -= r;
          if (r == l) {
            break;
          }
        }
        Serial.println(rx_size);
//        client.write(jpeg_data.buf, jpeg_data.length + 1600); 
        state = 0;
        Serial.print("Receive ");
        Serial.print(rx_size);
        Serial.println("byte");
        /*for (int i = 0; i < rx_size; i++) {
          Serial.print(i+1);
          Serial.print(" / ");
          Serial.print(rx_size);
          Serial.print(" ");
          Serial.print(jpeg_data.length);
          Serial.print(" ");
          Serial.print(jpeg_data.buf[i], HEX);
          Serial.println(" ");
        }*/
        client.write(jpeg_data.buf, rx_size); 
      }
    } else {
      Serial.println("sendPic delay read packet");
    }
    if (!client.connected())
      break;
  }
  Serial.println("sendPic end");
}
 
void streamPic() {
  int state = 1;
  Serial.println("streamPic start");
  while(state){
    if (Serial2.available()) {
      digitalWrite(10, LOW);
      uint8_t rx_buffer[10];
      int rx_size = Serial2.readBytes(rx_buffer, 10);    
      if (rx_size == 10) {
        if ((rx_buffer[0] == packet_begin[0]) && (rx_buffer[1] == packet_begin[1]) && (rx_buffer[2] == packet_begin[2])) {
          jpeg_data.length = (uint32_t)(rx_buffer[4] << 16) | (rx_buffer[5] << 8) | rx_buffer[6];
          Serial.println(jpeg_data.length);
  
          int rx_size = Serial2.readBytes(jpeg_data.buf, jpeg_data.length);
          state = 0;
        } else {
          Serial.println("streamPic illegal packet");
        }
      } else {
        Serial.println("streamPic cannot read packet");
      }
    } else {
      Serial.println("streamPic delay read packet");
    }
  }
  
  WiFiClient client = server.client();
  Serial.println("streamPic 5");
  String response = "HTTP/1.1 200 OK\r\n";
  response += "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n";
  server.sendContent(response);
 
  while (1)  {
    digitalWrite(10, HIGH);
          
    if (Serial2.available()) {
      digitalWrite(10, LOW);
      uint8_t rx_buffer[10];
      int rx_size = Serial2.readBytes(rx_buffer, 10);
      if (rx_size == 10) {
        if ((rx_buffer[0] == packet_begin[0]) && (rx_buffer[1] == packet_begin[1]) && (rx_buffer[2] == packet_begin[2])) {
          jpeg_data.length = (uint32_t)(rx_buffer[4] << 16) | (rx_buffer[5] << 8) | rx_buffer[6];
          Serial.println(jpeg_data.length);
  
          int rx_size = Serial2.readBytes(jpeg_data.buf, jpeg_data.length);
        }
        response = "--frame\r\n";
        response += "Content-Type: image/jpeg\r\n\r\n";
        server.sendContent(response);
 
        client.write(jpeg_data.buf, jpeg_data.length);
        server.sendContent("\r\n");
        
        if (!client.connected())
          break;
        Serial.println("streamPic 7");
      }else{
        int rx_size = Serial2.readBytes(rx_buffer, 1);
        break;
      }
    }
 
    if (!client.connected())
      break;
    Serial.println("streamPic 8");
  }
  Serial.println("streamPic end");
}
 
void setup() {
  pinMode(10, OUTPUT);
  
  M5.begin();
  M5.Axp.ScreenBreath(0);
  
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 32, 33);
 
  jpeg_data.buf = (uint8_t *) malloc(sizeof(uint8_t) * RX_BUF_SIZE);
 
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
 
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("  http://");
  Serial.print(WiFi.localIP());
  Serial.println("/pic");
  Serial.print("  http://");
  Serial.print(WiFi.localIP());
  Serial.println("/stream");
 
  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }
 
  server.on("/", []() {
    server.send(200, "text/plain", "this works as well");
  });
 
  server.on("/pic", HTTP_GET, sendPic);
  server.on("/stream", HTTP_GET, streamPic);
 
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop() {
  server.handleClient();
}
#endif
