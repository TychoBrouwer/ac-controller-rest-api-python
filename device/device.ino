#include <WiFi.h>             // Library used for wifi connection
#include <ArduinoJson.h>      // Library used for JSON parsing
#include <WebSocketsClient.h> // Library used for websocket: https://github.com/Links2004/arduinoWebSockets

#include <Arduino.h>
#include <IRremoteESP8266.h> // Library used for IR transmission: https://github.com/crankyoldgit/IRremoteESP8266
#include <IRac.h>
#include <IRutils.h>
#include <IRrecv.h>

#define DEBUG true

#if (DEBUG)
#define SERIAL_BEGIN()    \
  {                       \
    Serial.begin(115200); \
  }
#define PRINTS(s)       \
  {                     \
    Serial.print(F(s)); \
  }
#define PRINT(s, v)     \
  {                     \
    Serial.print(F(s)); \
    Serial.println(v);  \
  }
#define PRINTF(s, v)          \
  {                           \
    Serial.print(F(s));       \
    Serial.printf("%s\n", v); \
  }
#else
#define SERIAL_BEGIN()
#define PRINTS(s)
#define PRINT(s, v)
#define PRINTF(s, v)
#endif

#define kSendPin 2
#define kRecvPin 22

#define Red_LED_pin 32
#define Green_LED_pin 33

// Commom AC class
IRac ac(kSendPin);
stdAc::state_t state;

// IR Receive class
const uint16_t kCaptureBufferSize = 1024;
const uint8_t kTimeout = 50;
IRrecv irrecv(kRecvPin, kCaptureBufferSize, kTimeout, true);

// Web socket client
WebSocketsClient webSocket;
bool socketConnected = false;

// WiFi credentials
char *WIFI_SSID = "FRITZ!Box 7560 BH";
char *WIFI_PASSWORD = "72117123858228781469";

// Client indentifier
char *deviceID = "DEVICE IDENTIFIER";

// Timeout variables for during sending
uint32_t timeoutTime = 0;
uint16_t timeoutPeriod = 1000;

// Function to convert bool to string 1 or 0
bool charToBool(const char *state)
{
  return state == "1";
}

char *stringToChar(String string)
{
  int len = string.length() + 1;
  char *buf = new char[len];
  string.toCharArray(buf, len);

  return buf;
}

String stateToString(stdAc::state_t state)
{
  // Construct JSON string
  String stateString = "\{\"deviceID\":\"DEVICE IDENTIFIER";
  stateString = stateString + "\",\"protocol\":\"" + typeToString(state.protocol);
  stateString = stateString + "\",\"model\":\"" + state.model;
  stateString = stateString + "\",\"power\":\"" + state.power;
  stateString = stateString + "\",\"mode\":\"" + ac.opmodeToString(state.mode);
  stateString = stateString + "\",\"degrees\":\"" + state.degrees;
  stateString = stateString + "\",\"celsius\":\"" + state.celsius;
  stateString = stateString + "\",\"fanspeed\":\"" + ac.fanspeedToString(state.fanspeed);
  stateString = stateString + "\",\"swingv\":\"" + ac.swingvToString(state.swingv);
  stateString = stateString + "\",\"swingh\":\"" + ac.swinghToString(state.swingh);
  stateString = stateString + "\",\"quiet\":\"" + state.celsius;
  stateString = stateString + "\",\"turbo\":\"" + state.turbo;
  stateString = stateString + "\",\"econo\":\"" + state.econo;
  stateString = stateString + "\",\"light\":\"" + state.light;
  stateString = stateString + "\",\"filter\":\"" + state.filter;
  stateString = stateString + "\",\"clean\":\"" + state.clean;
  stateString = stateString + "\",\"beep\":\"" + state.beep;
  stateString = stateString + "\",\"sleep\":\"" + state.sleep;
  stateString = stateString + "\",\"clock\":\"" + state.clock;
  stateString = stateString + "\"}";

  PRINTS("[JSON] Successfully parsed state string\n");

  return stateString;
}

