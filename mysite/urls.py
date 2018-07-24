from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='mysite'

urlpatterns = [
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'add_student_form/$', views.add_student, name='add_student'),
    url(r'student_list/$', views.student_list, name='student_list'),
    url(r'edit_student/(?P<pk>\d+)/$', views.edit_student, name='edit_student'),
    url(r'remove_student/(?P<pk>\d+)/$', views.remove_student, name='remove_student'),
    url(r'send_student_sms/(?P<pk>\d+)/$', views.send_student_sms, name='send_student_sms'),
    url(r'send_bulk_sms/$', views.send_bulk_sms, name='send_bulk_sms'),
    url(r'bulk_sms/$', views.bulk_sms, name='bulk_sms'),
    url(r'send_sms_api/(?P<pk>\d+)/$', views.send_sms_api, name='send_sms_api'),
    url(r'send_email/(?P<c>\d+)/$', views.send_email, name='send_email'),
    url(r'payment_status/(?P<c>\d+)/$', views.payment_status, name='payment_status'),
    url(r'first_payment/(?P<pk>\d+)/$', views.first_payment_form, name='first_payment_form'),
    url(r'second_payment/(?P<pk>\d+)/$', views.second_payment_form, name='second_payment_form'),
    url(r'third_payment/(?P<pk>\d+)/$', views.third_payment_form, name='third_payment_form'),
    url(r'dues/$', views.dues, name='dues'),
    url(r'change_password/$', views.my_password_change, name='my_password_change'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)