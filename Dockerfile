FROM python:3.9-alpine3.13
LABEL maintainer='Kenan BOLAT'

ENV PYTHONUNBUFFERED 1
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
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
            build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ;  \
    fi &&\
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol/* && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts/* && \
    chown -R django-user:django-user /scripts/* && \
    chown -R django-user:django-user /app/sqlite3.db \

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]