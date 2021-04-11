ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

MAINTAINER Tim Davies

LABEL Description="Run rtl_433 to monitor 433MHz events and proxy to MQTT server"

RUN apk-add --no-cache rtl-sdr librtlsdr-dev

RUN apk add --no-cache --virtual build-deps alpine-sdk cmake git libusb-dev && \
    mkdir /tmp/src && \
    cd /tmp/src && \
    git clone https://github.com/merbanan/rtl_433 && \
    cd rtl_433/ && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install && \
    apk del build-deps && \
    rm -r /tmp/src

RUN apk add --no-cache python3 py3-virtualenv && \
    virtualenv venv

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt

COPY proxy /src

CMD /venv/bin/python -m src.proxy /data/options.json