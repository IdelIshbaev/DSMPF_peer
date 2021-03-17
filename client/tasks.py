from celery import Celery
import requests
from urllib.parse import urljoin
import os

SELF_ADDRESS = os.getenv("SELF_ADDRESS", f"http://127.0.0.1:{os.environ['PORT']}")


app = Celery(broker="redis://localhost", backend="rpc://")


@app.task
def timeout_task(address):
    url = urljoin(SELF_ADDRESS, "/timeout/")
    requests.post(url, json={"address": address})
