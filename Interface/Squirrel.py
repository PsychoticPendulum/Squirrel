#! /usr/bin/env python3

import os
import sys
import json
import time
import base64

try:
    from Log import *
except:
    print("ERROR:   Library missing: Log")
    exit(1)

try:
    import pandas as pd
except:
    Log(LVL.FAIL, "Missing Library:    pandas")

try:
    import MySQLdb
except:
    Log(LVL.FAIL, "Library missing:    mysql")

try:
    import paho.mqtt.client as mqtt
except:
    Log(LVL.FAIL, "Library missing:    paho.mqtt")


def SendToDatabase(value):
    db = MySQLdb.connect(host=host,user=user,password=password,db=database)
    cursor = db.cursor()
    query = f"INSERT INTO arduino (value, time) VALUES ({value}, CURRENT_TIME());"
    cursor.execute(query)
    db.commit()
    db.close()


def on_connect(client,userdata,flags,rc):
    Log(LVL.INFO, f"Connected to MQTT broker with response {rc}")
    client.subscribe(f"{topic}")


def on_message(client,userdata,msg):
    Log(LVL.INFO, f"Message recieved: {str(msg.payload.decode('utf-8'))}")
    SendToDatabase(str(msg.payload.decode('utf-8')))
    time.sleep(1) 

def ParseJSON(path):
    with open(path, "rb") as json_file:
        json_data = json.load(json_file)
        return json_data.get("host"), json_data.get("user"),base64.b64decode(json_data.get("pass")).decode("utf-8"), json_data.get("db"), json_data.get("broker"), json_data.get("topic"), int(json_data.get("port")), int(json_data.get("ttl"))


if len(sys.argv) < 2:
    Log(LVL.FAIL, "Not enough arguments")

host, user, password, database, broker, topic, port, ttl = ParseJSON(sys.argv[1])

message_received = False

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print(broker)
client.connect(broker,port,ttl)

try:
    client.loop_forever()
except KeyboardInterrupt:
    Log(LVL.WARN, "Keyboard Interrupt")
