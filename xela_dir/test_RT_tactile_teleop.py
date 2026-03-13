#!/usr/bin/env python3
# original code
import websocket
import json
import time
from time import sleep
import threading
import numpy as np
import paho.mqtt.client as mqtt
import json
from datetime import datetime

####################### MQTT Publisher ################################

# MQTT Broker settings
BROKER = "54.81.75.57"  # Public test broker
PORT = 1883
TOPIC = "CAS/haptic_feedback"
global last_val, crnt_pckt_num,packet_list, packet_hist
# global packet_hist
packet_hist=[]
last_val=0.0
packet_num=0
packet_list=[]
def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    """Callback when message is published"""
    print(f"Message published with mid: {mid}")

_MQTT=True



################################################################################
if _MQTT:
    client = mqtt.Client()
    
    # Assign callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(BROKER, PORT, 60)




# custom library imports
import MyXela 
feature_extractor = MyXela.XelaTactileFeatureExtractor()

# dataset_record=MyXela.XelaTactileRecorder(save_every=100)
# featu

ip_xela = "10.50.49.23" # xela ip, check from server
#"192.168.0.103"  # your computer IP on the network
port = 5000  # the port the server is running on
print(f"running client connecting to ws://{ip_xela}:{port}")
lastmessage = {"message": "No message"}  # default message you will overwrite when you get update

def on_message(wsapp, message):
    global lastmessage  # globalize to overwrite original
    global crnt_pckt_num
    try:
        data = json.loads(message)
    except Exception:
        pass
    else:
        try:
            if data["message"] == "Welcome":  # get the Welcome Message with details, print if you like
                print(data)
            else:
                lastmessage = data
        except Exception:
            pass  # ignore message as it's probably invalid

def threader(target, args=False, **targs):
    # args is tuple of arguments for threaded function other key-value pairs will be sent to Thread
    if args:
        targs["args"] = (args,)
    thr = threading.Thread(target=target, **targs)
    thr.daemon = True
    thr.start()

def mesreader():  # this is your app reading the last valid message you received
    global last_val, crnt_pckt_num
    crnt_pckt_num=0
    while True:  # to run forever,
        try:
            if lastmessage["message"] != "No message":
                # print(f"type of lastmessage: {type(lastmessage)}")
                # print(type(lastmessage), len(lastmessage))
                # print("I received: {}\n---".format(str(lastmessage)))
                # print("extracting feature")
                feature_extractor.extract_force(lastmessage)
                # print(f"Extracted features: {feature_extractor.fz_norm.shape, feature_extractor.fy_norm.shape, feature_extractor.fz_norm.shape}")
                pub_val=round( np.max(feature_extractor.fz_norm) ,2)

                if last_val==pub_val:
                    # print(f"last_val== pub_val: {last_val==pub_val}")
                    pub_val=0.0
                else:
                    if _MQTT: 
                        sent_time=(time.time()%1000)
                        print(f"sent time {sent_time}")
                        sent_time=round(sent_time,4)
                        print(f"ddsent time {sent_time}")
                        # now=datetime.now()
                        last_val=pub_val 
                        if last_val<0.3:
                            pub_val=0.0
                        crnt_pckt_num+=1
                        packet_list.append([crnt_pckt_num,sent_time])
                        print(f"published value (max of Fz norm): {pub_val} and crnt_pckt, sent time: {crnt_pckt_num,sent_time}")
                        pub_val=json.dumps({"stiffness":pub_val,"packet_info":[crnt_pckt_num,sent_time]})    
                        client.publish(TOPIC, pub_val)
                        print("published")

                # print("recording to dataset...")
                # dataset_record.record(lastmessage)
            t=1.5
            print(f"--- sleeping for {t} seconds ---")
            sleep(t)  # your calculations and processes here (sleep is used as simulation here)
        except KeyboardInterrupt:
            client.disconnect()
            print("breaking")
            break  # break on KeyboardInterrupt
        except Exception as e:
            print("Exception: {}: {}".format(type(e).__name__, e))

try:  # try to close the app once you press CTRL + C
    threader(mesreader, name="Receiver")  # start you main app
    websocket.setdefaulttimeout(1)  # you should avoid increasing it.
    wsapp = websocket.WebSocketApp("ws://{}:{}".format(ip_xela, port), on_message=on_message)  # set up WebSockets
    wsapp.run_forever()  # Run until connection dies
except Exception as e:
    print("Exception: {}: {}".format(type(e).__name__, e))

    exit()