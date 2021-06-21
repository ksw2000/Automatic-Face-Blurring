#!/bin/bash
apt update
apt install python3.7
apt install build-essential cmake
apt install libopenblas-dev liblapack-dev
apt install libx11-dev libgtk-3-dev
apt install python3-pip
python -m pip install --upgrade pip
pip3 install dlib
pip3 install face-recognition
pip3 install pillow
pip3 install scikit-build
pip3 install opencv-python