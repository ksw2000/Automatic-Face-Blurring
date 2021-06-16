# 2021/06/16
# Authur: Kashiwa
# Reference: https://www.tpisoftware.com/tpu/articleDetails/950

import cv2
import dlib
import numpy

faceDetector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('dlib-dat/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1(
    'dlib-dat/dlib_face_recognition_resnet_model_v1.dat')


def calculate_target_images_descriptor(imgList, decThreshold=0):
    descriptorList = []
    for img in imgList:        
        faces, _, _ = faceDetector.run(img, 1, decThreshold)
        for _, d in enumerate(faces):
            shape = sp(img, d)
            faceDescriptor = facerec.compute_face_descriptor(img, shape)
            descriptorList.append(numpy.array(faceDescriptor))
    return descriptorList


def mosaic_face_advance(frame, targetDescriptorList, recThreshold=.58, decThreshold = 0):
    # decThreshold 是偵測人臉的最低門檻，值越高越接近人臉
    # recThreshold 是偵測相同臉旦的最高門檻，值越低兩者越相近

    faces, _, _ = faceDetector.run(frame, 1, decThreshold)
    width, height = frame.shape[1], frame.shape[0]

    dists = []
    locations = []
    minDist = 1
    minDistIndex = 0
    for d in faces:
        # 避免範圍超過圖片範圍
        left, top = max(0, d.left()), max(0, d.top())
        right, bottom = min(width, d.right()), min(height, d.bottom())

        shape = sp(frame, d)
        faceDescriptor = facerec.compute_face_descriptor(frame, shape)
     
        # 該張臉對 target list 中最小值
        dist = 1
        for targetDescriptor in targetDescriptorList:
            candidate = numpy.linalg.norm(targetDescriptor - faceDescriptor)
            if candidate < dist:
                dist = candidate
        
        # 尋找該幀中最接近的臉
        if dist < minDist:
            minDist = dist
            minDistIndex = len(dists)

        dists.append(dist)
        locations.append((left, top, right, bottom))

    # 一幀中僅有最小的為 target 且該最小的 dist 仍必需小於門檻
    for index in range(len(locations)):
        left, top, right, bottom = locations[index]
        if index == minDistIndex and dists[index] < recThreshold:
            rectangle(frame, left, top, right, bottom)
        else:
            mosaic(frame, left, top, right, bottom)

        cv2.putText(frame, str(dists[index]), (left, top), cv2.FONT_HERSHEY_PLAIN,
                1, (255, 255, 0), 1, cv2.LINE_AA)

def mosaic_face(frame):
    # .run()
    # The first argument is the source of image
    # The second argument is the max times of detection
    # The third argument is a threshold
    # only the image which have a score bigger than this one can be returned
    faces, _, _ = faceDetector.run(frame, 1, 0)
    height = frame.shape[0]
    width = frame.shape[1]
    
    for _, f in enumerate(faces):
        left, top = max(0, f.left()), max(0, f.top())
        right, bottom = min(width, f.right()), min(height, f.bottom())
        mosaic(frame, left, top, right, bottom)

def mosaic(frame, left, top, right, bottom):
    frame[top:bottom, left:right] = cv2.GaussianBlur(
        frame[top:bottom, left:right], (59, 59), 0)

def rectangle(frame, left, top, right, bottom):
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 3)

# 馬賽克影片自動生成
# video_scr_path string 原影片路徑
# video_dest_path string 生成影片路徑
# target_img_list list 排除的人臉路徑
def video_generator(video_src_path, video_dest_path, target_img_list):
    cv2_target_img_list = []
    for img in target_img_list:
        cv2_target_img_list.append(cv2.imread(img))
    
    target_descriptors = calculate_target_images_descriptor(cv2_target_img_list)
    
    # Does active the recognition mode or not
    recog_mode = len(target_img_list) != 0

    if not recog_mode:
        print("Face recoginition mode OFF\n\n")
    else:
        print("Face recoginition mode ON\n\n")

    # 讀取影片相關資訊
    video_src = cv2.VideoCapture(video_src_path)
    video_dest = cv2.VideoWriter(
        video_dest_path, cv2.VideoWriter_fourcc(*'mp4v'),
        video_src.get(cv2.CAP_PROP_FPS), (
            int(video_src.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video_src.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
    )

    # 開始一幀一幀讀取
    success, frame = video_src.read()
    if not success:
        print("Error opening video stream or file")
        return

    count = 0
    while success:
        if recog_mode:
            mosaic_face_advance(frame, target_descriptors)
        else:
            mosaic_face(frame)

        if count % 30 == 0:
            print("Finish %d frames" % (count))
        count += 1

        video_dest.write(frame)
        success, frame = video_src.read()

    video_src.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # video_src_path        指定輸入之影片位置
    # video_dest_path       指定輸出之影片位置
    # target_img_path_list  指定不會被打馬的人臉
    video_src_path = './demo/demo3/src.mp4'
    video_dest_path = './demo/demo3/res-dlib-full.mp4'
    target_img_path_list = ['./demo/demo3/target.png']
    video_generator(video_src_path, video_dest_path, target_img_path_list)
