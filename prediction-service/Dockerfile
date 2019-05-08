FROM python:3.6

EXPOSE 8000

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

CMD ["python", "/app/app.py"]
