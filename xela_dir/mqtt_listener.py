####################### MQTT Publisher ################################
import paho.mqtt.client as mqtt
import json
import time
# MQTT Broker settings
# test for experiment is 1000 seconds
BROKER = "54.81.75.57"  # Public test broker
PORT = 1883
TOPIC_LIST = ["CAS/haptic_feedback"]
global sync_time, packet_hist
packet_hist=[]
sync_time= 1773291123


# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        for topic in TOPIC_LIST:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message from topic {msg.topic}: {msg.payload.decode()}")
    # data= dict(json.loads(msg.payload.decode()))
    # msg=dict(msg.payload)
    payload_str = msg.payload.decode('utf-8')
        # 2. Parse string to JSON (dictionary)
    data = json.loads(payload_str)
    data=dict(data)
    rec_time= time.time()
    rec_time=(rec_time)%1000
    print(f"rec_time: {rec_time}")
    packet_no,sent_time= data["packet_info"][0], data["packet_info"][1] #[packet,sent_Time]
    packet_lat=round((rec_time-sent_time),3 )
    print(f"pakcet number: {packet_no}, latency: {packet_lat}, rec_time: {rec_time}, sent_time: {sent_time}")
    packet_hist.append([packet_no,packet_lat,rec_time,sent_time])

# Create MQTT client and set callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(BROKER, 1883, 60)  # Default MQTT port is 1883
    print("Connecting to broker...")
    
    # Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting
    client.loop_forever()
except KeyboardInterrupt:
    print("breaking ")
    client.disconnect()
except Exception as e:
    print(f"An error occurred: {e}")