void setAcNextState(const char *option, const char *stateValue)
{
  if (strcmp(option, "model") == 0)
  {
    state.model = ac.strToModel(stateValue);
  }
  else if (strcmp(option, "power") == 0)
  {
    state.power = charToBool(stateValue);
  }
  else if (strcmp(option, "mode") == 0)
  {
    state.mode = ac.strToOpmode(stateValue);
  }
  else if (strcmp(option, "degrees") == 0)
  {
    state.degrees = atof(stateValue);
  }
  else if (strcmp(option, "celsius") == 0)
  {
    state.celsius = charToBool(stateValue);
  }
  else if (strcmp(option, "fanspeed") == 0)
  {
    state.fanspeed = ac.strToFanspeed(stateValue);
  }
  else if (strcmp(option, "quiet") == 0)
  {
    state.quiet = charToBool(stateValue);
  }
  else if (strcmp(option, "turbo") == 0)
  {
    state.turbo = charToBool(stateValue);
  }
  else if (strcmp(option, "econo") == 0)
  {
    state.econo = charToBool(stateValue);
  }
  else if (strcmp(option, "light") == 0)
  {
    state.light = charToBool(stateValue);
  }
  else if (strcmp(option, "filter") == 0)
  {
    state.filter = charToBool(stateValue);
  }
  else if (strcmp(option, "clean") == 0)
  {
    state.clean = charToBool(stateValue);
  }
  else if (strcmp(option, "beep") == 0)
  {
    state.beep = charToBool(stateValue);
  }
  else if (strcmp(option, "sleep") == 0)
  {
    state.sleep = atoi(stateValue);
  }
  else if (strcmp(option, "clock") == 0)
  {
    state.clock = atoi(stateValue);
  }

  PRINT("[AC] Succesfully set next AC status for ", option);
  PRINT("[AC] to value ", stateValue);
}

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{
  switch (type)
  {
  case WStype_DISCONNECTED:
    // Set socket connection to false and print disconnected once
    if (socketConnected == true)
    {
      PRINTS("[WSc] Disconnected!\n");
    }
    socketConnected = false;

    break;
  case WStype_CONNECTED:
    PRINTS("[WSc] Connected to websocket\n");

    // Set socket connection to true
    socketConnected = true;
    break;
  case WStype_TEXT:
  {
    PRINTF("[WSc] ", payload);

    if (strcmp((char *)payload, "Server is working!") == 0)
    {
      // Send device ID to server
      webSocket.sendTXT(deviceID);

      PRINTS("[WSc] Send running server conformation\n");

      // Break early
      break;
    }

    // Parse request data
    DynamicJsonDocument requestJson(512);
    deserializeJson(requestJson, (char *)payload);

    if (requestJson["op"] == "get-settings")
    {
      // Get JSON state char
      const char *stateString = stringToChar(stateToString(state));

      // Send settings to server
      webSocket.sendTXT(stateString);
    }
    else if (requestJson["op"] == "update-settings")
    {
      // Iterate through settings to update
      for (JsonPair pair : requestJson["settings"].as<JsonObject>())
      {
        // Set new state of AC
        setAcNextState(pair.key().c_str(), pair.value().as<const char *>());

        // Send new state to AC
        timeoutTime = millis();
        ac.sendAc(state, &state);
      }
    }
    else if (requestJson["op"] == "update-weather")
    {
    }

    PRINTS("[WSc] Successfully handled websocket request\n");

    break;
  }
  default:
    PRINTS("[WSc] Unrecognised websocket event type\n");

    break;
  }
}

void receiveIR()
{
  // IR receive results
  decode_results RecvResults;

  // Decode results
  if (irrecv.decode(&RecvResults))
  {
    // Debug for testing
    PRINT("[AC] IR data successfully decoded ", typeToString(RecvResults.decode_type));

    // Check if protocol detected is supported by library
    if (ac.isProtocolSupported(RecvResults.decode_type))
    {
      PRINTS("[AC] AC protocol is supported");

      // Get state from received char
      IRAcUtils::decodeToState(&RecvResults, &state);

      PRINT("[AC] Protocol: ", state.protocol);
      PRINT("[AC] Model: ", state.model);

      ac.sendAc(state, &state);

      PRINTS("[AC] Initial state successfully set\n");
    }

    // Receive the next value
    irrecv.resume();
  }
}

void setup()
{
  SERIAL_BEGIN();

  // Connect to WiFi network
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    PRINTS(".");
  }

  PRINTS("\n");
  PRINT("[WiFi] Connected at IP address: ", WiFi.localIP());

  // Begin websocket
  webSocket.beginSSL("accontroller.tbrouwer.com", 443, "/ws");
  webSocket.onEvent(webSocketEvent);

  PRINTS("[WSc] Websocket created\n");

  // Start the receiver
  irrecv.enableIRIn();
}

void loop()
{
  // Check for new websocket messages
  webSocket.loop();

  // If new IR message received
  if (millis() > timeoutTime + timeoutPeriod)
  {
    receiveIR();
  }
}
