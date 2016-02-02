FROM python:3.5.1
WORKDIR /code
COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt
ADD . /code
