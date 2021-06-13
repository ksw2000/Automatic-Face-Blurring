# 自動車牌、人臉打馬

## 瓶頸

1. OpenCV 人臉偵測跟屎一樣
    > 法一：圖片先不要先轉灰(範例通常都有轉灰)
    >
    > 法二：改用 dlib 來偵測，但 dlib 效果也不太行，豆頁痛
2. OpenCV 出來的影片沒有聲音

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
py main-dlib.py     # 以 dlib 實現人臉辨識
```

+ /
    + docker/ *build docker environment*
    + image/ *DEMO for face.py*
    + demo.mp4 *各位自己放，不然github會炸掉*
    + face.py *by Hana*
    + init.py *Linux環境初始化小幫手*
    + main-dlib.py *臉部偵測以 dlib 實作*
    + main-fr.py *臉部偵測以 face-recognition 實作*
    + main-opencv.py *臉部偵測以 openCV2 實作*
    + video.py *by Sky*

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