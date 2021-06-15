# 2021/06/16
# @author:
#   1. Hana:    face detect
#   2. Sky:     mosaic
#   3. Annie:   face recoginition
#   4. Kashiwa: integration

import cv2
import face_recognition

def get_face(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    faces = face_recognition.face_locations(frame)
    res = []
    for top, right, bottom, left in faces:
        left, top = max(0, left), max(0, top)
        right, bottom = min(width, right), min(height, bottom)
        res.append([left, top, right, bottom])
    return res


def get_face_skip_target(frame, target_encodings):
    res = []
    faces = get_face(frame)
    print("Get", len(faces), "faces")
    for (left, top, right, bottom) in faces:
        # Check bounding
        encodings = face_recognition.face_encodings(
            frame[top:bottom, left:right])
        for encoding in encodings:
            matches = face_recognition.compare_faces(
                target_encodings, encoding)

            if True not in matches:
                print("    - Mark 1")
                res.append([left, top, right, bottom])
            else:
                rectangle(frame, left, top, right, bottom)
                print("    - Skip 1")

    return res

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
    target_img_encodings = []
    for img in target_img_list:
        for encoding in face_recognition.face_encodings(cv2.imread(img)):
            target_img_encodings.append(encoding)

    # Does active the recognition mode or not
    recog_mode = len(target_img_encodings) != 0

    if not recog_mode:
        print(" - Face recoginition mode OFF")
    else:
        print(" - Face recoginition mode ON")

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
            faces = get_face_skip_target(frame, target_img_encodings)
        else:
            faces = get_face(frame)

        for (left, top, right, bottom) in faces:
            mosaic(frame, left, top, right, bottom)

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
    video_src_path = './demo/demo6.mp4'
    video_dest_path = './demo/demo6-res.mp4'
    target_img_path_list = [
        './demo/demo-face-5.png', './demo/image06-target.jpg']
    video_generator(video_src_path, video_dest_path, target_img_path_list)
