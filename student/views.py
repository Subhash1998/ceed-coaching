from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from mysite.decorators import user_is_student
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging, traceback
import hashlib
import requests
from random import randint
from . import config
from django.urls import reverse
from django.core.mail import EmailMessage
from .models import PaymentDetails
from datetime import date

keys = ['udf1', 'udf2', 'txnid', 'mihpayid', 'encryptedPaymentId',
        'payuMoneyId', 'net_amount_debit', 'hash', 'error_Message']

@login_required
@user_is_student
def student_dashboard(request):
	return render(request,"student/student_dashboard.html")


@login_required
@user_is_student
def pay(request):
	data = {}
	name = amount = contact = date=None
	if request.method == 'POST':
		name = request.POST.get('name')
		amount = request.POST.get('amount')
		contact = request.POST.get('contact')
		date = request.POST.get('date')
		if name and amount and contact and date:
			if not all(x.isalpha() or x.isspace() for x in name):
				messages.error(request,"Error")
				return render(request, "student/payment_form.html")
		else:
			messages.error(request,"Invalid field value")
			return render(request, "student/payment_form.html")
		try:
			txnid = get_transaction_id()
			data["txnid"] = txnid
			data["action"] = config.PAYMENT_URL_LIVE
			data["amount"] = amount
			data["productinfo"] = 'Student Payment'
			data["key"] = config.KEY
			data["firstname"] = name
			data["email"] = request.user.email
			data["phone"] = contact
			data["udf1"]=""
			data["udf2"]=""
			data["service_provider"] = config.SERVICE_PROVIDER
			hash_string = config.KEY+"|"+txnid+"|"+str(data["amount"])+"|"+data["productinfo"]+"|"
			hash_string += data["firstname"]+"|"+data["email"]+"|"
			hash_string += "||||||||||"+config.SALT
			data["hash_string"] = hash_string
			hash_= generate_hash(request, txnid,hash_string)
			data["hash"]=hash_
			failure = reverse("student:payment_failure")
			success = reverse("student:payment_success")
			data["furl"] = request.build_absolute_uri(failure)
			data["surl"] = request.build_absolute_uri(success)
		except:
				messages.error(request,"Error..")
				return render(request,"student/payment_form.html",data)
		pay_details=PaymentDetails.objects.create(user=request.user,
													name=name,
													txnid=txnid,
													amount=amount,
													email=request.user.email,
													contact=contact)
		return render(request,"student/payment.html",data)
	print("sfsbfmn")
	return render(request, "student/payment_form.html", data)

def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid


# create hash string using all the fields
def get_hash_string(request, **data):
    print(type(data))
    hash_string = config.KEY+"|"+data["txnid"]+"|"+str(float(data["amount"]))+"|"+data["productinfo"]+"|"
    hash_string += data["firstname"]+"|"+data["email"]+data["udf1"]+data["udf2"]+"|"
    hash_string += "||||||||"+config.SALT

    return hash_string

def generate_hash(request, txnid,hash_string):
    try:
        # get keys and SALT from dashboard once account is created.
        hashSequence = "key|txnid|amount|productinfo|name|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        #hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower() 
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
    return None

@csrf_exempt
def payment_success(request):
	data = {}
	data1 = []
	for key in keys:
		data1.append(request.POST.get(key))
	print(data1)
	try:
		student = PaymentDetails.objects.get(user=request.user,txnid=data1[2])
	except:
		return redirect('student:payment_failure')

	if student:
		student.mihpayid=data1[3]
		student.enc_pay_id=data1[4] 
		student.payuMoneyId=data1[5]
		student.net_amount_debit=data1[6]
		student.hash=data1[7]
		student.message="Payment Success"
		student.save()
	pay_message = "Dear {}\nYour payment for academy is successful.\nTransaction id for your payment is {}.\n" \
	              "Thankyou." \
	    .format(student.name, student.txnid)
	try:
	    payload = {
	        'sender': 'SPECTR',
		    'route': '4',
		    'country': '91',
		    'authkey': '210112APJgCTharC5ad321b5',
		    'message': pay_message,
		    'mobiles': [[student.contact]]
	    }
	    mssg = requests.get('http://api.msg91.com/api/sendhttp.php', params=payload)

	    if (mssg.status_code == 200):
	        messages.success(request, 'Transaction successful message sent.')
	except:
	    messages.warning(request, 'Show unique treansaction id in coaching to gain access.')
	try:
	    email = EmailMessage("Student Payment", pay_message, to=[student.email])
	    email.send(fail_silently=True)
	except:
	    pass
	messages.success(request, 'Transaction successful!')
	data={'student':student,'date':date.today()}
	return render(request, "student/success.html", data)


@csrf_exempt
def payment_failure(request):
	return render(request,"student/failure.html")


 