import cv2

# Get the list of available camera devices
camera_list = []
for i in range(10):  # You can adjust the range as needed
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        camera_list.append(f"Camera {i}")
        cap.release()

# Print the list of available cameras
for camera in camera_list:
    print(camera)