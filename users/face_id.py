import face_recognition as fr
import cv2
import time
from django.urls import path, include
import os
from django.conf import settings
from django.core.files import File
import numpy as np


def faceLogin(user):
    loc = str(settings.BASE_DIR)+user.profile.face_encode.url
    face_file = open(loc, 'r')
    user_face_encoding = []
    user_face_encoding.append(np.array(eval(face_file.read()[7:-2])))
    image = fr.load_image_file(user.profile.face.path)
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)
    check = fr.compare_faces(user_face_encoding[0], face_encodings)
    if check[0]:
        return True
    else:
        return False


def faceCapture(request):
    directory = settings.MEDIA_ROOT+r'/face_encodes'
    os.chdir(directory)
    image = fr.load_image_file(request.user.profile.face.path)
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)
    if face_encodings != []:
        face = str(request.user.username)+'.txt'
        with open(directory+'/'+face, 'w') as file:
            file.write(str(face_encodings))
        file = open(directory+'/'+face, 'rb')
        face_file = File(file)
        request.user.profile.face_encode.save(face, face_file, save=True)
        return True
    return False
