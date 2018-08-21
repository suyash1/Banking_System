# -*- coding: utf-8 -*-
'''
@author: suyash
simple admin interface of the application.
Register your models below to have admin access on the
In order to use admin interface, you need to register superuser.
Please look up https://docs.djangoproject.com/en/1.11/intro/tutorial02/#introducing-the-django-admin
'''
from __future__ import unicode_literals

from django.contrib import admin
from .models import Account, Transactions

admin.site.register(Account)
admin.site.register(Transactions)
