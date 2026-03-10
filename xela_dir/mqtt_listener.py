####################### MQTT Publisher ################################
import paho.mqtt.client as mqtt
# MQTT Broker settings
BROKER = "50.17.69.6"  # Public test broker
PORT = 1883
TOPIC_LIST = ["CAS/haptic_feedback"]



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
except Exception as e:
    print(f"An error occurred: {e}")