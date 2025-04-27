import cv2
import dlib
import numpy as np

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Load face image
face_img = cv2.imread("girl_1.webp")
gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

# Detect face
faces = detector(gray)
for face in faces:
    landmarks = predictor(gray, face)
    face_features = np.array([[p.x, p.y] for p in landmarks.parts()])  # Store keypoints

# Save face features
np.save("face_features.npy", face_features)