FROM python:3.8-slim

RUN pip install pipenv
COPY Pipfile* /tmp/

RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV REGISTRY_ADDRESS=http://127.0.0.1:5000
ENV NUM_PLAYERS=4

RUN apt-get update && apt-get install -y redis-server
RUN service redis-server start

WORKDIR /app
COPY . /app

RUN ["chmod", "+x", "./entrypoint.sh"]
ENTRYPOINT [ "./entrypoint.sh" ]
