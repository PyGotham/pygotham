FROM python:3.4.3
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code
