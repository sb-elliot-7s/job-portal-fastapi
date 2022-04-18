from celery import Celery

BROKER_URL = 'pyamqp://guest@localhost//'
celery_app = Celery('app', broker=BROKER_URL)

import auth.tasks
