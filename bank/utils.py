'''
@author suyash
Utility functions reside here

TODO:
1. Redis connection pooling
'''

import redis
from datetime import datetime
from bank.models import Account

r = redis.StrictRedis(host='localhost', port=6379, db=1)

def set_transaction_log(key):
	r.set(key, str(datetime.now()))

def unset_transaction_log(key):
	r.delete(key)

def is_duplicate_transaction(key):
	return True if r.get(key) else False

def is_valid_account(acc_num):
	try:
		acc = Account.objects.get(account_number=acc_num)
		if acc:
			return True
		else:
			return False
	except:
		return False
