
import time
import numpy as np
from bidirectional_control_DHG import DHG_Bidirectional
import paho.mqtt.client as mqtt
import json
import logging
logging.basicConfig(filename='pinch.log', level=logging.INFO, format='%(asctime)s %(message)s')
from datetime import datetime
now=datetime.now
print("datetime hours: {}, min: {}, sec: {}".format(now.hour,now.minute,now.seconds)

# random_stiff=round(np.random.uniform(),2)
N=100

global stiffness_value, set_point_value, dhg_device, start_time
start_time=1773228300
stiffness_value=0.0 
set_point_value=0.5

def call_stiff_changer(stiffness, set_point):
    global stiffness_value, set_point_value, dhg_device,BiDirectional_
    # random_stiff=round(np.random.uniform(),2)
    stiffness_value= stiffness
    #random_stiff
    
    set_point_value=set_point
    print("stiffness_value updated to: {}".format(stiffness_value))
    print("set_point_value updated to: {}".format(set_point_value))
    if BiDirectional_:
        print("setting stiffness: {} and set_point: {} to command write worker".format(stiffness_value, set_point_value))
        dhg_device.test_write_worker([stiffness_value]*5, [set_point_value]*5) # update impedance control
    


###########################################3 MQTT Block #####################################
# MQTT Settings
BROKER = "54.235.47.84" #"10.10.7.199"     # Change to IP if remote
PORT = 1883
TOPIC_PUB = "UE/to_toy_arm"
TOPIC_SUB = "CAS/haptic_feedback" # tactile feedback stream
MQTT_ = True


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connected to broker")
        client.subscribe(TOPIC_SUB)
        print(" Subscribed to: " + TOPIC_SUB)
    else:
        print(" Connection failed")

# When message received
def on_message(client, userdata, msg):
    print("Message received")
    data=dict(json.loads(msg.payload.decode()))
    print("Topic:", msg.topic)
    print("Message:", data)
    if msg.topic=="CAS/haptic_feedback": 
        print("updating stiffness {}".format(data["stiffness"]))
        packet_info=list(format(data["packet_info"]))
        print("time stamp: {}".format(data["packet_info"]))
        # datetime.now()
        # print("datetime hours: {}, min: {}, sec: {}".format(now.hour,now.minute,now.seconds)
        # now_min=now.minute*60+now.seconds
        now_min=time.time()-start_time
        sent_min=data["packet_info"][0]
        latency=now_min-sent_min
        print("sent time: {}, now_time: {}".format(now_min,sent_min,latency)))

        # print("updating set_point {}".format(data["arm_shape"]))
        logging.info("updating stiffness {}".format(data["stiffness"]))
        # logging.info("updating set_point {}".format(data["arm_shape"]))
        set_point=0.3 # 0 means open, 1 means close
        call_stiff_changer(data["stiffness"], 0.2)
        
    #test_write_worker


# Create client

client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message



# Connect to broker
if MQTT_:
    client.connect(BROKER, PORT, 60)
    client.loop_start()


####################################### MQTT end ############################################




##################################### DHG Controler block ####################################

import time as T

print("Iteration 1-> ")

dhg_device=DHG_Bidirectional()
dhg_device.connect()

print("Device connected: ", dhg_device.is_dhg_connected)
logging.info("Device connected: ", dhg_device.is_dhg_connected)
# once device connected, for Feedback direction, set stiffness and set point

############################################################################



###################################### Forward control -> Frame Read #####################################3

dhg_device.set_frame_read_worker()

dhg_device.publish_joint_state()
frd_channel = dhg_device.is_frame_read_connected
print("Forward channel activated: {}".format(dhg_device.is_frame_read_connected))

########################################################################################


######################################## backward channel publisher ###########################################
dhg_device.set_command_write_worker() # for haptic feedback


BiDirectional_= (dhg_device.is_command_write_connected and dhg_device.is_frame_read_connected) and MQTT_
print("Bidirectional control with *MQTT*: {}".format(BiDirectional_))

dhg_device.test_write_worker([0]*5, [0]*5)


t=5

for x in range(t):
    print("starting in {} seconds".format(t-x))    
    time.sleep(1)

######################################################## main loop ###############################

if BiDirectional_:
    print("Both backward and forward channels are active")
    print("starting loop for {} iterations".format(N))
    for itr in range(N):
        dhg_device.publish_joint_state() # have to do it everytime else it will feeze
        valset=dhg_device.Joint.position
        print("inside loop demo iteration: {0}".format(itr))
        
        print("index: {0}".format(valset[4])) # index
        # print("middle: {0}".format(valset[6])) # middle   
        # print("ring: {0}".format(valset[8])) # ring
        print("thumb: {0}".format(valset[2])) # thumb
        # print("pinky: {0}".format(valset[10])) # pinky
        t=1
        T.sleep(t)
        # print("sleeping for {} seconds".format(t))
        # print("hf received: ")

        # stiffness, set_point =  np.round(np.random.uniform(0, 1, 2), 2)
        # print("setting stiffness: {} and set_point: {} to command write worker")
        # dhg_device.test_write_worker([stiffness]*5, [set_point]*5) # update impedance control
        if MQTT_:
            data_finger={"Index": round(valset[4],2), "Middle": round(valset[6],2), "Ring": round(valset[8],2), "Pinky": round(valset[10],2), "Thumb": round(valset[2],2)}
            # data_finger=[valset[4],valset[6]]
            print("publsing: {}".format(data_finger))  # publish forward channel control
            payload=json.dumps(data_finger) #.tobytes()

        
            client.publish(TOPIC_PUB, payload)
        
        T.sleep(0.5)

    dhg_device.set_rest()
else: print("biDirectial with mqtt is {}".format(BiDirectional))

if MQTT_:
    client.loop_stop()
    print("closing mqtt connection")

print("resting")
print("ending")
