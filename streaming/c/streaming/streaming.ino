#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <M5StickC.h>
#include "setting.h"

const char* ssid = SSID;
const char* password = PASS;
 
WebServer server(80);
uint8_t *buff;
static const int RX_BUF_SIZE = 100000;

void sendPic() {
  WiFiClient client = server.client();
  Serial.println("sendPic start");

  Serial2.write("get");
  delay(100);

  uint8_t buf[3];
  int len = Serial2.readBytes(buf, 3);
  if (len != 3) {
    Serial.println("sendPic get length error");
    return;
  }
  int pLen = (uint32_t)(buf[0] << 16) | (buf[1] << 8) | buf[2];
  Serial.print("sendPic picture length : ");
  Serial.println(pLen);

  len = Serial2.readBytes(buff, pLen);
  if (len != pLen) {
    Serial.print("sendPic get picture error ");
    Serial.print(len);
    Serial.print("-");
    Serial.println(pLen);
    return;
  }

  len = Serial2.readBytes(buf, 3);
  if (len != 3) {
    Serial.println("sendPic get footer error");
    return;
  }
  client.write(buff, pLen); 
  Serial.println("sendPic end");
}
 
 
void setup() {
  pinMode(10, OUTPUT);
  
  M5.begin();
  M5.Axp.ScreenBreath(0);
  
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 32, 33);
 
  buff = (uint8_t *) malloc(sizeof(uint8_t) * RX_BUF_SIZE);
 
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
//  server.on("/stream", HTTP_GET, streamPic);
 
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop() {
  server.handleClient();
}
