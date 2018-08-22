'''
@author suyash
The core module which handles all the banking operation and db handling as well.
This module basically contains celery tasks for the background processing of the
banking operation.
All the operations are currently using Pessimist design approach, in which every
transaction is atomic and a read/write lock on table is acquired with every operation

Improvements-
1: DB handling can be decoupled in a separate DAO layer going forward
2: Using a combination of Optimistic(using versioning field for every write operation) 
   and Pessimistic design approach based upon concurrency in mind.
3: Only DBError is handled which can be further handled as of now
4: We can have a periodic task as well in case of task failure with retriable exception
   which will periodically try to execute the task upto certain number of retries
'''
from __future__ import absolute_import
from django.db import transaction, connection, DatabaseError
from .models import Account
from .celery import app
from celery.decorators import task
from celery import shared_task
from bank.utils import unset_transaction_log

class AccountOperation(object):
	'''
	Main operation class which is currently implements two methods: withdraw and deposit.
	'''
	def __init__(self):
		pass

	@classmethod
	def deposit(cls, account_num, amount):
		account = None
		try:
			with transaction.atomic():
				account = Account.objects.select_for_update().get(account_number=account_num)
				account.balance += amount
				account.save()
		except DatabaseError, e:
			account.balance -= amount
			transaction.rollback()
			raise e
		return account


	@classmethod
	def withdraw(cls, account_num, amount):
		try:
			with transaction.atomic():
				account = Account.objects.select_for_update().get(account_number=account_num)
				if account.balance - amount >= 0:
					account.balance -= amount
					account.save()
				else:
					return account, "Insufficient balance"
			return account, "Success"
		except DatabaseError, e:
			account.balance += amount
			transaction.rollback()
			raise e
		return account


@app.task
def transfer_money(from_acc, to_acc, amount):
	'''
	Async transfer celery task which will be executed after ETA is completed.
	Check views.py -> transfer method where ETA is being set.
	'''
	try:
		transaction_log = ''.join([from_acc, to_acc, str(amount)])
		with transaction.atomic():
			to_acc = Account.objects.select_for_update().get(account_number=to_acc)
			to_acc.balance += amount
			to_acc.save()
		unset_transaction_log(transaction_log)
	except DatabaseError, e:
		raise e

@app.task
def deposit_money(account_num, amount):
	'''
	Async deposit celery task which will be executed after ETA is completed.
	Check views.py -> deposit method where ETA is being set.
	'''
	account = None
	try:
		transaction_log = ''.join(['deposit', account_num, str(amount)])
		with transaction.atomic():
			account = Account.objects.select_for_update().get(account_number=account_num)
			account.balance += amount
			account.save()
		unset_transaction_log(transaction_log)
	except DatabaseError, e:
		raise e
