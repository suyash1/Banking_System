import redis
from datetime import datetime

r = redis.StrictRedis(host='localhost', port=6379, db=1)

def set_transaction_log(key):
	r.set(key, str(datetime.now()))

def unset_transaction_log(key):
	r.delete(key)

def is_duplicate_transaction(key):
	return True if r.get(key) else False
