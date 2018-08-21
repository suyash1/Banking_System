from rest_framework import serializers
from .models import Account, Transactions

ms = serializers.ModelSerializer

MINIMUM_BALANCE = 1000

class AccountSerializer(ms):
	'''
	'''
	account_number = serializers.CharField(read_only=True)
	balance = serializers.FloatField(required=True)

	def create(self, validated_data):
		acc = Account.objects.create(**validated_data)
		Transactions.objects.create(account_number=acc, amount=balance, action='created')
		return acc

	def credit(self, instance, validated_data):
		instance.balance = validated_data.get('amount')
		instane.save()
		return instance

	def debit(self, instance, validated_data):
		debit_amount = validated_data.get('amount')
		if not instance.balance - amount < MINIMUM_BALANCE:
			instance.balance -= amount
			instance.save()
			return instance
		return 'Debit not allowed below minimum balance'

	class Meta:
		'''
		'''
		model = Account
		fields = '__all__'

