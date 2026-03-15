
import paho.mqtt.client as mqtt
import serial

BROKER ="98.91.21.224"
PORT = 1883
TOPIC = "UE/to_toy_arm"

# Change COM port if needed
arduino = serial.Serial("COM3",9600)

def on_connect(client, userdata, flags, rc):
    print("Connected to Broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):

    data = msg.payload.decode()

    print("Received ->", data)

    arduino.write((data + "\n").encode())

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()