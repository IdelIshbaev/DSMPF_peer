FROM python:3.8-slim

RUN pip install pipenv
COPY Pipfile* /tmp/

RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "registry"]