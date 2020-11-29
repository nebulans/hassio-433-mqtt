ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

MAINTAINER Tim Davies

LABEL Description="Run rtl_433 to monitor 433MHz events and proxy to MQTT server"

RUN apk add --no-cache --virtual build-deps alpine-sdk cmake git libusb-dev && \
    mkdir /tmp/src && \
    cd /tmp/src && \
    git clone git://git.osmocom.org/rtl-sdr.git && \
    mkdir /tmp/src/rtl-sdr/build && \
    cd /tmp/src/rtl-sdr/build && \
    cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr/local && \
    make && \
    make install && \
    chmod +s /usr/local/bin/rtl_* && \
    cd /tmp/src/ && \
    git clone https://github.com/merbanan/rtl_433 && \
    cd rtl_433/ && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install && \
    apk del build-deps && \
    rm -r /tmp/src && \
    apk add --no-cache libusb

RUN apk add --no-cache python3 py3-virtualenv && \
    virtualenv venv

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt

COPY proxy /src

CMD /venv/bin/python /src/proxy.py /data/options.json