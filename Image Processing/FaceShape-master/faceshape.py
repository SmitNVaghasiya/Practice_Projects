#importing the libraries
import numpy as np
import cv2
import dlib
from sklearn.cluster import KMeans

# Load the paths for required files
imagepath = "shahrukh_test.jpg"  # Path to the image
face_cascade_path = "haarcascade_frontalface_default.xml"  # Haarcascade file path
predictor_path = "shape_predictor_68_face_landmarks.dat"  # Dlib shape predictor file path

# Create the Haar cascade for detecting faces
faceCascade = cv2.CascadeClassifier(face_cascade_path)

# Create the Dlib landmark predictor
predictor = dlib.shape_predictor(predictor_path)

# Read and preprocess the image
image = cv2.imread(imagepath)
if image is None:
    raise ValueError("Image not found or path is incorrect.")

# Resize the image to 500x500
image = cv2.resize(image, (500, 500))
original = image.copy()  # Create a copy for future use

# Convert the image to grayscale (required for both Haar cascade and dlib)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.05,
    minNeighbors=5,
    minSize=(100, 100),
    flags=cv2.CASCADE_SCALE_IMAGE
)

print(f"Found {len(faces)} face(s)!")

# Process each detected face
for (x, y, w, h) in faces:
    # Draw a rectangle around the face
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Convert OpenCV rectangle coordinates to Dlib rectangle
    dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

    # Detect landmarks (pass the grayscale image)
    detected_landmarks = predictor(gray, dlib_rect).parts()
    landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])

    # Analyze forehead region
    forehead = original[y:y + int(0.25 * h), x:x + w]
    rows, cols, bands = forehead.shape
    X = forehead.reshape(rows * cols, bands)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_kmeans = kmeans.fit_predict(X)

    for i in range(rows):
        for j in range(cols):
            if y_kmeans[i * cols + j]:
                forehead[i, j] = [255, 255, 255]
            else:
                forehead[i, j] = [0, 0, 0]

    # Calculate midpoint of the forehead
    forehead_mid = [int(cols / 2), int(rows / 2)]

    # Detect changes in pixel values for forehead length
    pixel_value = forehead[forehead_mid[1], forehead_mid[0]]
    left = right = None
    for i in range(cols):
        if forehead[forehead_mid[1], forehead_mid[0] - i].all() != pixel_value.all():
            left = [forehead_mid[0] - i, forehead_mid[1]]
            break
    for i in range(cols):
        if forehead[forehead_mid[1], forehead_mid[0] + i].all() != pixel_value.all():
            right = [forehead_mid[0] + i, forehead_mid[1]]
            break

    # Drawing lines on the detected landmarks
    line1 = np.linalg.norm(np.subtract(right, left))
    cv2.line(image, tuple(left), tuple(right), (0, 255, 0), 2)
    cv2.circle(image, tuple(left), 5, (255, 0, 0), -1)
    cv2.circle(image, tuple(right), 5, (255, 0, 0), -1)

    # Other lines based on landmarks
    # Example: Line connecting landmarks[1] and landmarks[15]
    linepointleft = (landmarks[1, 0], landmarks[1, 1])
    linepointright = (landmarks[15, 0], landmarks[15, 1])
    line2 = np.linalg.norm(np.subtract(linepointright, linepointleft))
    cv2.line(image, linepointleft, linepointright, (0, 255, 0), 2)

    # More lines and shape analysis
    # ...

# Show the results
cv2.imshow("Detected Features", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
