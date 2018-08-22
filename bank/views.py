# -*- coding: utf-8 -*-
'''
@author suyash
This consists of all the methods mapped to url end points
mentioned in urls.py file
'''
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import AccountSerializer
from .models import Account
from bank.core import AccountOperation, transfer_money, deposit_money
from django.utils.six import BytesIO
import json
import traceback
from datetime import datetime, timedelta
from bank.utils import set_transaction_log, is_duplicate_transaction, is_valid_account


@csrf_exempt
@api_view(['GET', 'POST'])
def account_list(request):
	if request.method == 'GET':
		acc = Account.objects.all()
		serializer = AccountSerializer(acc, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		data = JSONParser().parse(request.data)
		serializer = AccountSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)

		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET'])
def account_info(request, accNum):
	acc = None
	if is_valid_account(accNum):
		try:
			acc = Account.objects.get(account_number=accNum)
		except Account.DoesNotExist:
			return HttpResponse(status=404) 
	
		if request.method == 'GET':
			print 'here', acc
			serializer = AccountSerializer(acc)
			return Response(serializer.data)
	else:
		return Response('Invalid account')


@csrf_exempt
@api_view(['POST'])
def deposit(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		account_number = json_data.get('account_number')
		amount = json_data.get('amount')
		if is_valid_account(account_number):
			try:
				if not is_duplicate_transaction(''.join(['deposit', account_number, str(amount)])):
					set_transaction_log(''.join(['deposit', account_number, str(amount)]))
					deposit_money.apply_async((account_number, amount), eta=datetime.utcnow() + timedelta(seconds=20))
					return Response('Deposit request accepted, please check your account in few seconds')
				else:
					return Response('Looks like same request has already been made, please wait till the earlier request is completed')
			except Exception, e:
				print traceback.print_exc()
				return Response('Deposit failed')
		else:
			return Response('Invalid account')



@csrf_exempt
@api_view(['POST'])
def transfer(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		from_acc = json_data.get('from_acc')
		to_acc = json_data.get('to_acc')
		amount = json_data.get('amount')
		is_valid_from_acc = is_valid_account(from_acc)
		is_valid_to_acc = is_valid_account(to_acc)
		if is_valid_from_acc and is_valid_to_acc:
			try:
				if not is_duplicate_transaction(''.join([from_acc, to_acc, str(amount)])) and\
					'Success' in AccountOperation.withdraw(account_num=from_acc, amount=amount):
					set_transaction_log(''.join([from_acc, to_acc, str(amount)]))
					transfer_money.apply_async((from_acc, to_acc, amount), eta=datetime.utcnow() + timedelta(minutes=1))
					return Response('Transfer queued')
				else:
					return Response('You have made similar transaction which is pending currently. Please wait till it is completed.')
			except Exception, e:
				print traceback.print_exc()
				return HttpResponse(status=503)
		else:
			return Response('Invalid sender account') if not is_valid_from_acc else Response("Invalid receiver's account")
