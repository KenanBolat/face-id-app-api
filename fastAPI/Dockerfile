FROM python:3.9-alpine3.13
LABEL maintainer='Kenan BOLAT'

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8090

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
            build-base musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        fast-user && \
    chown -R fast-user:fast-user /vol/* && \

ENV PATH="/py/bin:$PATH"

USER fast-user

