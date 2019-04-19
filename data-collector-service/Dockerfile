FROM python:3.6

RUN mkdir /app
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install cron
ADD crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron

# ENV LOG_FILE="/app/log.txt"
# RUN touch ${LOG_FILE}
CMD ["cron", "-f"]
# CMD cron && tail -f ${LOG_FILE}
