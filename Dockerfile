FROM python:3.8.4-slim-buster

COPY app ./app

RUN sh -c 'apt-get update  -y  && apt-get install build-essential curl python3-dev musl-dev git -y && apt-get clean -y'

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

