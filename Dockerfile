# syntax=docker/dockerfile:1.2
FROM python:latest

WORKDIR /LATAM-CHALLENGE

COPY ./requirements.txt /LATAM-CHALLENGE/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /LATAM-CHALLENGE/requirements.txt

COPY ./challenge/ /LATAM-CHALLENGE/challenge/

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "80"]
