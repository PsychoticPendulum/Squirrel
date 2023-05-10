#pragma once

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

WiFiClient espclient;
PubSubClient client(espclient);

const char *ssid    = "F8";
const char *passwd  = "goodbyeworld!";
const char *server  = "172.20.10.13";

void connect_to_server(void);
void connect_to_network(const char *ssid, const char *passwd);

void publish(const char *topic, const char *msg);

char *msg = (char*)calloc(0xff,sizeof(char));
void callback(char *topic, byte *payload, unsigned int length);