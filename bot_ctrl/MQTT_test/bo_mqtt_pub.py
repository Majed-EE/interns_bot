import paho.mqtt.client as mqtt

BROKER = "98.91.21.224"
PORT = 1883
TOPIC_LIST = ["CAS/haptic_feedback", "UE/to_toy_arm"]#"robot/shobha/control"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Enter command: W S A D")

while True:
    msg = input("Command: ").upper()
    if msg in ['W', 'S', 'A', 'D', 'k']:
        client.publish(TOPIC_LIST, msg)
        print("Sent:", msg)