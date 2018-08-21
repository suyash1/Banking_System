'''
@author:suyash
the celery app which is performing backgroud async task processing

the config is loaded from project/settings file for now, which can be separated
as a part of good practice. Right now basic settings are used like broker and db number.
Redis is used as a broker here
'''
from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Banking_System.settings')

app = Celery('bank')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
