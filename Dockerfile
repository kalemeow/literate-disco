FROM ubuntu

MAINTAINER kalemeow <kizzale@gmail.com>

RUN apt-get update && apt-get install -y python3 \
	python3-pip

RUN python3 -m pip install apachelogs \
	Flask \
    apachelogs

VOLUME /data

ADD main.py /main.py

EXPOSE 5000

CMD python3 /main.py
