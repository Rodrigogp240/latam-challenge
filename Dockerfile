FROM python:3.10

WORKDIR /LATAM-CHALLENGE

COPY ./ /LATAM-CHALLENGE/

RUN pip install --no-cache-dir --upgrade -r /LATAM-CHALLENGE/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
