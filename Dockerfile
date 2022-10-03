FROM pytorch/pytorch:latest
ENV PYTHONUNBUFFERED 1
WORKDIR /web
COPY . .
RUN pip install -r requirements.txt