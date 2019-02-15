FROM python:3.7-alpine

LABEL maintainer="Jeremy Kenyon <jrkenyon07@gmail.com>"

RUN adduser -D sbmacro

WORKDIR /home/sbmacro

COPY requirements.txt requirements.txt

RUN python -m venv sbmacro
RUN sbmacro/bin/pip install -r requirements.txt
RUN sbmacro/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY sbmacro.py config.py sbmacro.db boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP sbmacro.py

RUN chown -R sbmacro:sbmacro ./
USER sbmacro

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]




