#!/usr/bin/env python3
# original code
import websocket
import json
import time
from time import sleep
import threading
import numpy as np
import paho.mqtt.client as mqtt
import json
# from datetime import datetime
from matplotlib import pyplot as plt
import serial 
#############################################
################## Arduino Configuration ##################
SERIAL_PORT = "COM10"
BAUD_RATE = 9600
# Arduino serial setup
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
LS_O_Th=150 # left servo open angle
LS_C_Th=130 # left servo close angle
RS_O_Th=30 # right servo open angle
RS_C_Th=50 # right servo close angle
open_command = f"{LS_O_Th},{RS_O_Th}\n"
close_command = f"{LS_C_Th},{RS_C_Th}\n"
time.sleep(1)
arduino.write(open_command.encode())
print("starting arduino at open position ..........")
time.sleep(2)


# open is 150,30
# close is 130,50

# ----------------------------






# custom library imports
import MyXela 
feature_extractor = MyXela.XelaTactileFeatureExtractor()


global np_sample
ip_xela ='10.10.8.55'# xela ip, check from server 10.50.49.23
#"192.168.0.103"  # your computer IP on the network
port = 5000  # the port the server is running on
print(f"running client connecting to ws://{ip_xela}:{port}")
lastmessage = {"message": "No message"}  # default message you will overwrite when you get update


def on_message(wsapp, message):
    global lastmessage  # globalize to overwrite original
    global crnt_pckt_num
    try:
        data = json.loads(message)
    except Exception:
        pass
    else:
        try:
            if data["message"] == "Welcome":  # get the Welcome Message with details, print if you like
                print(data)
            else:
                lastmessage = data
        except Exception:
            pass  # ignore message as it's probably invalid

def threader(target, args=False, **targs):
    # args is tuple of arguments for threaded function other key-value pairs will be sent to Thread
    if args:
        targs["args"] = (args,)
    thr = threading.Thread(target=target, **targs)
    thr.daemon = True
    thr.start()

    if not (thr.is_alive()):
        print("thread has ended")
        

# Add plotting functionality to visualize the data for 16 taxels over time
def plot_all_taxels(np_sample_x, np_sample_y, np_sample_z):
    t_sample, t_taxel = np_sample_x.shape
    time_steps = np.arange(t_sample-1)

    plt.figure(figsize=(12, 16))
    t_data=[np_sample_x,np_sample_y,np_sample_z]
    axs=["X","Y","Z"]
    # Plot all X values for all taxels
    # for data in range(len(t_data)):
    data=2
    for taxel in range(t_taxel):
        line_style = '-' if taxel < 8 else '--'  # Solid line for first 8 taxels, dotted for the rest
        plt.plot(time_steps, t_data[data][1:, taxel], label=f"Taxel {taxel + 1}", linestyle=line_style)
        # plt.plot(time_steps, np_sample_x[1:, taxel], label=f"Taxel {taxel + 1}")
    plt.title(f"All {axs[data]} Values for All Taxels")
    plt.xlabel("Time Step")
    plt.ylabel(f"{axs[data]} Values")
    plt.legend()
    plt.grid(True)
    plt.show()


def mesreader():  # this is your app reading the last valid message you received
    global data_sample_x,data_sample_y,data_sample_z

    crnt_pckt_num=0
    t_sample = 10
    t_taxel=16
    data_sample_x=np.zeros((t_sample,t_taxel))
    data_sample_y=np.zeros((t_sample,t_taxel))
    data_sample_z=np.zeros((t_sample,t_taxel))
    
    # while True:  # to run forever,
    for sample in range(t_sample):
        print(f"*********************** Running iteration to calculate mean {sample} ****************")
        try:
            if lastmessage["message"] != "No message":
                
                feature_extractor.extract_force(lastmessage)

                
                data_sample_z[sample]=feature_extractor.fz_touch
                data_sample_x[sample]=feature_extractor.fx_touch
                data_sample_y[sample]=feature_extractor.fy_touch
                # v_sample+=0
            t=0.1
            # print(f"--- sleeping for {t} seconds ---")
            sleep(t)  # your calculations and processes here (sleep is used as simulation here)
        except KeyboardInterrupt:
            # client.disconnect()
            print("breaking")
            break  # break on KeyboardInterrupt
        except Exception as e:
            print("Exception: {}: {}".format(type(e).__name__, e))

    total_touch_sample= 20
    
    new_z_mean=np.mean(data_sample_z,axis=0)
    threshold_val=np.asarray( ([0.1]*t_taxel) )
    for episode in range(5):
        touch_data_sample_z=np.zeros((total_touch_sample,t_taxel))
        crnt_LS_th=LS_O_Th
        crnt_RS_th=RS_O_Th
        print(f"*********************** Running episode {episode} ****************")
        for touch_sample in range(0,total_touch_sample):
            print(f"*********************** Running iteration for {touch_sample} ****************")
            try:
                if lastmessage["message"] != "No message":
                    
                    cmd_arduino = f"{crnt_LS_th},{RS_O_Th}\n"
                    arduino.write(cmd_arduino.encode())
                    feature_extractor.extract_force(lastmessage)

                    
                    touch_data_sample_z[touch_sample]=feature_extractor.fz_touch-new_z_mean

                    touch_indices=np.where(touch_data_sample_z[touch_sample]>threshold_val)[0]
                    print(f"touch_indices: {touch_indices}")
                    print("Corresponding thresholds:", touch_data_sample_z[touch_sample][touch_indices])
                    if len(touch_indices)>0:
                        print("Touch detected! Closing gripper.")
                        print(f"saving angle is {crnt_LS_th}")
                          # wait for the gripper to close
                        arduino.write(open_command.encode())
                        time.sleep(2.5)
                        break
                        
                    else: crnt_LS_th-=1
                    # v_sample+=0
                t=1.5
                print(f"--- sleeping for {t} seconds ---")
                sleep(t)  # your calculations and processes here (sleep is used as simulation here)
            except KeyboardInterrupt:
                # client.disconnect()
                print("breaking")
                break  # break on KeyboardInterrupt
            except Exception as e:
                print("Exception: {}: {}".format(type(e).__name__, e))







try:  # try to close the app once you press CTRL + C
    threader(mesreader, name="Receiver")  # start you main app
    websocket.setdefaulttimeout(1)  # you should avoid increasing it.
    wsapp = websocket.WebSocketApp("ws://{}:{}".format(ip_xela, port), on_message=on_message)  # set up WebSockets
    wsapp.run_forever()  # Run until connection dies
    # plot_all_taxels(data_sample_x,data_sample_y,data_sample_z)
except Exception as e:
    print("Exception: {}: {}".format(type(e).__name__, e))

    exit()