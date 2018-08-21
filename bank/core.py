'''
'''
from __future__ import absolute_import
from django.db import transaction, connection, DatabaseError
from .models import Account
from .celery import app
from celery.decorators import task
from celery import shared_task
from bank.utils import unset_transaction_log

MIN_BALANCE = 1000

class AccountOperation(object):
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
		else:
			transaction.commit()
		return account


	@classmethod
	def withdraw(cls, account_num, amount):
		with transaction.atomic():
			account = Account.objects.select_for_update().get(account_number=account_num)
			if account.balance - amount >= MIN_BALANCE:
				account.balance -= amount
				account.save()
		return account

@shared_task
def transfer_money(from_acc, to_acc, amount):
		transaction_log = ''.join([from_acc, to_acc, str(amount)])
		with transaction.atomic():
			from_acc = Account.objects.select_for_update().get(account_number=from_acc)
			to_acc = Account.objects.select_for_update().get(account_number=to_acc)
			if from_acc.balance - amount >= MIN_BALANCE:
				from_acc.balance -= amount
				from_acc.save()
				to_acc.balance += amount
				to_acc.save()
		unset_transaction_log(transaction_log)


