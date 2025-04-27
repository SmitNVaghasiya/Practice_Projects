import cv2

# Open the default camera
cam = cv2.VideoCapture(0)

# Set the desired frame width and height
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 24)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 24)

# Get the actual frame size
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Write the frame to the output file
    out.write(frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
out.release()
cv2.destroyAllWindows()
