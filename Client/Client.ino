#include <ESP8266WiFi.h>
#include <WebSocketClient.h>

const char* ssid     = "MasseyHacks2018";
char path[] = "/";
char host[] = "10.88.198.193";
  
WebSocketClient webSocketClient;

// Use WiFiClient class to create TCP connections
WiFiClient client;

// Pins
const int TRIG_PIN = 0; // I assume this is the port labelled D4
const int ECHO_PIN = 2; // I assume this is the port labelled D2

// Anything over 400 cm (23200 us pulse) is "out of range"
const unsigned int MAX_DIST = 200;

void setup() {
  // Set up the trigger pin as output
  pinMode(TRIG_PIN, OUTPUT);
  digitalWrite(TRIG_PIN, LOW);
  // Set up the echo pin as input
  pinMode(ECHO_PIN, INPUT);
  // Start serial debug interface
  Serial.begin(115200);
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(5000);
  

  // Connect to the websocket server
  if (client.connect(host, 2028)) {
    Serial.println("Connected");
  } else {
    Serial.println("Connection failed.");
    while(1) {
      // Hang on failure
    }
  }

  // Handshake with the server
  webSocketClient.path = path;
  webSocketClient.host = host;
  if (webSocketClient.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
    while(1) {
      // Hang on failure
    }  
  }

}


void loop() {
  String data;
  unsigned long duration;
  float cm;

  if (client.connected()) {
    
    webSocketClient.getData(data);
    if (data.length() > 0) {
      Serial.print("Received data: ");
      Serial.println(data);
    }

    // Hold the trigger pin high for at least 10 us
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    // Measure how long the echo pin was held high (pulse width)
    duration = pulseIn(ECHO_PIN, HIGH);

    // Calculate distance in centimetres. The constants
    // are found in the datasheet, and calculated from the assumed speed 
    //of sound in air at sea level (~340 m/s).
    cm = duration / 58.0;

    // Print out results
    if ( cm >= 10 && cm <= 40 ) { //block 1
      data = "1";
    } else if(cm >= 60 && cm <= 90){ //block 2
      data = "2";
    }
    else{
      data = "0";
    }
    Serial.print(cm);
    Serial.println(" cm \t");
    webSocketClient.sendData(data);
    // Here's where we actually wrap and send the data
    
    
  } else {
    Serial.println("Client disconnected.");
    while (1) {
      // Hang on disconnect.
    }
  }
  
  // Wait at least 60ms before next measurement
  delay(60);
  
}
