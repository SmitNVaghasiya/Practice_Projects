import cv2

image = cv2.imread("./src/girl_1.webp")

if image is None:
    print("Error: while loading the image")
else:
    # width, height, channels = image.shape # this gets the original size of the image
    width, height = 600,600
    image = cv2.resize(image, (width, height))
    cv2.imshow("Girl Photo",image)

cv2.waitKey(0)
cv2.destroyAllWindows()