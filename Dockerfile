FROM ubuntu:24.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    apt install python3.12 && \
    apt install python3-pip -y && \
    apt install python3-venv -y

CMD tail -f /dev/null
