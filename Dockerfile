FROM python:3.9
LABEL maintainer='Kenan BOLAT'

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8090

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && apt-get install libgl1 libpq-dev python-dev -y && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol/* && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts/* && \
    chown -R django-user:django-user /scripts/*
#
RUN mkdir -p /home/django-user/.deepface/weights/
RUN wget https://github.com/serengil/deepface_models/releases/download/v1.0/vgg_face_weights.h5 -P /home/django-user/.deepface/weights/


ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]