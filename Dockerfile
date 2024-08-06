FROM python:3.10-slim-buster
RUN apt-get update -y
RUN apt-get install git curl python3-pip -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install -U pip
COPY . /app/
WORKDIR /app/
RUN pip3 install -r requirements.txt
CMD python3 -m MBot
