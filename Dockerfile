FROM python:3

WORKDIR /usr/src/app

COPY soapclass/*.py ./soapclass/
COPY mousse-command.py ./
COPY .env ./

RUN apt-get -y update && \
    apt-get -y install --no-install-recommends tzdata && \
    apt-get purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install pytz python-telegram-bot python-dotenv

CMD [ "python", "./mousse-command.py" ]
