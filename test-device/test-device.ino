// Library used for wifi connection
#include <WiFi.h>
// Library used for web socket connection (https://github.com/morrissinger/ESP8266-Websocket)
#include "WebSocketClient.h"
// Library used for JSON parsing
#include <ArduinoJson.h>

// Include constants
#include "./constants.h"

// WiFi credentials
const char* ssid = "SSID";
const char* password = "PASSWORD";

// Web socket client
WebSocketClient webSocketClient;
// WiFi client
WiFiClient client;

JsonObject& settings = jsonBuffer.parseObject("{\"deviceID\":\"DEVICE IDENTIFIER\",\"setting1\":\"value1\",\"setting2\":\"value2\"}");

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi network
  WiFi.begin(ssid, password);
 
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 
  delay(5000);
 
  if (client.connect('ws://' + SERVER_ADDRESS + '/ws', 443)) {
    Serial.println("Connected");
  } else {
    Serial.println("Connection failed.");
  }
 
  // perform handshake with server
  // webSocketClient.path = '';
  webSocketClient.host = 'ws://' + SERVER_ADDRESS + '/ws';
  if (webSocketClient.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
  }

  if (client.connected()) {
    // Receive server conformation
    String data;
    webSocketClient.getData(data);
    Serial.println(data);

    // Send device identifier to server
    webSocketClient.sendData(settings['deviceID']);
  }
}
 
void loop() { 
  if (client.connected()) {
    // Receive data from server
    String data = webSocketClient.getData(data);
    Serial.println(data);
    JsonObject& dataJson = jsonBuffer.parseObject(data);

    // If get settings request is received send settings to server  
    if (dataJson['op'] == "get-settings") {
        String settingsString;
        settings.printTo(settingsString);
        webSocketClient.sendData(settingsString);
    }
  } else {
    Serial.println("Client disconnected.");
  }
 
  delay(500);
}
