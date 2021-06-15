import cv2 as cv
import numpy as np

def mosaic_video(left, top, right, bottom, frame): # left-top coordinate: (left: x-axis, top: y-axis), right-bottom coordinates: (right: x-axis, bottom: y-axis)
    image = frame[top:bottom, left:right] # Get the specific area
    frame[top:bottom, left:right] = cv.GaussianBlur(image, (59, 59), 0) # Blur specific area

VIDEO_PATH = "./bunny.mp4"
video = cv.VideoCapture(VIDEO_PATH)

if(video.isOpened() == False):
    print("Error opening video stream or file")

while(video.isOpened()):
    ret, frame = video.read()
    mosaic_video(400, 0, 600, 400, frame)
    if ret:
        cv.imshow("Frame", frame) # display the resulting frame

        if cv.waitKey(10) & 0xFF == ord('q'): # Press Q on keyboard to exit
            break
    else:
        break

video.release()
cv.destroyAllWindows()