FROM python:3.5.1-alpine

WORKDIR /code
EXPOSE 9000

# Add Tini
RUN apk --update add \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/community/ \
    tini
ENTRYPOINT ["/sbin/tini", "--"]

RUN apk --update add \
    gcc \
    linux-headers \
    musl \
    musl-dev \
    postgresql-dev
RUN python -m pip install uwsgi

COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt

ADD . /code

CMD ["uwsgi", "--ini", "uwsgi.ini"]
