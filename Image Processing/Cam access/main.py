import cv2 

cam = cv2.VideoCapture(0)

# frame_counts = cam.get(cv2.CAP_PROP_FRAME_COUNT)
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_type = cam.get(cv2.CAP_PROP_FRAME_TYPE)


# print("frame_counts: ",frame_counts)
# print("frame_height:",frame_height)
# print("frame_width:",frame_width)
# print("frame_type:",frame_type)

fps_video = 2.0  
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps_video, (frame_width, frame_height))

while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Write the frame to the output video file
    out.write(frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break
frame_type = cam.get(cv2.CAP_PROP_FRAME_TYPE)
frame_counts = cam.get(cv2.CAP_PROP_FRAME_COUNT)

print("frame_counts: ",frame_counts)
print("frame_type:",frame_type)
# Release the capture and writer objects
cam.release()
out.release()
cv2.destroyAllWindows()