FROM python:3.5.1

WORKDIR /code
EXPOSE 9000

# Add Tini
ENV TINI_VERSION v0.9.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

RUN python -m pip install uwsgi

COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt

ADD . /code

CMD ["uwsgi", "--ini", "uwsgi.ini"]
