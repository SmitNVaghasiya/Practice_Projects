import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import urllib.request

# Get camera and display video
camera = cv2.VideoCapture(0)
WindowName = 'Cascade Classifier'
cv2.namedWindow(WindowName, cv2.WINDOW_AUTOSIZE)

# Trained cascade classifiers
eye =cv2.data.haarcascades + "haarcascade_eye.xml"
face=cv2.data.haarcascades+"haarcascade_frontalface_default.xml"

# Cascade Classifier
cascade=cv2.CascadeClassifier(face)

start = time.time()
while time.time()-start<=20.0:
    # read frame
    ret, pixels = camera.read()        
    # convert to gray scale and identify faces
    gray = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    detect = cascade.detectMultiScale(gray,scaleFactor=1.1,
                                           minNeighbors=3,\
                                           minSize=(30, 30))
    # display identified faces on original image
    for (x, y, w, h) in detect:
        cv2.rectangle(pixels,(x,y),(x+w,y+h),(255,255,0),3)
    cv2.imshow(WindowName,pixels)        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and video file
camera.release()
cv2.destroyAllWindows()