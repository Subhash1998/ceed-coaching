from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='student'

urlpatterns = [
	url(r'success/$', views.payment_success, name="payment_success"),
    url(r'failure/$', views.payment_failure, name="payment_failure"),
    url(r'pay/$', views.pay, name="pay"),
    url(r'student_dashboard/$', views.student_dashboard, name='student_dashboard'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)