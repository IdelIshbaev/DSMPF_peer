from celery import Celery

app = Celery(broker="memory://localhost/")


@app.task
def example_task(x, y):
    # do something
    pass
