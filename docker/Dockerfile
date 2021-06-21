FROM ubuntu:18.04

RUN cd ~
RUN bash
RUN apt update
RUN apt upgrade -y
RUN apt install build-essential -y
RUN apt install nano -y
RUN apt install python3.7 -y
RUN apt install cmake -y
RUN apt install libopenblas-dev liblapack-dev -y
RUN apt install libx11-dev libgtk-3-dev -y
RUN apt install python3-pip -y
RUN pip3 install dlib
RUN pip3 install scikit-build
RUN pip3 install opencv-python

CMD ["bash"]
