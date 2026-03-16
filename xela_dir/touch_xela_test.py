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
data_Dict= {'message': 9163, 'time': 1771925442.3679874, 'sensors': 1, 'type': 'welcome', 'version': '1.7.7_161703', 
'1': {'time': 1771925442.3669958, 'sensor': '1', 
'data': '7FF3,7F6A,8C69,7F70,7F98,8C40,7FBB,7FC9,8B8A,8037,7FA2,8B6B,7FEF,7F5A,8BCF,801C,7F54,8AEA,8005,7F77,8C00,80B8,7FBE,8BBA,7E31,7F50,8CAD,7EC4,7F88,8D0E,7F89,7FFC,8D1D,7FB2,80E2,8CFC,7E59,7FC2,8E4A,7F23,7FF2,8BE2,7FC4,8023,8C69,7F11,7FDA,8C45', 
'model': 'uSPa44', 'taxels': 16, 'special': [[32755, 32618, 35945, 305.35619134449723, 0, 0, 142, -0.050808655502748934, 0, 0, -142, 325.719848771276], [32624, 32664, 35904, 305.25907582507256, 0, 0, 140, 0.007075825072547559, 0, 0, -140, 321.33022729328064], [32699, 32713, 35722, 306.0069897813793, 0, 0, 155, 0.09198978137925451, 0, 0, -155, 355.13593811834426], [32823, 32674, 35691, 307.48060972886685, 0, 0, 184, 0.016609728866853857, 0, 0, -184, 421.7435597447828], [32751, 32602, 35791, 306.464681930365, 0, 0, 164, -0.09231806963504141, 0, 0, -164, 375.8236232524979], [32796, 32596, 35562, 306.93732108167075, 0, 0, 173, -0.08467891832924579, 0, 0, -173, 397.1869128915188], [32773, 32631, 35840, 307.5453126039594, 0, 0, 185, -0.05168739604056327, 0, 0, -185, 424.6681296989667], [32952, 32702, 35770, 308.01956018073696, 0, 0, 195, -0.08643981926303468, 0, 0, -195, 446.1041201693116], [32305, 32592, 36013, 305.31223881638675, 0, 0, 141, -0.04976118361327053, 0, 0, -141, 323.73319450068226], [32452, 32648, 36110, 304.0595015722252, 0, 0, 116, -0.1084984277748049, 0, 0, -116, 267.10947106458013], [32649, 32764, 36125, 306.0404251298301, 0, 0, 156, 0.03642512983009283, 0, 0, -156, 356.6472158683221], [32690, 32994, 36092, 306.0886932655653, 0, 0, 157, 0.10669326556529768, 0, 0, -157, 358.82893560355376], [32345, 32706, 36426, 305.4025305891903, 0, 0, 143, 0.017530589190300816, 0, 0, -143, 327.8143826314022], [32547, 32754, 35810, 308.3829957964756, 0, 0, 202, -0.055004203524390505, 0, 0, -202, 462.5314100006981], [32708, 32803, 35945, 313.86726335818656, 0, 0, 310, 0.12026335818654843, 0, 0, -310, 710.4203037900337], [32529, 32730, 35909, 329.54498518101843, 0, 0, 621, -0.04301481898158954, 0, 0, -621, 1419.0533301820342]], 'temp': [305.35619134449723, 305.25907582507256, 306.0069897813793, 307.48060972886685, 306.464681930365, 306.93732108167075, 307.5453126039594, 308.01956018073696, 305.31223881638675, 304.0595015722252, 306.0404251298301, 306.0886932655653, 305.4025305891903, 308.3829957964756, 313.86726335818656, 329.54498518101843], 'ups': [78.89806540690975, 78.87514221507621, 77.34465574072793, 78.55222670245023, 79.22166670759049, 77.65130168509995, 76.75556478686502, 78.2881631799788, 79.22121781044949, 78.87506805161297, 78.90749077692095, 79.83121318851572, 79.53729865854537, 79.21261493164772, 80.86028802220895, 78.57798027637061]}, 'complete': 1771925442.3679874}
feature_extractor.extract_force(data_Dict)
print(feature_extractor.fz_touch)

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
    np_sample_x=(np_sample_x-np.mean(np_sample_x,axis=0))/np.mean(np_sample_x,axis=0)
    np_sample_y=(np_sample_y-np.mean(np_sample_y,axis=0))/np.mean(np_sample_y,axis=0)
    np_sample_z=(np_sample_z-np.mean(np_sample_z,axis=0))/np.mean(np_sample_z,axis=0)
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
        print(f"*********************** Running iteration {sample} ****************")
        try:
            if lastmessage["message"] != "No message":
                
                feature_extractor.extract_force(lastmessage)
                # print(f"Extracted features: {feature_extractor.fz_norm.shape, feature_extractor.fy_norm.shape, feature_extractor.fz_norm.shape}")
                print(f"touch is: {(feature_extractor.fz_touch)}")
                # if feature_extractor.fz_raw.any():
                
                data_sample_z[sample]=feature_extractor.fz_touch
                data_sample_x[sample]=feature_extractor.fx_touch
                data_sample_y[sample]=feature_extractor.fy_touch
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
    update_mean= Fakse
    if update_mean:
        np.save('xela_Dataset/x_mean.npy', np_sample_x_mean)
        np.save('xela_Dataset/y_mean.npy', np_sample_y_mean)
        np.save('xela_Dataset/z_mean.npy', np_sample_z_mean)

    print(f"mean x: {np_sample_x_mean}")
    print(f"mean y: {np_sample_y_mean}")
    print(f"mean z: {np_sample_z_mean}")
    print(f"shape x: {np_sample_x_mean.shape}")
    




try:  # try to close the app once you press CTRL + C
    threader(mesreader, name="Receiver")  # start you main app
    websocket.setdefaulttimeout(1)  # you should avoid increasing it.
    wsapp = websocket.WebSocketApp("ws://{}:{}".format(ip_xela, port), on_message=on_message)  # set up WebSockets
    wsapp.run_forever()  # Run until connection dies
    # plot_all_taxels(data_sample_x,data_sample_y,data_sample_z)
except Exception as e:
    print("Exception: {}: {}".format(type(e).__name__, e))

    exit()