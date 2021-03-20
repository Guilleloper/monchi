FROM python:3.9.2-buster

ENV BASE_PATH=/monchi

WORKDIR ${BASE_PATH}

RUN pip install python-telegram-bot==10.1.0 --upgrade \
  && groupadd -g 10002 monchi \
  && useradd -g 10002 -u 10002 -d /home/monchi -m -s /usr/sbin/nologin monchi \
  && mkdir ${BASE_PATH}/data \
  && mkdir ${BASE_PATH}/log

COPY ./bin bin
COPY ./config config

RUN chown -R monchi:monchi .

USER monchi:monchi

ENTRYPOINT ["python", "bin/monchi.py"]