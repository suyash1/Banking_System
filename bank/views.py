# -*- coding: utf-8 -*-
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
from bank.core import AccountOperation, transfer_money
from django.utils.six import BytesIO
import json
import traceback
from datetime import datetime, timedelta
from bank.utils import set_transaction_log, is_duplicate_transaction

class AccountView(generics.ListCreateAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer

	#def create(self, serializer):
#		print serializer.request.__dict__
#		serializer.save()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
@api_view(['GET', 'POST'])
def acc(request):
	if request.method == 'GET':
		acc = Account.objects.all()
		serializer = AccountSerializer(acc, many=True)
		#return JsonResponse(serializer.data, safe=False)
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
def acc_info(request, accNum):
	try:
		acc = Account.objects.get(account_number=accNum)
	except Account.DoesNotExist:
		return HttpResponse(status=404) 
	
	if request.method == 'GET':
		serializer = AccountSerializer(acc)
		#return JsonResponse(serializer.data)
		return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def deposit(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		print json_data
		account_number = json_data.get('account_number')
		amount = json_data.get('amount')
		try:
			account_data = AccountOperation.deposit(account_num=account_number, amount=amount)
			serializer = AccountSerializer(account_data)
			return Response(serializer.data)
		except Exception, e:
			print traceback.print_exc()
			return HttpResponse(status=503)



@csrf_exempt
@api_view(['POST'])
def transfer(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		print json_data
		from_acc = json_data.get('from_acc')
		to_acc = json_data.get('to_acc')
		amount = json_data.get('amount')
		try:
			#transfer_status = AccountOperation.transfer.delay(from_acc, to_acc, amount)
			if not is_duplicate_transaction(''.join([from_acc, to_acc, str(amount)])):
				set_transaction_log(''.join([from_acc, to_acc, str(amount)]))
				transfer_money.apply_async((from_acc, to_acc, amount), eta=datetime.utcnow() + timedelta(minutes=1))
				return Response('Transfer queued')
			else:
				return Response('You have made similar transaction which is pending currently. Please wait till it is completed.')
		except Exception, e:
			print traceback.print_exc()
			return HttpResponse(status=503)
