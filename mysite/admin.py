from django.contrib import admin
from .models import Student ,StudentSms ,StudentMail,User

admin.site.register([Student,StudentSms,StudentMail,User])
