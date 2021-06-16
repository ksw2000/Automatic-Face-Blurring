# 人臉打馬神器

一個可以把非特定人士的臉打馬掉的程式，適合 Youtuber 剪片，目前還在測試階段 :smile:

## 瓶頸

1. OpenCV 人臉偵測很差 → 改用 dlib
2. OpenCV 出來的影片沒有聲音
3. 大影片效能很差 → 可以先做壓縮


## Quick start
```shell
py main-opencv.py   # 以 open cv 實現人臉辨識
py main-fr.py       # 以 face-recognition 套件實現人臉辨識
py main-dlib.py     # 以 dlib (HOG) 實現人臉辨識
```

+ /
    + docker/ *build docker environment*
    + test/
        + image/ *DEMO for face.py*
        + face.py *by Hana*
        + video.py *by Sky*
        + recognition-dlib.py *by Kashiwa*
        + recognition.py *by Annie*
    + init.sh *Linux環境初始化小幫手*
    + main-dlib-full.py *全部以 dlib 實作*
    + main-dlib.py *臉部偵測以 dlib 實作，辨識以 face-recognition 實作*
    + main-fr.py *臉部偵測以 face-recognition 實作*
    + main-opencv.py *臉部偵測以 openCV2 實作*

1. `/test/face.py` 偵測人臉範圍，由 face_recognition 實作 by Hana
2. `/test/video.py` 偵對特定幀特定範圍上馬賽克，由 openCV 實作 by Sky
3. `/test/recognition.py` 給定兩張人臉，判定是否相同，由 face_recognition 實作 by Annie
4. `main-dlib-full.py` 臉部偵測與排除特定臉孔皆由 dlib 實作
5. `main-dlib.py` 臉部偵測由 dlib 實作，排除特定臉孔由 face_recognition 實作
6. `main-fr.py` 臉部偵測由 dlib 實作，排除特定臉孔由 face_recognition 實作

## Environment

### linux
```shell
sh init.sh
```

### docker :whale:
1. Build an image by `docker/build-image.cmd` 
2. Create a new container by `docker/run-container.cmd`

## Some problems

1. 如果 Linux openCV 裝不起來，要裝 python3.7，linux 預設裝 3.6

    ```sh
    apt install python3.7
    ```

2. Linux 裝 dlib
    
    參考：[https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/)

3. Windows dlib 裝不起來
    + install `cmake` first
    + install `Visual studio` (2015)