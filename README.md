# 人臉打馬神器

一個可以把非特定人士的臉打馬掉的程式，適合 Youtuber 剪片，目前還在測試接段

## 瓶頸

1. OpenCV 人臉偵測跟屎一樣
    > 法一：圖片先不要先轉灰(範例通常都有轉灰)
    >
    > 法二：改用 dlib 來偵測，但 dlib 效果也不太行，豆頁痛
2. OpenCV 出來的影片沒有聲音
3. 大影片效能很差

## 環境

### linux
```shell
sh init.sh
```

### docker :whale:
docker 的部分有提供一個 `docker/build-image.cmd` 和 `docker/run-container.cmd` 可能有些要自己改一下，我自己也不太會用，嘿嘿~

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
        + recoginition.py *by Annie*
    + init.sh *Linux環境初始化小幫手*
    + main-dlib.py *臉部偵測以 dlib 實作*
    + main-fr.py *臉部偵測以 face-recognition 實作*
    + main-fr-recog.py *臉部偵測並支援人臉辨識*
    + main-opencv.py *臉部偵測以 openCV2 實作*

## Some problems

1. 如果 Linux openCV 裝不起來，要裝 python3.7，linux 預設裝 3.6

    ```sh
    apt install python3.7
    ```

2. Linux 裝 dlib
    
    參考：[https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/)

3. Windows dlib 裝不起來
    + 要先裝 cmake
    + 然後裝 Visual studio 