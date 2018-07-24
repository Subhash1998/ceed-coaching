from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class PaymentDetails(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	name=models.CharField(max_length=150)
	txnid=models.CharField(max_length=200)
	amount=models.FloatField(default=0.0)
	email=models.EmailField()
	contact=PhoneNumberField()
	message=models.CharField(max_length=100)
	mihpayid=models.CharField(max_length=100)
	enc_pay_id=models.CharField(max_length=100)
	payuMoneyId=models.CharField(max_length=100)
	net_amount_debit=models.CharField(max_length=100)
	hash=models.CharField(max_length=100)

	def __str__(self):
		return str(self.txnid)
