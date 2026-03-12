import serial
import time
import paho.mqtt.client as mqtt
import json
# -------- SETTINGS --------
COM_PORT = "COM14"      # change if needed
BAUD_RATE = 9600
BROKER = "54.152.42.154"
PORT = 1883
TOPIC_LIST= ["CAS/haptic_feedback", "UE/to_toy_arm","UE/to_wheels"]
# --------------------------
_arduino=True
print(f"arduino connected: {_arduino}")
if _arduino:
    arduino = serial.Serial(COM_PORT, BAUD_RATE)
    time.sleep(2)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    for i in TOPIC_LIST:
        client.subscribe(i)
    
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"Topic: {msg.topic}")
    print("Received message:", data)
    topic=msg.topic
    if topic =="UE/to_wheels":
        print(f"to topic {topic}")
        # data=data
        direction ="wheel,"
        direction+=data["direction"].upper() # json is {"direction": char direction}
        # valid direction  "W S A D" else stop
        if direction[-1] in ['W', 'S', 'A', 'D', 'K']:
            
            if _arduino: arduino.write(direction.encode())
        else: 
            print(f"Debug message: invalid direction {direction}")
    elif topic =="UE/to_toy_arm":
        print(f"to topic {topic}")
        try:
            data = json.loads(msg.payload.decode())
            index_value = data.get("Index")   # 0-1 range
            middle_value = data.get("Middle") # 0-1 range

            # Prepare serial command
            command = "arm,"
            if index_value is not None:
                # Map Index 0-1 → 130-150
                index_angle = int(130 + (1-index_value) * 20)
                command += f"{index_angle}"
            else:
                command += "130"  # Default if missing

            command += ","  # separator for middle servo

            if middle_value is not None:
                # Map Middle 0-1 → 50-30
                middle_angle = int(50 - (1-middle_value) * 20)
                command += f"{middle_angle}"
            else:
                command += "50"  # Default if missing

            # Send to Arduino
            if _arduino: arduino.write(f"{command}\n".encode())

            # Print live values
            print(f"\rIndex: {index_value} | Servo: {index_angle if index_value is not None else 'NA'}° | "
                f"Middle: {middle_value} | Servo: {middle_angle if middle_value is not None else 'NA'}°", end='')

        except Exception as e:
            print("Error:", e)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Waiting for MQTT commands...")
client.loop_forever()
