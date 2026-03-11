import paho.mqtt.client as mqtt
import json
import time
BROKER = "54.152.42.154"
PORT = 1883
TOPIC_LIST = ["UE/to_toy_arm","UE/to_wheels"]#"robot/shobha/control"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Enter command: W S A D")
x=0
direction_list=['W', 'S', 'A', 'D', 'k']
while True:
    # msg = input("Command: ").upper()
    msg = direction_list[ x%len(direction_list) ]
    x+=1
    if msg in ['W', 'S', 'A', 'D', 'k']:
        ctrl_dict = {"direction":msg}
        msg = json.dumps(ctrl_dict)
        client.publish("UE/to_wheels", msg)
        print("Sent:", msg)
    t=3
    time.sleep(t)
    print(f"sleeping of {t} seconds")
    msg={"Index":0.0,"Middle":0.0, "Pinky":0.5,"Thumb":0.5,"Ring":0.5}
    msg=json.dumps(msg)
    client.publish("UE/to_toy_arm",msg)
    print(f"Sent: ",msg)
    print(f"sleeping of {t} seconds")
    time.sleep(t)
    msg={"Index":1.0,"Middle":1.0, "Pinky":0.5,"Thumb":0.5,"Ring":0.5}
    msg=json.dumps(msg)
    client.publish("UE/to_toy_arm",msg)
    print(f"Sent: ",msg)
    print(f"sleeping of {t} seconds")
    time.sleep(t)

