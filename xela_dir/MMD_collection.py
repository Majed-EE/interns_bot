import websocket
import json
from time import sleep
import threading
import time as t
import pyrealsense2 as rs
import numpy as np
import cv2
import os


ip = "10.10.5.245"
#"192.168.0.103"  # your computer IP on the network
port = 5000  # the port the server is running on
import MyXela
############################## realsense ##########
# Create folders
rgb_folder = "dataset/rgb"
depth_folder = "dataset/depth"

os.makedirs(rgb_folder, exist_ok=True)
os.makedirs(depth_folder, exist_ok=True)

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()

# Enable streams
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start camera
pipeline.start(config)

img_count = 0

#######################################################

FE=MyXela.XelaTactileFeatureExtractor()
csv_saver=MyXela.XelaTactileCSVLogger()

lastmessage = {"message": "No message"}  # default message you will overwrite when you get update

def on_message(wsapp, message):
    global lastmessage  # globalize to overwrite original
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

def mesreader():  #- this is your app reading the last valid message you received
    img_count=0
    t_exp=4.9
    t_start=t.time()
    while True:  # to run forever # main while loop 
        try:
            if lastmessage["message"] != "No message":
                print("I received: {}\n---".format(str(lastmessage)))
                FE.extract_force(lastmessage)
                csv_saver.log_forces(FE.fx_raw%1000,FE.fy_raw%1000,FE.fz_raw%1000)
                t_end=t.time()
                print(f"time: {round((t_end-t_start),2)}")
                if t_end-t_start>=t_exp:
                    break
                ########################## image setup ##############
                frames = pipeline.wait_for_frames()

                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()

                # Convert to numpy arrays
                rgb_image = np.asanyarray(color_frame.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())

                # Show images
                depth_colormap = cv2.applyColorMap(
                    cv2.convertScaleAbs(depth_image, alpha=0.03),
                    cv2.COLORMAP_JET
                )

                combined = np.hstack((rgb_image, depth_colormap))
                cv2.imshow("RGB | Depth", combined)
                key = cv2.waitKey(1)

                rgb_name = f"{rgb_folder}/rgb_frame00{img_count}.jpg"
                depth_name = f"{depth_folder}/depth_frame00{img_count}.png"
                
                cv2.imwrite(rgb_name, rgb_image)
                cv2.imwrite(depth_name, depth_image)

                print(f"Saved: {rgb_name} & {depth_name}")
                img_count += 1
                


                #################################### end image setup ##########
            sleep(0.5)  # your calculations and processes here (sleep is used as simulation here)
        
        except KeyboardInterrupt:
            break  # break on KeyboardInterrupt
        except Exception as e:
            print("Exception: {}: {}".format(type(e).__name__, e))
        

try:  # try to close the app once you press CTRL + C
    threader(mesreader, name="Receiver")  # start you main app
    websocket.setdefaulttimeout(1)  # you should avoid increasing it.
    wsapp = websocket.WebSocketApp("ws://{}:{}".format(ip, port), on_message=on_message)  # set up WebSockets
    wsapp.run_forever()  # Run until connection dies
except Exception:
    exit()