from .models import Student , StudentMail
from django import forms

class AddStudent(forms.ModelForm):

	class Meta:
		model=Student
		fields=["first_name","last_name","email","mobile","parent_mobile","address","std","date_of_join"]
		help_texts = {
            'first_name': 'Enter student first name',
            'last_name': 'Enter student last name',
            'email': 'Enter email id of student',
            'mobile': 'Must be 10 or 13 digit followed by country code',
            'parent_mobile': 'Must be 10 or 13 digit followed by country code',            
            'address': 'Home address of student',
            'std': 'Enter class student is in',
            'date_of_join':'Enter date of joining of student to coaching center',
        }


class FirstPaymentStatus(forms.ModelForm):

    class Meta:
        model=Student
        fields=["paid_amount_first",]


class SecondPaymentStatus(forms.ModelForm):

    class Meta:
        model=Student
        fields=["paid_amount_second",]


class ThirdPaymentStatus(forms.ModelForm):

    class Meta:
        model=Student
        fields=["paid_amount_third",]