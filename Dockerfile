FROM python:3.7-alpine

RUN adduser -D conferatur
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base
RUN pip install --upgrade pip

WORKDIR /home/conferatur
COPY . /home/conferatur/

RUN pip install '.[api]'

RUN chown -R conferatur:conferatur ./
USER conferatur

EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", ":8080", "--access-logfile", "-", "--error-logfile", "-", "conferatur.api.gunicorn"]