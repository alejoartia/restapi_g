FROM python:3.9

WORKDIR '/backend'

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

COPY app ./app

RUN sh -c 'apt-get update  -y  && apt-get install build-essential curl python3-dev musl-dev git -y && apt-get clean -y'

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

RUN pytest -vv

CMD [ "/start.sh" ]

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]



