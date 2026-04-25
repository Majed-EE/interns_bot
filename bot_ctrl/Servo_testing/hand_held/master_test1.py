import cv2
import threading
import time
import serial

# Configure serial connection
# Change 'COM3' to your Arduino port
# Windows: 'COM3', 'COM4', etc.
# Linux/Mac: '/dev/ttyUSB0', '/dev/ttyACM0'













# -----------------------------
# SHARED EVENT VARIABLE
# -----------------------------
event_flag = False
lock = threading.Lock()

# -----------------------------
# THREAD: EVENT LISTENER
# -----------------------------
def event_listener():
    global event_flag
    arduino_port = 'COM4'
    baud_rate = 9600

    try:
        # Open serial connection
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        
        print(f"Connected to Arduino on {arduino_port}")
        print("Reading serial data... Press Ctrl+C to stop\n")
        
        while True:
            # Read one line from serial
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Arduino says: {line}")
                # time.sleep(3)
        # user_input = input("enter record: ")
                if int(line)==1 or int(line)==0:
                    with lock:
                        event_flag = not event_flag
                        print("Event changed:", event_flag)

                
    except serial.SerialException as e:
        print(f"Error: Could not open port {arduino_port}")
        print(f"Details: {e}")
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        ser.close()




# -----------------------------
# START THREAD
# -----------------------------
thread = threading.Thread(target=event_listener, daemon=True)
thread.start()

# -----------------------------
# VIDEO SETUP
# -----------------------------
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = None
recording = False

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Read event safely
    with lock:
        event = event_flag

    # -----------------------------
    # START RECORDING
    # -----------------------------
    if event and not recording:
        print("Recording STARTED")
        h, w = frame.shape[:2]
        video_writer = cv2.VideoWriter("Arduino_test.mp4", fourcc, 30, (w, h))
        recording = True

    # -----------------------------
    # STOP RECORDING
    # -----------------------------
    if not event and recording:
        print("Recording STOPPED")
        recording = False
        video_writer.release()
        video_writer = None

    # -----------------------------
    # WRITE FRAME
    # -----------------------------
    if recording and video_writer is not None:
        video_writer.write(frame)

    # Display
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup
if video_writer is not None:
    video_writer.release()

cap.release()
cv2.destroyAllWindows()


