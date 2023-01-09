FROM python:3.9-bullseye
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_PASSWORD password
ENV DJANGO_SUPERUSER_EMAIL admin@wonbeomjang.kr
ENV GRIPP_BASIC_TOKEN YWRtaW46cGFzc3dvcmQ=
WORKDIR /ffmpeg
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx wget
RUN wget https://github.com/cannot-climb/gripp-ffmpeg/raw/master/5.1.1/ffmpeg-release-$(dpkg --print-architecture)-static.tar.xz -O ffmpeg.tar.xz
RUN ["tar", "Jxvf", "ffmpeg.tar.xz", "--strip-components", "1"]
RUN ["rm", "ffmpeg.tar.xz"]
RUN ["ln", "-s", "/ffmpeg/ffmpeg", "/usr/local/bin/ffmpeg"]
RUN ["ln", "-s", "/ffmpeg/ffprobe", "/usr/local/bin/ffprobe"]
WORKDIR /web
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python -c 'import torch; torch.hub.load("ultralytics/yolov5", "yolov5n")'
RUN rm yolov5n.pt
ENTRYPOINT ["/web/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
