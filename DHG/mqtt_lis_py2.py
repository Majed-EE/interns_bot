import time
import json
import paho.mqtt.client as mqtt

# MQTT Broker settings
# test for experiment is 1000 seconds
BROKER = "54.81.75.57"  # Public test broker
PORT = 1883
TOPIC_LIST = ["CAS/haptic_feedback"]
global sync_time, packet_hist
packet_hist = []
sync_time = 1773291123


# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        for topic in TOPIC_LIST:
            client.subscribe(topic)
            print("Subscribed to topic: {}".format(topic))  # Python 2.7 string formatting
    else:
        print("Failed to connect, return code {}".format(rc))

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print("Received message from topic {}: {}".format(msg.topic, msg.payload))
    
    # 1. Decode payload
    payload_str = msg.payload
    # 2. Parse string to JSON (dictionary)
    data = json.loads(payload_str)
    data = dict(data)
    
    # Handle time calculation
    rec_time = (time.time() - sync_time) % 1000
    
    # Access packet info
    packet_no, sent_time = data["packet_info"][0], data["packet_info"][1]  # [packet, sent_Time]
    
    # Calculate latency
    packet_lat = round((rec_time - sent_time), 3)
    
    print("packet number: {}, latency: {}, rec_time: {}, sent_time: {}".format(
        packet_no, packet_lat, rec_time, sent_time))
    
    packet_hist.append([packet_no, packet_lat, rec_time, sent_time])

# Create MQTT client and set callbacks
# Note: In Python 2.7, you might need to specify protocol version
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(BROKER, PORT, 60)  # Default MQTT port is 1883
    print("Connecting to broker...")
    
    # Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting
    client.loop_forever()
    
except KeyboardInterrupt:
    print("breaking ")
    client.disconnect()
    
except Exception as e:
    print("An error occurred: {}".format(e))