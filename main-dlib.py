# 2021/06 
# Authur: 
#   1. Kashiwa: face detect by dlib & integration
#   2. Sky:     mosaic
# Reference:
# 1. http://dlib.net/face_detector.py.html

import cv2
import dlib

# face detector
faceDetector = dlib.get_frontal_face_detector()

# @return left, top, right, bottom
def get_face(frame):
    # .run()
    # The first argument is the source of image
    # The second argument is the max times of detection
    # The third argument is a threshold, only the score bigger than this value
    # will be returned
    faces, _, _ = faceDetector.run(frame, 1, 0)
    height = frame.shape[0]
    width = frame.shape[1]
    res = []
    for _, f in enumerate(faces):
        left, top = max(0, f.left()), max(0, f.top())
        right, bottom = min(width, f.right()), min(height, f.bottom())
        res.append([left, top, right, bottom])
    return res

# left-top coordinate: (left: x-axis, top: y-axis), right-bottom coordinates: (right: x-axis, bottom: y-axis)
def mosaic_video(frame, left, top, right, bottom):
    frame[top:bottom, left:right] = cv2.GaussianBlur(
        frame[top:bottom, left:right], (59, 59), 0)

video_src_path = "./demo.mp4"
video_dest_path = "./demo-res-dlib.mp4"

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

count = 0
while success:
    faces = get_face(frame)
    for face in faces:
        if frame is not None:
            mosaic_video(frame, face[0], face[1], face[2], face[3])

    if count % 30 == 0:
        print("Finish %d frames" % (count))
    count += 1

    video_dest.write(frame)
    success, frame = video_src.read()

video_src.release()
cv2.destroyAllWindows()
