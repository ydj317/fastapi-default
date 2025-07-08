from app.celery_worker import my_task

@my_task.task
def add(x, y):
    return x + y
