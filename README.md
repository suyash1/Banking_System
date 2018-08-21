# Banking_System

## Description
This is a sample application for banking MVP. This app involves basic banking operations like, creation of account, deposit and withdraw money and transfer to some other account.
You can add/modify user from django admin page. For transfer, there is no benificiary addition as such, this is just a POST method which primarily checks if payee and receiver accounts are in the database.

This application is written using python 2.7, django, and djangorest framework. The other components involve celery for async task management queue, redis as broker for celery and also for transaction log management, and sqlite3 as database.
Please refer to ```bank/models.py``` for schema design.

## Setup
You will be needing ```pip``` to be installed in your system for smooth setup. If you want to use [virtual environment](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv), the set up is well defined in the link.

Run the following commands after starting virtualenv (if not virtualenv, then run the following as sudo) 

```
pip install -r requirements.txt
```
Once requirements are installed, go to ```Banking_System``` project repository where you can see ```bank``` app, ```manage.py``` file etc. In order to run the app locally/remotely, open ```Banking_System/settings.py``` and look for ```ALLOWED_HOSTS``` for settings instruction

Before starting app, you will need to fire up ```redis-server``` and ```clery worker```.
To install redis, please follow the redis-server installation based upon your OS. celery will be installed through requirements.txt
Once redis-server is installed, run the following in a separate tab or in background using screen/supervisord/nohup 

```
redis-server
```

Once redis server is up, start celery worker (from Banking_System project repo) as follows in a separate tab. For running as daemon, please look up how to run celery in background.
```
celery --app=bank  worker --loglevel=INFO
```

If you want to run app locally, fire up:
```
python manage.py runserver
```
