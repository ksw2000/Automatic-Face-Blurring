# 2021/06 
# Authur: 
#   1. Kashiwa: openCV detect face & intergration 
#   2. Sky: mosaic

# Reference:
#   1. https://github.com/adarsh1021/facedetection
#   2. https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html

import cv2

# face_detect
# https://github.com/adarsh1021/facedetection/blob/master/haarcascade_frontalface_default.xml
faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# @return left, top, right, bottom
def get_face(frame):
    # 第一個參數是圖源
    # 第二個參數是在掃描時搜尋窗口的比例，預設是 1.1
    # 第三個參數是指檢索成功的矩形其相鄰的其他矩形，至少要距離幾個相素，預設是 3
    # https://blog.csdn.net/itismelzp/article/details/50379359
    faces = faceDetector.detectMultiScale(
        frame, 1.05, 4, flags=cv2.CASCADE_DO_CANNY_PRUNING)
    res = []
    for (x, y, w, h) in faces:
        res.append([x, y, x+w, y+h])
    return res

# left-top coordinate: (left: x-axis, top: y-axis), right-bottom coordinates: (right: x-axis, bottom: y-axis)
def mosaic_video(frame, left, top, right, bottom):
    frame[top:bottom, left:right] = cv2.GaussianBlur(
        frame[top:bottom, left:right], (59, 59), 0)

video_src_path = "./demo.mp4"
video_dest_path = "./demo-res-cv.mp4"

# 讀取影片相關資訊
video_src = cv2.VideoCapture(video_src_path)

fps = video_src.get(cv2.CAP_PROP_FPS)
size = (int(video_src.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video_src.get(cv2.CAP_PROP_FRAME_HEIGHT)))

video_dest = cv2.VideoWriter(video_dest_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

# 一幀一幀讀取
success, frame = video_src.read()
if not success:
    print("Error opening video stream or file")

while success:
    for face in get_face(frame):
        mosaic_video(frame, face[0], face[1], face[2], face[3])

    # display the resulting frame
    cv2.imshow("Frame", frame)  
    
    # Press Q on keyboard to exit
    if cv2.waitKey(10) & 0xFF == ord('q'):  
        break
    video_dest.write(frame)
    success, frame = video_src.read()

video_src.release()
cv2.destroyAllWindows()
