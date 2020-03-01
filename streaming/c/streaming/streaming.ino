#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <M5StickC.h>
#include "setting.h"

const char* ssid = SSID;
const char* password = PASS;
String msg[4];
 
WebServer server(80);
uint8_t *buff;
static const int RX_BUF_SIZE = 100000;

void disp(String s1, String s2, String s3, String s4) {
  if (s1 != "") {
    msg[0] = s1;
  }
  if (s2 != "") {
    msg[1] = s2;
  }
  if (s3 != "") {
    msg[2] = s3;
  }
  if (s4 != "") {
    msg[3] = s4;
  }
  M5.Lcd.fillScreen(TFT_BLACK);
  M5.Lcd.setTextFont(2);      // 16ピクセル
  M5.Lcd.setCursor(0, 0);     // x(右), y(下)
  M5.Lcd.print(msg[0]);

  M5.Lcd.setTextFont(1);      // 8ピクセル
  M5.Lcd.setCursor(0, 20);
  M5.Lcd.print(msg[1]);
  
  M5.Lcd.setCursor(0, 40);
  M5.Lcd.print(msg[2]);
  
  M5.Lcd.setTextFont(2);      // 16ピクセル
  M5.Lcd.setCursor(0, 60);     // x(右), y(下)
  M5.Lcd.print(msg[3]);
}

bool transfer(WiFiClient client) {
  Serial.println("transfer start");

  Serial2.write("get");
  delay(50);

  uint8_t buf[3];
  int len = Serial2.readBytes(buf, 3);
  if (len != 3) {
    Serial.println("transfer get length error");
    return false;
  }
  int pLen = (uint32_t)(buf[0] << 16) | (buf[1] << 8) | buf[2];
  Serial.print("transfer picture length : ");
  Serial.println(pLen);
  int tLen = pLen;
  while (1) {
    len = Serial2.readBytes(buff, tLen);
    if (len == 0) {
      Serial.print("transfer get picture error ");
      Serial.print(len);
      Serial.print("-");
      Serial.println(tLen);
      return false;
    } else if (len != tLen) {
      Serial.print("transfer get picture retry ");
      Serial.print(len);
      Serial.print("-");
      Serial.println(tLen);
      tLen -= len;
    } else {
      break;
    }
    if (!client.connected()) {
      break;
    }
    delay(10);
  }

  len = Serial2.readBytes(buf, 3);
  if (len != 3) {
    Serial.println("transfer get footer error");
    return false;
  }
  client.write(buff, pLen); 
  //
  Serial.println("transfer end");
  return true;
}

void sendPic() {
  disp("", "", "", "/pic");
  WiFiClient client = server.client();
  Serial.println("sendPic start");

  transfer(client);

  Serial.println("sendPic end");
  disp("", "", "", "/pic end");
}

void streamPic() {
  disp("", "", "", "/stream");
  Serial.println("streamPic start");
  WiFiClient client = server.client();
  String response = "HTTP/1.1 200 OK\r\n";
  response += "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n";
  server.sendContent(response);

  while (1) {
    if (!client.connected()) {
      break;
    }
    response = "--frame\r\n";
    response += "Content-Type: image/jpeg\r\n\r\n";
    server.sendContent(response);

    if (!transfer(client)) {
      break;
    }
    
    server.sendContent("\r\n");
    if (!client.connected()) {
      break;
    }
  }
  Serial.println("streamPic end");
  disp("", "", "", "/stream end");
}

void setup() {
  M5.begin();
//  M5.Axp.ScreenBreath(0);   // スクリーンの輝度を制御
  M5.begin();
  M5.Lcd.setRotation(1);
    
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 32, 33);
 
  buff = (uint8_t *) malloc(sizeof(uint8_t) * RX_BUF_SIZE);
 
  disp(" AP : " +  String(ssid), "", "", "STATUS : Connecting...");
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
  disp("", " http://" + WiFi.localIP().toString() + "/pic", " http://" + WiFi.localIP().toString() + "/stream", "STATUS : Connected");
 
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
