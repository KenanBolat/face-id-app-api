FROM python:3.9
LABEL maintainer='Kenan BOLAT'

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app/sqlite3.db /app/sqlite3.db
COPY ./scripts/run.sh /scripts/run.sh
COPY ./app /app
WORKDIR /app
EXPOSE 8000

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

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 3600 app.wsgi:application
