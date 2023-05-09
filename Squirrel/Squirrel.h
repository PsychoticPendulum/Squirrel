#pragma once

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

WiFiClient espclient;
PubSubClient client(espclient);

const char *ssid    = "wlan1313";
const char *passwd  = "wlan1313pw";
const char *server  = "192.168.1.95";

void connect_to_server(void);
void connect_to_network(const char *ssid, const char *passwd);

void publish(const char *topic, const char *msg);

char *msg = (char*)calloc(0xff,sizeof(char));
void callback(char *topic, byte *payload, unsigned int length);