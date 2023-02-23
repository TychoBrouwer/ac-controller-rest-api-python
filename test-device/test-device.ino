// Library used for wifi connection
#include <WiFi.h>
// Library used for web socket connection (https://github.com/gilmaimon/ArduinoWebsockets)
#include <ArduinoWebsockets.h>
// Library used for JSON parsing
#include <ArduinoJson.h>

// Include constants
#include "./constants.h"

// Web socket client
using namespace websockets;
WebsocketsClient client;

// Settings JSON object
DynamicJsonDocument settingsJson(1024);

// WiFi credentials
char* WIFI_SSID = "SSID";
char* WIFI_PASSWORD = "PASSWORD";

const char* SERVER_ADDRESS = "wss://accontroller.tbrouwer.com:443/ws";

void setup() {
  Serial.begin(115200);

  // Default/current settings (safe in a file?)
  String settings = "{\"deviceID\":\"DEVICE IDENTIFIER\",\"setting1\":\"value1\",\"setting2\":\"value2\"}";
  // Parse settings into settings object
  deserializeJson(settingsJson, settings);
  
  // Connect to WiFi network
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
 
  delay(1000);

  // Connect to server
  client.connect(SERVER_ADDRESS);

  // Receive server conformation
  auto conf = client.readBlocking();

  // Send a message
  client.send(settingsJson["deviceID"].as<const char*>());
}

void loop() {
  // Receive data from server
  auto request = client.readBlocking();
  Serial.println(request.data());
  Serial.println(request.c_str());

  // Parse request data
  DynamicJsonDocument requestJson(1024);
  deserializeJson(requestJson, request.data());
  
  if (requestJson['op'] == "get-settings") {
    // Serialize current settings to string
    String settingsString;
    serializeJson(settingsJson, settingsString);

    // Send settings to server
    client.send(settingsString);
  } else if (requestJson['op'] == "update-settings") {
      // Update settings
      JsonVariant settingsToUpdate = requestJson['settings'];

      // Iterate through settings to update
      for (JsonPair pair : settingsToUpdate.as<JsonObject>()) {
        settingsJson[pair.key().c_str()] = pair.value();
      }
  }

  delay(100);
}
