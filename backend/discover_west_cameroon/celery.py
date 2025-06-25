
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discover_west_cameroon.settings')



app = Celery('discover_west_cameroon')
# celery.py (development fallback)
#app.conf.broker_url = 'memory://'
#app.conf.result_backend = 'cache+memory://'

# For production, you would typically set these in your settings.py or environment variables
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.broker_connection_retry_on_startup = True