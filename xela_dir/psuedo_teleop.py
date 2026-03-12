import json
import time
import MyXela
import numpy as np
import matplotlib.pyplot as plt
feature_extractor = MyXela.XelaTactileFeatureExtractor()
import time
# Path to the JSON file
json_file_path = "xelaDataset/xela_record_0000_1768303296.json"

##### mqtt variables ####
_MQTT=True
BROKER_EDGE_IP =  "10.10.12.24"
BROKER_CUSTOM_CLOUD_IP = "54.81.75.57"
# BROKER_CLOUD_IP=   "test.mosquitto.org"

global sync_time, crnt_pckt_num
sync_time= 1773291123
crnt_pckt_num = 0  # current packet number
################################## MQTT SETUP - optional ##################################
import paho.mqtt.client as mqtt

node_topic="CAS/haptic_feedback"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code", reason_code)

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")
    # def on_message(client, userdata, msg):
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message


# mqtt_send=True  # set to True to enable MQTT sending
if _MQTT:

    client.connect(BROKER_CUSTOM_CLOUD_IP, 1883, 60)

    client.loop_start()
    print(f"connected to mqtt broker IP {BROKER_CUSTOM_CLOUD_IP}")
#############################################################################################






def print_values_from_json(json_file_path):
    global crnt_pckt_num
    """
    Reads a JSON file and prints the values at each timestep.

    Parameters:
        json_file_path (str): Path to the JSON file.
    """
    print(f"feature_extractor mean and std: {feature_extractor.mean_rest.shape, feature_extractor.std_rest.shape}")
    # time.sleep(10)
    data_array=[]
    try:
        # Load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        print(f"Loaded data type: {type(data), len(data)}")
        #feature_extractor mean and std: ((16, 3), (16, 3))
        # Loaded data type: (<class 'list'>, 100)
        # time.sleep(10)
        # Iterate over the timesteps and print values
        for timestep, values in enumerate(data):
            # print(f"Timestep {timestep}: {values}")
            print(f"**************currently at time step: {timestep}**************************")
            feature_extractor.extract_force(values)
            
            print(f"Extracted features: {feature_extractor.fz_norm.shape, feature_extractor.fy_norm.shape, feature_extractor.fz_norm.shape}")
            # output -> add size Extracted features: ((16,), (16,), (16,))
            pub_val=round(np.max(feature_extractor.fz_norm),3)  # for force value
            shape_value = round(np.random.uniform(0,0.5), 2) # for shape value
            if _MQTT:
                crnt_pckt_num+=1
                sent_time=round((time.time()-sync_time),3)
                sent_time = sent_time%1000
                payload= json.dumps({"xela_1": pub_val,"arm_shape": shape_value,"packet_info": [crnt_pckt_num,sent_time]})
                print("publishing topic: ", node_topic, " payload: ", payload, "packet_info: ", [crnt_pckt_num,sent_time])
                client.publish(node_topic, payload)  # Publish to topic1
            data_array.append(feature_extractor.norm_special)
            time.sleep(2.1)  # simulate delay between timesteps

    except Exception as e:
        print(f"Error reading JSON file: {e}")

    return data_array

# if __name__ == "__main__":
data_array=print_values_from_json(json_file_path)
# data_array=np.array(data_array)
# # print(f"data_array.shape: {data_array.shape}")
# mean, std = np.mean(data_array, axis=0), np.std(data_array, axis=0)
# # print(f"Calculated mean and std shapes: {mean.shape, std.shape}")
# # print(f"mean: {mean}")
# # Step function plot for each taxel over time
# fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
# arr0= data_array[:,:,0]  # Fx normalized
# arr1= data_array[:,:,1]  # Fy normalized
# arr2= data_array[:,:,2]  # Fz normalized
# # arr2= z_norm_rest
# for i in range(arr0.shape[1]):
#     axs[0].step(range(arr1.shape[0]), arr1[:, i], where='mid', label=f'Taxel {i+1}')
# axs[0].set_title('Array x: Step Function Plot')
# axs[0].set_ylabel('Value')
# axs[0].legend(loc='upper right', fontsize='small', ncol=4)

# for i in range(arr1.shape[1]):
#     axs[1].step(range(arr1.shape[0]), arr1[:, i], where='mid', label=f'Taxel {i+1}')
# axs[1].set_title('Array y: Step Function Plot')
# axs[1].set_ylabel('Value')
# axs[1].legend(loc='upper right', fontsize='small', ncol=4)

# for i in range(arr2.shape[1]):
#     axs[2].step(range(arr2.shape[0]), arr2[:, i], where='mid', label=f'Taxel {i+1}')
# axs[2].set_title('Array z: Step Function Plot')
# axs[2].set_xlabel('Time Step')
# axs[2].set_ylabel('Value')
# axs[2].legend(loc='upper right', fontsize='small', ncol=4)
# plt.tight_layout()
# plt.show()