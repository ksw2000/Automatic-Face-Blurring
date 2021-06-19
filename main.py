# 2021/06/16
# Authur: Kashiwa
# Reference: https://www.tpisoftware.com/tpu/articleDetails/950

import cv2
import dlib
import numpy

# 宣告三個分類器
# face detector: 臉部偵測，偵測臉部範圍
# sp: 尋找臉部 68 個特徵測
# facerec: 臉部辨識

faceDetector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('dlib-dat/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1(
    'dlib-dat/dlib_face_recognition_resnet_model_v1.dat')


def target_images_descriptor(imgList, decThreshold=0):
    descriptorList = []
    for img in imgList:        
        faces, _, _ = faceDetector.run(img, 1, decThreshold)
        for _, d in enumerate(faces):
            shape = sp(img, d)
            faceDescriptor = facerec.compute_face_descriptor(img, shape)
            descriptorList.append(numpy.array(faceDescriptor))
    return descriptorList


def mosaic_except_target(frame, targetDescriptorList, recThreshold=.58, decThreshold = 0):
    # targetDescriptorList 是所有 target 圖片中人臉的 descriptor
    # decThreshold 是偵測人臉的最低門檻，值越高越接近人臉
    # recThreshold 是偵測相同臉旦的最高門檻，值越低兩者越相近

    faces, _, _ = faceDetector.run(frame, 1, decThreshold)
    width, height = frame.shape[1], frame.shape[0]

    location_dists_pair = []
    for face in faces:
        # 避免範圍超過圖片範圍
        left, top = max(0, face.left()), max(0, face.top())
        right, bottom = min(width, face.right()), min(height, face.bottom())

        shape = sp(frame, face)
        faceDescriptor = facerec.compute_face_descriptor(frame, shape)
     
        # 取得該張臉在 target list 中最小值
        dist = 1
        for targetDescriptor in targetDescriptorList:
            candidate = numpy.linalg.norm(targetDescriptor - faceDescriptor)
            if candidate < dist:
                dist = candidate

        location_dists_pair.append({
            "dist" : dist,
            "locations": (left, top, right, bottom)
        })

    # 一幀中最多僅有的 n 張臉為 target
    # n = target 的 長度
    # 且這 n 張臉的 dist 仍必需小於門檻

    n = len(targetDescriptorList)
    location_dists_pair.sort(key=lambda s: s["dist"])

    for index, pair in enumerate(location_dists_pair):
        left, top, right, bottom = pair['locations']
        if index < n and pair['dist'] < recThreshold:
            # 目標臉 ─ 顯示紅色方框
            rectangle(frame, left, top, right, bottom)
        else:
            # 非目標臉 ─ 打馬
            mosaic(frame, left, top, right, bottom)

        cv2.putText(frame, str(pair['dist']), (left, top), cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 0), 1, cv2.LINE_AA)

def mosaic_face(frame):
    # faceDetector.run()
    # 第一個參數是來源圖
    # 第二個參數是偵測的最大次數
    # 第三個參數是門檻值，只有信心值比這個門檻值高的臉會被回傳
    # 信心值越高越有可能是臉
    faces, _, _ = faceDetector.run(frame, 1, 0)
    height, width = frame.shape[0], frame.shape[1]
    
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
    
    target_descriptors = target_images_descriptor(cv2_target_img_list)
    
    # 是否啟用排除特定人臉模式
    recog_mode = len(target_img_list) != 0

    if recog_mode:
        print("Face recoginition mode ON\n\n")
    else:
        print("Face recoginition mode OFF\n\n")

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
            mosaic_except_target(frame, target_descriptors)
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
    video_src_path = './demo/src.mp4'
    video_dest_path = './demo/res.mp4'
    target_img_path_list = ['./demo/target.png']
    video_generator(video_src_path, video_dest_path, target_img_path_list)
