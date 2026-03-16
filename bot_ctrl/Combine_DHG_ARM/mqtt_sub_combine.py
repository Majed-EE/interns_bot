import paho.mqtt.client as mqtt
import serial
import json
import time

# ---------- CONFIG ----------
BROKER_ADDRESS = "100.53.2.92"
BROKER_PORT = 1883
TOPIC = "UE/to_toy_arm"
SERIAL_PORT = "COM14"
BAUD_RATE = 9600
# ----------------------------

# Arduino serial setup
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(1)
arduino.write("130,50\n".encode())
print("starting..........")
time.sleep(2)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        index_value = data.get("Index")   # 0-1 range
        middle_value = data.get("Middle") # 0-1 range

        # Prepare serial command
        command = ""

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
        arduino.write(f"{command}\n".encode())

        # Print live values
        print(f"\rIndex: {index_value} | Servo: {index_angle if index_value is not None else 'NA'}° | "
              f"Middle: {middle_value} | Servo: {middle_angle if middle_value is not None else 'NA'}°", end='')

    except Exception as e:
        print("Error:", e)

# MQTT setup
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
client.subscribe(TOPIC)
print("MQTT Subscriber Running... (Press Ctrl+C to exit)")
client.loop_forever()