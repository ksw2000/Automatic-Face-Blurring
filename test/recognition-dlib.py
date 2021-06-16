# 2021/06/16
# author: Kashiwa
# Face recognition by dlib
# Reference: https://www.tpisoftware.com/tpu/articleDetails/950

import cv2
import dlib
import numpy

img_src_path = 'image/image06.jpg'
img_target_path = 'image/image06-target.jpg'

# 臉部偵測器
faceDetector = dlib.get_frontal_face_detector()

# 載入人臉特徵點檢測器
sp = dlib.shape_predictor('../dlib-dat/shape_predictor_68_face_landmarks.dat')

# 載入人臉辨識檢測器
facerec = dlib.face_recognition_model_v1(
    '../dlib-dat/dlib_face_recognition_resnet_model_v1.dat')

def calculate_target_images_descriptor(imgList):
    descriptorList = []
    for img in imgList:        
        faces, _, _ = faceDetector.run(img, 1, 0)
        for _, d in enumerate(faces):
            shape = sp(img, d)
            faceDescriptor = facerec.compute_face_descriptor(img, shape)
            descriptorList.append(numpy.array(faceDescriptor))
    return descriptorList

def check_face(img, targetDescriptorList, threshold = .5):
    faces, _, _ = faceDetector.run(img, 1, 0)
    height = img.shape[0]
    width = img.shape[1]
    locations = []
    locations_target = []

    for _, d in enumerate(faces):
        shape = sp(img, d)
        faceDescriptor = facerec.compute_face_descriptor(img, shape)
        
        isTarget = False
        for targetDescriptor in targetDescriptorList:
            dist = numpy.linalg.norm(targetDescriptor - faceDescriptor)
            if dist < threshold:
                isTarget = True

        left, top = max(0, d.left()), max(0, d.top())
        right, bottom = min(width, d.right()), min(height, d.bottom())
        
        if isTarget:
            locations_target.append([left, top, right, bottom])
        else:
            locations.append([left, top, right, bottom])

    return locations, locations_target

if __name__ == "__main__":

    loc, loc_tar = check_face(cv2.imread(img_src_path), calculate_target_images_descriptor([cv2.imread(img_target_path)]))
    print(loc)
    print(loc_tar)
