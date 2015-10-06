FROM python:3.4.3
WORKDIR /code
COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt
ADD . /code
