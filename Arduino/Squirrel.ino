#include "Squirrel.h"
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 0x5

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);

void setup(void) {
  Serial.begin(115200);
  pinMode(D0,OUTPUT);

  connect_to_network(ssid,passwd);
  client.setServer(server,1883);
  client.setCallback(callback);
}

int GetTemp() {
  DS18B20.requestTemperatures();
  char *buffer = (char*)malloc(sizeof(char)*0xf);
  sprintf(buffer, "%d", (int)DS18B20.getTempCByIndex(0));
  int temp = atoi(buffer);
  free(buffer);
  return temp;
}

void loop(void) {
  Serial.println("Here we");
  if (!client.connected()) { connect_to_server(); }
  Serial.println("go!");

  int temp = GetTemp();
  sprintf(msg,"%d",temp);
  publish("dev/test",msg);

  client.loop();
}

void connect_to_server(void) {
  Serial.print("Connecting to server ");
  while (!client.connected()) {
    Serial.print(".");
    String clientID = "ESP8266Client-";
    clientID += String(random(0xffff),HEX);
    
    digitalWrite(D0,LOW);
    if (client.connect(clientID.c_str())) {
      sprintf(msg,"I exist and my name is %s", clientID.c_str());
      client.publish("dev/test",msg);
      client.subscribe("dev/test");
    } else { delay(5000); }
    digitalWrite(D0,HIGH);
  }
}

void connect_to_network(const char *ssid, const char *passwd) {
  Serial.println();
  Serial.println("Establishing connection");
  WiFi.begin(ssid, passwd);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    digitalWrite(D0,LOW); delay(250);
    digitalWrite(D0,HIGH); delay(250);
  } Serial.print("Success!\nIP: ");
  Serial.println(WiFi.localIP());
}

void publish(const char *topic, const char *msg) {
  Serial.println(msg);
  client.publish(topic,msg);
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("]: ");

  memset(msg, 0x0, 0xff * sizeof(char));
  for (int i = 0; i < length; i++) { msg[i] = ((char)payload[i]); }
  Serial.println(msg);
}
