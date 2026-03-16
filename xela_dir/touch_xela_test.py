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
from datetime import datetime
from matplotlib import pyplot as plt
#############################################


# custom library imports
import MyXela 
feature_extractor = MyXela.XelaTactileFeatureExtractor()


global np_sample
ip_xela = "10.50.49.23" # xela ip, check from server 10.50.49.23
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
    # np_sample_x=(np_sample_x-np.mean(np_sample_x,axis=0))/np.mean(np_sample_x,axis=0)
    # np_sample_y=(np_sample_y-np.mean(np_sample_y,axis=0))/np.mean(np_sample_y,axis=0)
    # np_sample_z=(np_sample_z-np.mean(np_sample_z,axis=0))/np.mean(np_sample_z,axis=0)
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
                # print(f"Extracted features: {feature_extractor.fz_norm.shape, feature_extractor.fy_norm.shape, feature_extractor.fz_norm.shape}")
                # print(f"touch is: {(feature_extractor.fz_touch)}")
                # if feature_extractor.fz_raw.any():
                
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

    total_touch_sample= 50
    new_z_mean=np.mean(data_sample_z,axis=0)
    threshold_val=np.asarray( ([0.04]*t_taxel) )
    touch_data_sample_z=np.zeros((total_touch_sample,t_taxel))


    for touch_sample in range(0,total_touch_sample):
        print(f"*********************** Running iteration for {touch_sample} ****************")
        try:
            if lastmessage["message"] != "No message":
                
                feature_extractor.extract_force(lastmessage)
                # print(f"Extracted features: {feature_extractor.fz_norm.shape, feature_extractor.fy_norm.shape, feature_extractor.fz_norm.shape}")
                # print(f"touch is: {(feature_extractor.fz_touch)}")
                # if feature_extractor.fz_raw.any():
                
                touch_data_sample_z[touch_sample]=feature_extractor.fz_touch-new_z_mean
                # data_sample_x[touch_sample]=feature_extractor.fx_touch
                # data_sample_y[touch_sample]=feature_extractor.fy_touch
                # print(f"touch is: {data_sample_z[touch_sample]}")
                touch_indices=np.where(touch_data_sample_z[touch_sample]>threshold_val)[0]
                print(f"touch_indices: {touch_indices}")
                print("Corresponding thresholds:", touch_data_sample_z[touch_sample][touch_indices])
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

    
    np_sample_x_mean=np.mean(data_sample_x,axis=0)
    np_sample_y_mean=np.mean(data_sample_y,axis=0)
    np_sample_z_mean=np.mean(data_sample_z,axis=0)
    update_mean= False
    if update_mean:
        np.save('xela_Dataset/x_mean.npy', np_sample_x_mean)
        np.save('xela_Dataset/y_mean.npy', np_sample_y_mean)
        np.save('xela_Dataset/z_mean.npy', np_sample_z_mean)
    print("################### program ending ####################")

    # print(f"mean x: {np_sample_x_mean}")
    # print(f"mean y: {np_sample_y_mean}")
    # print(f"mean z: {np_sample_z_mean}")
    # print(f"shape x: {np_sample_x_mean.shape}")
    




try:  # try to close the app once you press CTRL + C
    threader(mesreader, name="Receiver")  # start you main app
    websocket.setdefaulttimeout(1)  # you should avoid increasing it.
    wsapp = websocket.WebSocketApp("ws://{}:{}".format(ip_xela, port), on_message=on_message)  # set up WebSockets
    wsapp.run_forever()  # Run until connection dies
    # plot_all_taxels(data_sample_x,data_sample_y,data_sample_z)
except Exception as e:
    print("Exception: {}: {}".format(type(e).__name__, e))

    exit()