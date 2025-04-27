import cv2
import face_recognition
# CV2.imshow is disabled on the google colab due to crashing issue

hritik_train = face_recognition.load_image_file("hritik_train.jpg")
hritik_train = cv2.cvtColor(hritik_train, cv2.COLOR_BGR2RGB)
hritik_test = face_recognition.load_image_file("hritik_test.jpg")
hritik_test = cv2.cvtColor(hritik_test, cv2.COLOR_BGR2RGB)
shahrukh_test = face_recognition.load_image_file("shahrukh_test.jpg")
shahrukh_test = cv2.cvtColor(shahrukh_test, cv2.COLOR_BGR2RGB)

face_loc = face_recognition.face_locations(hritik_train)
encode_train = face_recognition.face_encodings(hritik_train)[0]
cv2.rectangle(hritik_train, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (255, 0, 255), 2)
# print(face_loc)

face_loc_test = face_recognition.face_locations(hritik_test)
encode_test = face_recognition.face_encodings(hritik_test)[0]
cv2.rectangle(hritik_test, (face_loc_test[3], face_loc_test[0]), (face_loc_test[1], face_loc_test[2]), (255, 255, 0), 2)
# print(face_loc_test)

# face_loc_test = face_recognition.face_locations(shahrukh_test)[0]
# encode_test = face_recognition.face_encodings(shahrukh_test)[0]
# cv2.rectangle(shahrukh_test, (face_loc_test[3], face_loc_test[0]), (face_loc_test[1], face_loc_test[2]), (255, 255, 0), 2)

result = face_recognition.compare_faces([encode_train], encode_test)
face_dis = face_recognition.face_distance([encode_train], encode_test)
print(result, face_dis)
cv2.putText(hritik_test, f'{result} {face_dis[0],1}', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (240,10,30),2)

# cv2.imshow("Hritik Train",hritik_train) #use this to run in the normal system
# cv2.imshow("Hritik Test",hritik_test)

# cv2_imshow(hritik_train)
# cv2_imshow(hritik_test)
# cv2_imshow(shahrukh_test)
cv2.waitKey(0)