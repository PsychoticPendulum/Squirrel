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

def ParseJSON(path):
    with open(path, "rb") as json_file:
        json_data = json.load(json_file)
        return json_data.get("host"), json_data.get("user"),base64.b64decode(json_data.get("pass")).decode("utf-8"), json_data.get("db"), json_data.get("broker"), json_data.get("topic")

def GetInput(host, topic):
    return os.popen(f"mosquitto_sub -C 1 -h {host} -t {topic}").read().rstrip('\n')

def CheckDependencies():
    if sys.platform == "win32":
        Log(LVL.FAIL, "Windows is not yet supported")
    else:
        return os.popen("whereis mosquitto_sub > /dev/null ; echo $?").read().rstrip('\n')
    return False

def SendToDatabase(host, user, password, database):
    db = MySQLdb.connect(host=host,user=user,password=password,db=database)
    cursor = db.cursor()
    query = f"INSERT INTO arduino (value, time) VALUES ({VALUE}, CURRENT_TIME());"
    cursor.execute(query)
    db.commit()
    db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        Log(LVL.FAIL, "Not enough arguments")
    path = sys.argv[1]

    CheckDependencies()

    host, user, password, database, broker, topic = ParseJSON(path)

    while True:
        try:
            data = float(GetInput(broker,topic))

        except KeyboardInterrupt:
            Log(LVL.INFO, "Keyboard Interrupt detected. Ending execution")
            exit(0)

        except:
            Log(LVL.WARN, "Value could not be parsed")

        time.sleep(1)
