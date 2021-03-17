#!/bin/bash

python -m client > /dev/null &
sleep 2
celery -A client.tasks worker --uid=nobody --gid=nogroup --loglevel=ERROR > /dev/null &
sleep 2
python client/frontend.py
