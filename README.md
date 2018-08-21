# Banking_System

##Description
This is a sample application for banking MVP. This app involves basic banking operations like, creation of account, deposit and withdraw money and transfer to some other account.
You can add/modify user from django admin page. For transfer, there is no benificiary addition as such, this is just a POST method which primarily checks if payee and receiver accounts are in the database.

This application is written using python 2.7, django, and djangorest framework. The other components involve celery for async task management queue, redis as broker for celery and also for transaction log management, and sqlite3 as database.
Please refer to ```bank/models.py``` for schema design.
