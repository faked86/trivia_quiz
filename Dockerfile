# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./run.py ./run.py
COPY src src
COPY ./wait-for-it.sh ./wait-for-it.sh
RUN chmod +x ./wait-for-it.sh

CMD python run.py
