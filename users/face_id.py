import face_recognition as fr
import cv2
import time
from django.urls import path, include
import os
from django.conf import settings
from django.core.files import File
import numpy as np


def faceLogin(loc, username):
    # reference to webcam
    webcam = cv2.VideoCapture(0)
    s, img = webcam.read()
    if s:  # frame captured without any errors
        loc = str(settings.BASE_DIR)+loc
        # cv2.imwrite("filename.jpg",img)
        face_file = open(loc, 'r')
        user_face_encoding = []
        # fr.face_encodings(user_image)[0]
        user_face_encoding.append(np.array(eval(face_file.read()[7:-2])))
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = fr.face_locations(rgb_small_frame)
        face_encodings = fr.face_encodings(rgb_small_frame, face_locations)
        check = fr.compare_faces(user_face_encoding[0], face_encodings)
        name = 'Unknown'
        if check[0]:
            name = username
            flag = True
        else:
            flag = False
        while True:
            ret, frame = webcam.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # release handle to webcam
        webcam.release()
        cv2.destroyAllWindows()
        return flag


def faceCapture(form_instance):
    webcam = cv2.VideoCapture(0)
    while True:
        directory = settings.MEDIA_ROOT+r'\face_encodes'
        os.chdir(directory)
        ret, frame = webcam.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = fr.face_locations(rgb_small_frame)
        face_encodings = fr.face_encodings(rgb_small_frame, face_locations)
        # Display the resulting image
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if face_encodings != [] and cv2.waitKey(1) & 0xFF == ord('q'):
            break
    face = str(form_instance.user.username)+'.txt'
    # cv2.imwrite(image,frame)
    with open(directory+'\\'+face, 'w') as file:
        file.write(str(face_encodings))
    file = open(directory+'\\'+face, 'rb')
    face_file = File(file)
    form_instance.face_encode.save(face, face_file, save=True)
    webcam.release()
    cv2.destroyAllWindows()
