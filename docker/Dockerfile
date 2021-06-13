FROM ubuntu:18.04
MAINTAINER liao2000

RUN cd ~
RUN bash
RUN apt update
RUN apt upgrade -y
RUN apt install build-essential -y
RUN apt install nano -y
RUN apt install python3.7
RUN apt install cmake
RUN apt install libopenblas-dev liblapack-dev
RUN apt install libx11-dev libgtk-3-dev
RUN apt install python-pip
RUN python -m pip install --upgrade pip
RUN pip3 install dlib
RUN pip3 install face-recognition
RUN pip3 install pillow
RUN pip3 install opencv-python

CMD ["bash"]
