FROM python:3.8

RUN adduser --disabled-password chesski

WORKDIR /home/chesski

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY chesski.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP chesski.py

RUN chown -R chesski:chesski ./
USER chesski

EXPOSE 8080

ENTRYPOINT ["./boot.sh"]