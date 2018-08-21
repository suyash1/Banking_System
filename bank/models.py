# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.crypto import get_random_string


class Account(models.Model):
	account_number = models.CharField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Account number', max_length=200)
	balance = models.FloatField(default=0)
	
	class Meta:
		verbose_name = 'Account'
		verbose_name_plural = 'Accounts'

	def __unicode__(self):
		return str(self.account_number)
	

class Transactions(models.Model):
	account_number = models.ForeignKey(Account)
	reference = models.CharField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Transaction Reference', max_length=200)
	amount = models.FloatField(null=True, blank=True, default=0.0)
	action = models.CharField(null=True, max_length=15)
	
	class Meta:
		verbose_name = 'Transaction'
		verbose_name_plural = 'Transactions'
	
	def __unicode__(self):
		return self.reference

	
