FROM pytorch/pytorch:latest
ENV PYTHONUNBUFFERED 1
WORKDIR /web
COPY . .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN python -c 'import torch; torch.hub.load("ultralytics/yolov5", "yolov5n")'
RUN rm yolov5n.pt
RUN mkdir logs