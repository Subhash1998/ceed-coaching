from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import AddStudent,FirstPaymentStatus,SecondPaymentStatus,ThirdPaymentStatus
from django.contrib import messages
from .models import Student ,StudentSms , StudentMail
from django.http import HttpResponseRedirect
import requests
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.mail import EmailMessage,EmailMultiAlternatives
from .decorators import user_is_master,user_is_student


@login_required
@user_is_master
def dashboard(request):
	student_count=Student.objects.filter().count()
	student_count_ninth=Student.objects.filter(std=9).count()
	student_count_tenth=Student.objects.filter(std=10).count()
	student_count_eleventh=Student.objects.filter(std=11).count()
	student_count_twelth=Student.objects.filter(std=12).count()
	context={
		'student_count':student_count,
		'student_count_ninth':student_count_ninth,
		'student_count_tenth':student_count_tenth,
		'student_count_eleventh':student_count_eleventh,
		'student_count_twelth':student_count_twelth
	}
	return render(request,"mysite/dashboard.html",context)

@login_required
@user_is_master
def my_password_change(request):
	form = PasswordChangeForm(request.user)
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			try:
				user = form.save()
				update_session_auth_hash(request, user)
				messages.success(request, 'Your password is successfully updated.')
				return HttpResponseRedirect(reverse('quiz_test:dashboard'))
			except Exception as e:
				print(e)	
				messages.error(request, 'Error updating password.')
		else:
			messages.error(request, 'Error updating password.')
	return render(request, 'mysite/my_password_change.html', {'form':form})


@login_required
@user_is_master
def add_student(request):
	form=AddStudent()
	if request.method=='POST':
		form=AddStudent(request.POST)
		if form.is_valid():
			try:
				student=form.save(commit=False)
				student.user=request.user
				decide=student.std
				if decide==9:
					student.total_amount=39000
				if decide==10:
					student.total_amount=39000
				if decide==11:
					student.total_amount=60000
				if decide==12:
					student.total_amount=60000
				student.due_amount=student.total_amount
				student.save()
				messages.success(request,"Student Added successfully.")
				return HttpResponseRedirect(reverse("mysite:student_list"))
			except Exception as e:
				print(e)
				messages.error(request,"Error adding Student.")
		else:
			messages.error(request,"Error adding Student.")
	return render(request,"mysite/add_student_form.html",{'form':form})


@login_required
@user_is_master
def student_list(request):
	student=Student.objects.filter()
	ninth=Student.objects.filter(std=9)
	tenth=Student.objects.filter(std=10)
	eleventh=Student.objects.filter(std=11)
	twelth=Student.objects.filter(std=12)
	context={
		'student':student,
		'ninth':ninth,
		'tenth':tenth,
		'eleventh':eleventh,
		'twelth':twelth
	}
	return render(request,"mysite/student_list.html",context)

@login_required
@user_is_master
def edit_student(request,pk):
	student = get_object_or_404(Student, pk=pk)
	form = AddStudent(request.POST or None, instance=student)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Student details editing successful.')
		return HttpResponseRedirect(reverse('mysite:student_list'))
	return render(request, 'mysite/edit_student.html', {'form':form})

