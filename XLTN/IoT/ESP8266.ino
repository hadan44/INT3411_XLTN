#include <DHT.h>
#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <IRrecv.h>
#include <IRutils.h>
#include <IRsend.h>

#define DHTPIN 5    // modify to the pin we connected
#define DHTTYPE DHT21   // AM2301 

const char* ssid="Tiendauto";
const char* pass="hoilamgi";
const char* brokerUser = "username";
const char* brokerPass = "123456";
const char* broker = "192.168.0.109";
const char* outTopic="Iot/Infra/Register";
const char* senTopic="Iot/Sensor";
//const char* inTopic ="Iot/Infra/Register";
const int mqtt_port = 1883;


IRrecv irrecv(5);// init new receiver
decode_results results;// save decoded result

IRsend irsend(4); // init ir send

DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

void setupWifi(){
  delay(50);
  Serial.println("Connecting to wifi");
 WiFi.begin(ssid, pass); 
  while (WiFi.status() != WL_CONNECTED) {
     delay(50);
    Serial.print(".");
  }
  Serial.println("Connected");
  delay(1000);
}
 
void reconnect(){
  while(!client.connected()){
    if(client.connect("ESP8266Client", brokerUser, brokerPass)){
      Serial.println("connected");
      // Subscribe
      client.subscribe("Iot/Ir");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length){
  Serial.print("New message topic:");
  Serial.println(topic);
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(payload);
  if (!root.success()) {
    Serial.println("parseObject() failed");
    return;
  }
  String id = root["infra_id"];
  byte value = root["value"];

  // Print values.
  Serial.print("id:");
  Serial.println(id);
  Serial.print("value:");
  Serial.println(value);

  //on-off SAMSUNG TV
  if(value == 0) {
    irsend.sendSAMSUNG(3772793023); 
    return;
  }

  //volume up SAMSUNG TV
  if(value == 1) {
    irsend.sendSAMSUNG(3772833823);
    return;
  }

  //volume down SAMSUNG TV
  if(value == 2) {
    irsend.sendSAMSUNG(3772829743);
    return;
  }

  //mute SAMSUNG TV
  if(value == 3) {
    irsend.sendSAMSUNG(3772837903);
    return;
  }

  //channel up SAMSUNG TV
  if(value == 4) {
    irsend.sendSAMSUNG(3772795063);
    return;
  }

  //channel down SAMSUNG TV
  if(value == 5) {
    irsend.sendSAMSUNG(3772778743);
    return;
  }
}

JsonObject& payload(float value, String type){
  StaticJsonBuffer<300> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();
  JSONencoder["infra_id"] = type;
  JSONencoder["value"] = value;
  return JSONencoder;
}

void registerToServer(char* type, char* sensorName){
    StaticJsonBuffer<300> JSONbuffer;
    JsonObject& JSONencoder = JSONbuffer.createObject();
 
    JSONencoder["infra_id"] = sensorName;
    JSONencoder["type"] = type;
    JSONencoder["in_topic"] = " ";
    JSONencoder["out_topic"] = outTopic;
   
    char JSONmessageBuffer[100];
    JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    if(client.publish("Iot/Infra/Register",JSONmessageBuffer) == true) {
        Serial.println(F("Register Success!"));
        return;
      } else {
        Serial.println(F("Register Fail!"));
        delay(1000);
    } 
} 

void setup() {
  delay(100);
  Serial.begin(9600);
  Serial.println("running");
  setupWifi();
  delay(200);
  client.setServer(broker, mqtt_port);
  delay(200);
  client.setCallback(callback);
  delay(200);
  client.connect("ESP8266Client", brokerUser, brokerPass);
  delay(200);
  client.subscribe("Iot/Ir");
  delay(500);
  pinMode(4,OUTPUT);
  irsend.begin();
  delay(200);
  dht.begin();
  delay(500);
}

void loop() {
   if (!client.connected()){
      reconnect();
    }
  client.loop();
  float h = dht.readHumidity();
  float t = dht.readTemperature(); // or dht.readTemperature(true) for Fahrenheit;
  if (isnan(h) || isnan(t)) {
      delay(2000);
      return;
  }
  char JSONmessageBuffer[100] = {};

    Serial.print(F("Temperature = "));
    Serial.print(t);
    Serial.print(F( " *C,  Humidity = " ));
    Serial.print(h);
    Serial.println(F( "%" ));
  
  payload(t, "AM2301_T").printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  client.publish(senTopic,JSONmessageBuffer);
  JSONmessageBuffer[100] = {};
  payload(h, "AM2301_H").printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  client.publish(senTopic,JSONmessageBuffer);
  delay(10000);
}