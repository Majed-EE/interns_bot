import pyrealsense2 as rs
import numpy as np
import cv2
import os

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

print("Press 's' to save RGB + Depth")
print("Press 'q' to quit")

try:
    while True:
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

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

        if key == ord('s'):
            rgb_name = f"{rgb_folder}/rgb_{img_count}.jpg"
            depth_name = f"{depth_folder}/depth_{img_count}.png"

            cv2.imwrite(rgb_name, rgb_image)
            cv2.imwrite(depth_name, depth_image)

            print(f"Saved: {rgb_name} & {depth_name}")
            img_count += 1

        elif key == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()