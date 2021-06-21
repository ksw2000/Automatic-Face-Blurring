# 人臉打馬神器

一個可以把非特定人士的臉打馬掉的程式，適合 Youtuber 剪片，目前還在測試階段 :smile:

## Quick start

```shell
# 人臉馬賽克
py main.py src.mp4

# 排除特定人臉
py main.py src.mp4 -t target1.png target2.jpg

# 指定輸出名稱
py main.py src.mp4 -t target1.png -o my-video.mp4

# 印出臉部特徵值
py main.py src.mp4 -t target1.png --show
```

+ /
    + docker/ *build docker environment*
    + dlib-dat/ *dlib 的分類器*
    + test/ *測試用檔案*
        + another-ver/ *以其他套件進行實作*
        + image/ *DEMO for face.py*
    + init.sh *Linux環境初始化小幫手*
    + main.py

**測試檔案**

1. `/test/face.py` 偵測人臉範圍，由 face_recognition 實作 by Hana
2. `/test/video.py` 偵對特定幀特定範圍上馬賽克，由 openCV 實作 by Sky
3. `/test/recognition.py` 給定兩張人臉，判定是否相同，由 face_recognition 實作 by Annie
4. `/test/recognition-dlib.py` 改用 dlib 實作 by Kashiwa
5. `/test/another-ver/` 以其他套件實作 main.py
    |  路徑  | 臉部偵測 | 臉部辨識 |
    |--------|---------|----------|
    | `main-dlib.py` | face_recognition | dlib |
    | `main-fr.py` | face_recognition | face_recognition |
    | `main-opencv.py` | open cv | 不支援 |

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