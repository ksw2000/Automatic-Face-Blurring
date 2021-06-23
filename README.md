# Automatic Face Blurring

Automatic Face Blurring - A simple final project in the artificial intelligence course at NCHU.

## Overview

The python CLI tool that can blur the human's face except for the targets you specify. 

It is a little difficult to initialize an environment for this program, so I suggest you can run this program on [Google Colab](https://colab.research.google.com/).


## Quick start

```shell
# Blur all face in src.mp4
py main.py src.mp4

# Blur all faces except for target1.png and target2.png
py main.py src.mp4 -t target1.png target2.jpg

# Besides, you can specify the filename of the output video.
py main.py src.mp4 -t target1.png -o my-video.mp4

# Show face descriptor on the face.
py main.py src.mp4 -t target1.png --show
```

+ /
    + docker/ *build docker environment*
    + dlib-dat/ *
Dependencies for dlib*
    + init.sh *Build linux environment*
    + main.py
