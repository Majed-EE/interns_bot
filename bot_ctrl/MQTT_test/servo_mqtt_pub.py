import paho.mqtt.client as mqtt

BROKER = "98.91.21.224"
PORT = 1883
TOPIC = "UE/to_toy_arm"

client = mqtt.Client()
client.connect(BROKER, PORT)

print("Publisher Started")

while True:

    index = input("Enter Index Angle (130-150): ")
    middle = input("Enter Middle Angle (30-50): ")

    msg = f"{index},{middle}"

    client.publish(TOPIC, msg)

    print("Sent ->", msg)