import serial
import time
import paho.mqtt.client as mqtt

# -------- SETTINGS --------
COM_PORT = "COM9"      # change if needed
BAUD_RATE = 9600
BROKER = "100.53.2.92"
PORT = 1883
TOPIC_LIST= ["CAS/haptic_feedback", "UE/to_toy_arm","UE/to_wheels"]
# --------------------------

arduino = serial.Serial(COM_PORT, BAUD_RATE)
time.sleep(2)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    for i in TOPIC_LIST:
        client.subscribe(i)
    
def on_message(client, userdata, msg):
    command = msg.payload.decode().upper()
    print("Received:", command)

    if command in ['W', 'S', 'A', 'D', 'K']:
        arduino.write(command.encode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Waiting for MQTT commands...")
client.loop_forever()