@login_required
@user_is_master
def remove_student(request,pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.error(request, 'Student removed.')
    return redirect('mysite:student_list')


@login_required
@user_is_master
def send_student_sms(request,pk):
    student = get_object_or_404(Student, pk=pk)
    message = "Dear {} {}\nIt seems you enquired about our different services. " \
              "We are excited to inform you that we have some special offers for you. " \
              "Take the first step towards a fit and healthy you today. " \
              "Please visit us or give a call/missed call at 1998 to know more.\nRegards,\nIncharge"\
        .format(student.first_name, student.last_name, student.mobile)
    context = {
        'message': message,
        'student': student,
        'pk': pk
    }
    # messages.success(request, 'Message sent successfully.')
    return render(request, 'mysite/send_student_sms.html', context)

@login_required
@user_is_master
def send_sms_api(request, pk):
    student = get_object_or_404(Student, pk=pk)
    message = request.GET['message']
    if student.mobile:
        payload = {
            'sender': 'SPECTR',
            'route': '4',
            'country': '91',
            'authkey': '',
            'message': message,
            'mobiles': [[student.mobile]]
        }
        r = requests.get('http://api.msg91.com/api/sendhttp.php', params=payload)

        if (r.status_code == 200):
            s = StudentSms(
                first_name=student.first_name,
                last_name=student.last_name,
                mobile=student.mobile,
                message=message
            )
            s.save()
            messages.success(request, 'Message sent successfully.')
            return HttpResponseRedirect(reverse('mysite:student_list'))

    error = "Error sending sms. Status code: {}".r.status_code
    json = {
        'success': False,
        'error': error
    }
    messages.error(request, 'Failed sending message.')
    return HttpResponseRedirect(reverse('mysite:student_list'))

@login_required
@user_is_master
def send_bulk_sms(request):
    message = "Dear Student\nIt seems you enquired about our different services. " \
              "We are excited to inform you that we have some special offers for you. " \
              "Take the first step towards a fit and healthy you today. " \
              "Please visit us or give a call/missed call at 1998 to know more.\nRegards,\nIncharge"
    context = {
        'message': message,
    }
    # messages.success(request, 'Message sent successfully.')
    return render(request, 'mysite/bulk_message.html', context)

@login_required
@user_is_master
def bulk_sms(request):
	c=request.GET['class']
	print(c)
	if c != "All" :
		student=Student.objects.filter(std=c)
	else:
		student=Student.objects.filter()
	for s in student:
		message = request.GET['message']
		if s.mobile:
			payload = {
			    'sender': 'SPECTR',
			    'route': '4',
			    'country': '91',
			    'authkey': '210112APJgCTharC5ad321b5',
			    'message': message,
			    'mobiles': [[s.mobile]]
			}
			r = requests.get('http://api.msg91.com/api/sendhttp.php', params=payload)

			if (r.status_code == 200):
			    st = StudentSms(
			        first_name=s.first_name,
			        last_name=s.last_name,
			        mobile=s.mobile,
			        message=message
			    )
			    st.save()

	messages.success(request,"Message Sending Successful.")
	return redirect("mysite:student_list")

@login_required
@user_is_master
def send_email(request,c):
	try:
		if request.method == 'POST' and request.FILES['myfile']:
			subject = request.POST.get('subject')
			myfile = request.FILES['myfile']
			student=Student.objects.filter(std=c)
			for s in student:
				msg = EmailMessage("title", subject, to=[s.email])
				msg.attach(myfile.name, myfile.read(), myfile.content_type)
				msg.send()
				e=StudentMail(first_name=s.first_name,last_name=s.last_name,files=myfile,email=s.email,sent="Sent")
				e.save()
			messages.success(request,"Email Sent.")
			return redirect("mysite:student_list")

	except Exception as e:
		print(e)
		messages.error(request,"Failed to send email.")

	return render(request,"mysite/send_email.html")


@login_required
@user_is_master
def payment_status(request,c):
	student=Student.objects.filter(std=c)
	second_student=student.filter(first_installment=1)
	third_student=student.filter(first_installment=1,second_installment=1)
	context={
		'first_student':student,
		'second_student':second_student,
		'third_student':third_student
	}

	return render(request,"mysite/payment_status.html",context)

@login_required
@user_is_master
def first_payment_form(request,pk):
	student = get_object_or_404(Student, pk=pk)
	form = FirstPaymentStatus(request.POST or None, instance=student)
	if request.method == 'POST' and form.is_valid():
		payment=form.save()
		payment.total_paid_first=payment.paid_amount_first
		payment.total_paid_second=payment.total_paid_first
		p=payment.due_amount
		p=p-(payment.paid_amount_first)
		payment.due_amount=p
		payment.first_installment=1
		payment.save()
		messages.success(request, 'Student Payment details editing successful.')
		return HttpResponseRedirect(reverse('mysite:payment_status',kwargs={'c':student.std}))
	return render(request, 'mysite/first_payment.html', {'form':form})


@login_required
@user_is_master
def second_payment_form(request,pk):
	student = get_object_or_404(Student, pk=pk)
	form = SecondPaymentStatus(request.POST or None, instance=student)
	if request.method == 'POST' and form.is_valid():
		payment=form.save()
		p=payment.total_paid_first
		p=p+payment.paid_amount_second
		payment.total_paid_second=p
		payment.total_paid_third=payment.total_paid_second
		p=payment.due_amount
		p=p-(payment.paid_amount_second)
		payment.due_amount=p
		payment.second_installment=1
		payment.save()
		messages.success(request, 'Student Payment details editing successful.')
		return HttpResponseRedirect(reverse('mysite:payment_status',kwargs={'c':student.std}))
	return render(request, 'mysite/first_payment.html', {'form':form})

@login_required
@user_is_master
def third_payment_form(request,pk):
	student = get_object_or_404(Student, pk=pk)
	form = ThirdPaymentStatus(request.POST or None, instance=student)
	if request.method == 'POST' and form.is_valid():
		payment=form.save()
		p=payment.total_paid_second
		p=p+payment.paid_amount_third
		payment.total_paid_third=p
		p=payment.due_amount
		p=p-(payment.paid_amount_third)
		payment.due_amount=p
		payment.third_installment=1
		payment.save()
		messages.success(request, 'Student Payment details editing successful.')
		return HttpResponseRedirect(reverse('mysite:payment_status',kwargs={'c':student.std}))
	return render(request, 'mysite/first_payment.html', {'form':form})

@login_required
@user_is_master
def dues(request):
	student=Student.objects.filter()
	stu=[]
	if student:
		for s in student:
			if s.due_amount > 0:
				stu.append(s)
	return render(request,"mysite/dues.html",{'stu':stu})

