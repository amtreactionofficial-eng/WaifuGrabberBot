FROM python:3.10-slim
RUN apt update && apt upgrade -y
RUN apt-get install git curl python3-pip ffmpeg -y
COPY requirements.txt .

RUN pip3 install wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt
WORKDIR /app
COPY . .
CMD python3 -m Grabber
