#include <WiFi.h>             // Library used for wifi connection
#include <ArduinoJson.h>      // Library used for JSON parsing
#include <WebSocketsClient.h> // Library used for websocket: https://github.com/Links2004/arduinoWebSockets

// #include <Arduino.h>
// #include <IRremoteESP8266.h> // Library used for IR transmission
// #include <IRsend.h> // Library used for IR transmission

// WiFi credentials
char *WIFI_SSID = "FRITZ!Box 7560 BH";
char *WIFI_PASSWORD = "72117123858228781469";

// // IR LED pin
// const uint16_t kIrLed = 2;
// IRsend irsend(kIrLed);

// LED pins
const int Red_LED_pin = 32;
const int Green_LED_pin = 33;

// // Example IR codes for Mitsubishi AC
// uint8_t mitsubishiState_on[19]={0xAD, 0x51, 0x3C, 0xE5, 0x1A, 0x0C, 0xF3, 0x05, 0xFA, 0x00, 0xFF, 0xC0, 0x3F, 0xC8, 0x37, 0x00, 0xFF, 0x80, 0x7F};
// uint8_t mitsubishiState_off[19]={0xAD, 0x51, 0x3C, 0xE5, 0x1A, 0x04, 0xFB, 0x05, 0xFA, 0x00, 0xFF, 0xC0, 0x3F, 0xC8, 0x37, 0x00, 0xFF, 0x80, 0x7F};

// Web socket client
// using namespace websockets;
// WebsocketsClient client;
WebSocketsClient webSocket;

bool socketStatus = false;

// Settings JSON object
DynamicJsonDocument settingsJson(1024);

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{
  switch (type)
  {
  case WStype_DISCONNECTED:
    if (socketStatus == true) {
      Serial.println("[WSc] Disconnected!");
    }
    socketStatus = false;

    break;
  case WStype_CONNECTED:
    Serial.println("[WSc] Connected to websocket");

    socketStatus = true;
    break;
  case WStype_TEXT:
  {
    Serial.printf("[WSc] %s\n", payload);

    if (strcmp((char *)payload, "Server is working!") == 0)
    {
      // Send device ID to server
      webSocket.sendTXT(settingsJson["deviceID"].as<const char *>());

      // Break early
      break;
    }

    // Parse request data
    DynamicJsonDocument requestJson(1024);
    deserializeJson(requestJson, (char *)payload);

    if (requestJson["op"] == "get-settings")
    {
      // Serialize current settings to string
      String settingsString;
      serializeJson(settingsJson, settingsString);

      // Send settings to server
      webSocket.sendTXT(settingsString);
    }
    else if (requestJson["op"] == "update-settings")
    {
      // Update settings
      JsonVariant settingsToUpdate = requestJson["settings"];

      // Iterate through settings to update
      for (JsonPair pair : settingsToUpdate.as<JsonObject>())
      {
        settingsJson[pair.key()] = pair.value();
      }
    }

    break;
  }
  default:
    break;
  }
}

// void turn_ac_on(){
//   irsend.sendMitsubishiHeavy152(mitsubishiState_on);
//   delay(500);
//   digitalWrite(Green_LED_pin, HIGH);
//   delay(1500);
//   digitalWrite(Green_LED_pin, LOW);
// }

// void turn_ac_off(){
//   irsend.sendMitsubishiHeavy152(mitsubishiState_off);
//   delay(500);
//   digitalWrite(Red_LED_pin, HIGH);
//   delay(1500);
//   digitalWrite(Red_LED_pin, LOW);
// }

void setup()
{
  Serial.begin(115200);
  Serial.setDebugOutput(true);

  // Default/current settings (safe in a file?)
  String settings = "{\"deviceID\":\"DEVICE IDENTIFIER\",\"setting1\":\"value1\",\"setting2\":\"value2\"}";
  // Parse settings into settings object
  deserializeJson(settingsJson, settings);

  // Connect to WiFi network
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  webSocket.beginSSL("accontroller.tbrouwer.com", 443, "/ws");
  webSocket.onEvent(webSocketEvent);
}

void loop()
{
  // Check for new messages
  webSocket.loop();
}
