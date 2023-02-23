#include <WiFi.h> // Library used for wifi connection
#include <ArduinoWebsockets.h> // Library used for web socket connection (https://github.com/gilmaimon/ArduinoWebsockets)
#include <ArduinoJson.h> // Library used for JSON parsing 

#include <Arduino.h> 
#include <IRremoteESP8266.h> // Library used for IR transmission
#include <IRsend.h> // Library used for IR transmission

// WiFi credentials
char* WIFI_SSID = "SSID";
char* WIFI_PASSWORD = "PASSWORD";
// Websocked server address
const char* SERVER_ADDRESS = "wss://accontroller.tbrouwer.com:443/ws";

// IR LED pin
const uint16_t kIrLed = 2;
IRsend irsend(kIrLed);

// LED pins
const int Red_LED_pin=32;
const int Green_LED_pin=33;

// Example IR codes for Mitsubishi AC
uint8_t mitsubishiState_on[19]={0xAD, 0x51, 0x3C, 0xE5, 0x1A, 0x0C, 0xF3, 0x05, 0xFA, 0x00, 0xFF, 0xC0, 0x3F, 0xC8, 0x37, 0x00, 0xFF, 0x80, 0x7F};
uint8_t mitsubishiState_off[19]={0xAD, 0x51, 0x3C, 0xE5, 0x1A, 0x04, 0xFB, 0x05, 0xFA, 0x00, 0xFF, 0xC0, 0x3F, 0xC8, 0x37, 0x00, 0xFF, 0x80, 0x7F};

// Web socket client
using namespace websockets;
WebsocketsClient client;

// Settings JSON object
DynamicJsonDocument settingsJson(1024);

void onMessageCallback(WebsocketsMessage request) {
  Serial.println(request.data());

  // Check if server is working
  if (request.data() == "Server is working!") {
    // Send device ID to server
    client.send(settingsJson["deviceID"].as<const char*>());

    // Return early
    return;
  }

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
        settingsJson[pair.key()] = pair.value();
      }
  }

  return;
}

void onEventsCallback(WebsocketsEvent event, String data) {
    if(event == WebsocketsEvent::ConnectionOpened) {
        Serial.println("Connnection Opened");
    } else if(event == WebsocketsEvent::ConnectionClosed) {
        Serial.println(client.getCloseReason());
        Serial.println("Connnection Closed");
    } else if(event == WebsocketsEvent::GotPing) {
        Serial.println("Got a Ping!");
    } else if(event == WebsocketsEvent::GotPong) {
        Serial.println("Got a Pong!");
    }
}

void turn_ac_on(){
  irsend.sendMitsubishiHeavy152(mitsubishiState_on);
  delay(500);
  digitalWrite(Green_LED_pin, HIGH);
  delay(1500);
  digitalWrite(Green_LED_pin, LOW);
}

void turn_ac_off(){
  irsend.sendMitsubishiHeavy152(mitsubishiState_off);
  delay(500);
  digitalWrite(Red_LED_pin, HIGH);
  delay(1500);
  digitalWrite(Red_LED_pin, LOW);
}

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

  // run callback when messages are received
  client.onMessage(onMessageCallback);
  
  // run callback when events are occurring
  client.onEvent(onEventsCallback);

  // Connect to server
  client.connect(SERVER_ADDRESS);

  // // Receive server conformation
  // auto conf = client.readBlocking();

  // // Send a message
  // client.send(settingsJson["deviceID"].as<const char*>());
}

void loop() {
  // Check for new messages
  client.poll();

  // // Receive data from server
  // auto request = client.readBlocking();
  // Serial.println(request.data());
  // Serial.println(request.c_str());

  // // Parse request data
  // DynamicJsonDocument requestJson(1024);
  // deserializeJson(requestJson, request.data());
  
  // if (requestJson['op'] == "get-settings") {
  //   // Serialize current settings to string
  //   String settingsString;
  //   serializeJson(settingsJson, settingsString);

  //   // Send settings to server
  //   client.send(settingsString);
  // } else if (requestJson['op'] == "update-settings") {
  //     // Update settings
  //     JsonVariant settingsToUpdate = requestJson['settings'];

  //     // Iterate through settings to update
  //     for (JsonPair pair : settingsToUpdate.as<JsonObject>()) {
  //       settingsJson[pair.key().c_str()] = pair.value();
  //     }
  // }

  // delay(100);
}
