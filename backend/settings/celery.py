import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')
app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'every-1-minute-every-day': {
        'task': 'debug_task',
        'schedule': crontab(minute='*/1')
    }
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
