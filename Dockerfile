FROM python:3.5.1

WORKDIR /code
EXPOSE 9000

RUN python -m pip install uwsgi

COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt

ADD . /code

CMD ["uwsgi", "--ini", "uwsgi.ini"]
