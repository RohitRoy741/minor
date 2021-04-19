import face_recognition as fr
import cv2
from django.urls import path, include
from django.contrib import messages
import os
from django.conf import settings
from django.core.files import File
import numpy as np


def faceLogin(user):
    #oc = str(settings.BASE_DIR)+user.profile.face_encode.url
    #face_file = open(loc, 'r')
    user_face_encoding = []
    #read user encoding from file and eval
    #user_face_encoding.append(np.array(eval(face_file.read()[7:-2])))
    user_face_encoding.append(np.array(eval(user.profile.face_encode[7:-2])))
    #load temp user face image
    image = fr.load_image_file(user.profile.face.path)
    try:
        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)
        check = fr.compare_faces(user_face_encoding[0], face_encodings)
    except:
        return False
    if check[0]:
        return True
    else:
        return False

def faceCapture(request):
    #directory = settings.MEDIA_ROOT+r'\face_encodes'
    #change directory to local media to load face image
    #os.chdir(directory)
    image = fr.load_image_file(request.user.profile.face.path)
    try:
        face_locations = fr.face_locations(image)
    except:
        messages.error(request,'Error detecting face! Try again')
        return False
    face_encodings = fr.face_encodings(image, face_locations)
    if face_encodings != [] :
        #face = str(request.user.username)+'.txt'
        #write face encodes as string in file
        #with open(directory+'\\'+face, 'w') as file:
            #file.write(str(face_encodings))
        #file = open(directory+'\\'+face, 'rb')
        #convert to django File object to save to model
        #face_file = File(file)
        #request.user.profile.face_encode.save(face, face_file, save=True)
        request.user.profile.face_encode=str(face_encodings)
        request.user.save()
        return True
    return False
