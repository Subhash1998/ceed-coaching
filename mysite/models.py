from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

ichoice=(
	(0,'Not Paid'),
	(1,'Paid'),
	)

user_type_choices = (
    ('master', 'master'),
    ('Others', 'Others')
)


class User(AbstractUser):
    user_type = models.CharField(max_length=50, choices=user_type_choices, default='Others')


class Student(models.Model):
	user = models.ForeignKey(User, related_name='teacher', null=True, on_delete=models.CASCADE)
	first_name=models.CharField(max_length=150)
	last_name=models.CharField(max_length=150,blank=True)
	email=models.EmailField()
	mobile=PhoneNumberField(blank=True)
	parent_mobile=PhoneNumberField()
	address=models.CharField(max_length=500)
	std=models.IntegerField(default=0,validators = [MaxValueValidator(12)])
	date_of_join=models.DateField(default=timezone.now)

	total_amount=models.IntegerField(default=0)
	paid_amount_first=models.IntegerField(default=0)
	paid_amount_second=models.IntegerField(default=0)
	paid_amount_third=models.IntegerField(default=0)
	total_paid_first=models.IntegerField(default=0)
	total_paid_second=models.IntegerField(default=0)
	total_paid_third=models.IntegerField(default=0)
	due_amount=models.IntegerField(default=0)
	first_installment=models.IntegerField(default=0,choices=ichoice)
	second_installment=models.IntegerField(default=0,choices=ichoice)
	third_installment=models.IntegerField(default=0,choices=ichoice)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name 


class StudentSms(models.Model):
	first_name=models.CharField(max_length=150)
	last_name=models.CharField(max_length=150,blank=True)
	mobile=PhoneNumberField()
	message=models.CharField(max_length=1000)

	def __str__(self):
		return self.first_name + ' ' + self.last_name


class StudentMail(models.Model):
	first_name=models.CharField(max_length=150)
	last_name=models.CharField(max_length=150,blank=True)
	files=models.FileField(upload_to='documents/')
	email=models.EmailField()
	sent=models.CharField(max_length=100,default="Not Sent")
	def __str__(self):
		return str(self.email)


