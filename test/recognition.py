# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 10:35:21 2021

@author: Annie
"""

import cv2
import face_recognition
import numpy as np

#Load the image specified
specify_img = cv2.imread('image/image06-target.jpg')
specify_img_encoding = face_recognition.face_encodings(specify_img)[0]
known_encodings = [specify_img_encoding]
known_flag = ["known"]

def locate(frame):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame)
    return face_locations, face_encodings

def face_recog(frame):
    face_locations ,face_encodings = locate(frame)
    face_flags = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        flag = "unknown"
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            flag = known_flag[best_match_index]
        face_flags.append(flag)
    return face_flags

# @return left, top, right, bottom
def get_face(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    faces,ens = locate(frame)               ##########
    res = []
    for top, right, bottom, left in faces:
        left, top = max(0, left), max(0, top)
        right, bottom = min(width, right), min(height, bottom)
        res.append([left, top, right, bottom])
    return res

# left-top coordinate: (left: x-axis, top: y-axis), right-bottom coordinates: (right: x-axis, bottom: y-axis)
def mosaic_video(frame, left, top, right, bottom):
    frame[top:bottom, left:right] = cv2.GaussianBlur(
        frame[top:bottom, left:right], (59, 59), 0)
    
img = cv2.imread('image/image06.jpg')
faces_location = get_face(img)
face_flags = face_recog(img)
for (left, top, right, bottom), flag in zip(faces_location, face_flags):
    if flag == 'known':
        continue
    mosaic_video(img,left, top, right, bottom)
cv2.imwrite('image/image06-result.jpg', img)
