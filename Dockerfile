FROM python:3

WORKDIR /usr/src/app

COPY soapclass/*.py ./soapclass/
COPY mousse-command.py ./
COPY .env ./

RUN pip install pytz 
RUN pip install python-telegram-bot
RUN pip install python-dotenv

CMD [ "python", "./mousse-command.py" ]