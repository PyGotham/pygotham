FROM python:3.5.1-alpine

WORKDIR /code
EXPOSE 9000

# Install the system requirements. Clean up the cache after; the --no-cache flag
# takes care of a lot of this, but there are a few things that get cached anyway
# (at least as of the last time I checked the behavior), so manually clear the
# cache just to be certain.
RUN \
    apk --update --no-cache add \
        gcc \
        linux-headers \
        musl-dev \
        postgresql-dev \
        tini \
    && rm -rf /var/cache/apk/*
RUN python -m pip install uwsgi

ENTRYPOINT ["/sbin/tini", "--"]

# Copy the application's requirements separate from the application itself.
# Doing this as part of the `ADD . /code` below would result in running
# `pip install` whenever there was a change to the application, including things
# like templates and assets.
COPY requirements.txt /code/
RUN python -m pip install --no-cache-dir -r requirements.txt

ADD . /code

CMD ["uwsgi", "--ini", "uwsgi.ini"]
