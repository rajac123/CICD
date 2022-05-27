from django.shortcuts import render
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.loader import get_template
from synap import settings
import calendar
import requests
from rest_framework.views import APIView
# import razorpay
from itertools import chain
from django_mysql.locks import Lock
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import pandas
import xlwt
from dateutil.relativedelta import *
import dateutil.parser
from dateutil import parser
from django.http import Http404
from django.http import HttpResponse,JsonResponse
from django.db import connection
from rest_framework import status
import json
import csv 
from rest_framework import viewsets
from collections import defaultdict
from .import models
from .import serializer1
from .import video
from django.db.models import Q
import datetime
import http.client
import random
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
# from fuzzywuzzy import fuzz,process
# import barcode
# from barcode.writer import ImageWriter
import socket
import os
import time
from django.http import HttpRequest
import urllib.request
import platform
from django.template.loader import get_template
# from reportlab.graphics import renderPM
from base64 import b64encode
import pdfkit
from functools import reduce
import operator
from pandas.tseries import offsets
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (From, To, PlainTextContent, HtmlContent, Mail)
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
import string
from rest_framework.parsers import JSONParser
from pytz import timezone
from datetime import  datetime as dt
import uuid
from Crypto.Cipher import AES
import base64
from io import BytesIO
from xhtml2pdf import pisa
from itertools import repeat

import decimal
def decimal_default(o):
  if isinstance(o, decimal.Decimal):
    return o.__str__()

def encrypt(key, plaintext):
  crypto = AES.new(key, AES.MODE_CTR, counter=lambda: key)
  return (base64.b64encode(crypto.encrypt(plaintext))).decode()
def decrypt(key, ciphertext):
  crypto = AES.new(key, AES.MODE_CTR, counter=lambda: key)
  return (crypto.decrypt(base64.b64decode((ciphertext)))).decode()

def TimeZoneConvert(hospital_n_key):
  hospital = models.HospitalMaster.objects.filter(hospital_n_key=hospital_n_key)
  return (datetime.datetime.now(timezone(hospital[0].time_zone)).strftime('%Y-%m-%d %H:%M:%S'))

def DefaultTimeZone():
  return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def DoctorRoleQuery(org_n_key):
  mdroles = models.GERoles.objects.filter(Q(role_check='Yes') & Q(org_n_key='ORGID-1')).values_list('roles_name',flat=True)
  return list(set(mdroles))

def TimeZoneBloodbank(bloodbank_n_key):
  bloodbank = models.BloodBank_Master.objects.filter(bloodbank_n_key=bloodbank_n_key)
  return (datetime.datetime.now(timezone(bloodbank[0].time_zone)).strftime('%Y-%m-%d %H:%M:%S'))

@csrf_exempt
def OrganizationRegister(request):
  request = json.loads(request.body.decode('utf-8'))
  if request:
    email = models.OrganizationMaster.objects.filter(email=request['email'])
    if not email:
      user = models.OrganizationMaster.objects.filter(phone_num=request['phone_num'])
      if not user:
        phoneno = request["phone_num"]
        dial_code = request["dial_code"]
        conn = http.client.HTTPConnection("2factor.in")
        conn.request(
            "POST", "https://2factor.in/API/V1/19ff5a0a-b0eb-11e7-94da-0200cd936042/SMS/" + str(dial_code + phoneno) + "/AUTOGEN/Mrecs")
        res = conn.getresponse()
        data = res.read()
        decode_data = data.decode()
        return HttpResponse(json.dumps({"data": json.loads(decode_data)}), content_type="application/json")
      else:
        return HttpResponse(json.dumps({'Status': "This Phone Number is already exists!"}), content_type="application/json")
    else:
      return HttpResponse(json.dumps({'Status': "This email address is already exists !"}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({'Status': "Failed to Post"}), content_type="application/json")

@csrf_exempt
def verify_org(request):
  conn = http.client.HTTPConnection("2factor.in")
  request = json.loads(request.body.decode('utf-8'))
  sendOTP = request.get("sendOTP")
  typedOTP = request.get("typedOTP")
  conn.request("POST", "https://2factor.in/API/V1/19ff5a0a-b0eb-11e7-94da-0200cd936042/SMS/VERIFY/" +
               sendOTP + '/' + typedOTP)
  res = conn.getresponse()
  data = res.read()
  decode_data = data.decode()
  json_data = json.loads(decode_data)
  if json_data['Details'] == 'OTP Matched':
    org_create = models.OrganizationMaster.objects.create(first_name=request['first_name'], last_name=request['last_name'],
      email=request['email'], phone_num=request['phone_num'],
      job_function=request['job_function'], speciality=request['speciality'],
      org_name=request['org_name'],dial_code = request['dial_code'],no_of_providers=request['no_of_providers'],
      created_on=DefaultTimeZone(), confirmation="Agree",online_practice='Yes',online_bloodbank='Yes'
      )

    employeecreate = models.EmployeesMaster.objects.create(org_n_key=org_create.org_n_key,first_name=request['first_name'],last_name=request['last_name'], email=request['email'], phone_number=request['phone_num'],
     password=request['password'],is_new_user='No', created_on=DefaultTimeZone(), role='Master',created_by_id='Admin',created_by_name='Synapstics',is_active=1)


    today = datetime.date.today()
    expiry_date = today + datetime.timedelta(days=6)

    str_data = request['org_name']
    split_data = str_data.split(' ')
    fulldata = []

    createuser = User.objects.create_user(password=request['password'], username=employeecreate.user_name, email=request['email'])
    createuser.save()
    createuser_id=createuser.id
    createuser_pk = createuser.pk
    sendgrid_client = SendGridAPIClient(
            api_key='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')
    message = Mail(
          from_email='support@synapstics.com',
          to_emails=request['email'],
          subject='',
          html_content='<strong>Verification Mail</strong>')
    message.dynamic_template_data = {
          'username':employeecreate.user_name,
          'password':request['password']
         
    }
    message.template_id = 'd-8f04908d44814d769e440604b63bd990'
    response = sendgrid_client.send(message=message)

    sms_setting = models.SmsSettings.objects.create(thanks_sms_content = "Thanks for visiting "+str(request['org_name']),org_n_key=org_create.org_n_key,
    reminder_sms_content = "You have an appointment in "+str(request['org_name']),org_name=request['org_name'],registration_sms_content="You are added as an employee in "+str(request['org_name']),
    remaining_sms=1000,total_count =1000,created_by_id=employeecreate.employee_n_key,created_by_name=employeecreate.first_name,
    created_on = DefaultTimeZone())

    employeequeryset=models.EmployeesMaster.objects.all().order_by('-employee_id')[:1]
    details_of_employee = serializers.serialize('json',employeequeryset)
    
      
    user = authenticate(
        username=employeecreate.user_name, password=request['password'])

    if user:
      token, created = Token.objects.get_or_create(user=user)
      token_string = str(token)
      valid_token = token_string.replace("\\", "")
      return HttpResponse(json.dumps({"data": json.loads(decode_data), "token": valid_token,"info":json.loads(details_of_employee)}), content_type='application/json')
    else:
      return HttpResponse(json.dumps({"status": "Username and password mismatched"}), content_type="application/json")
  else:
    hello = {"data":{"status": "OTP Mismatched"}}
    return HttpResponse(json.dumps(hello), content_type="application/json")

@csrf_exempt
def ValidatePassword(request):
  payload = json.loads(request.body.decode('utf-8'))
  if payload:
    employees=models.OrganizationMaster.objects.all()
    duppemployee=[]
    for i in employees:
      if i.phone_num == payload['phone_num'] or i.email == payload['email']:
          duppemployee.append('You have Been Already Registered Please Login Your Account')
          break;
      if i.phone_num == payload['phone_num'] and i.email == payload['email']:
          duppemployee.append('You have Been Already Registered Please Login Your Account')
          break;
  return HttpResponse(json.dumps({"status":duppemployee}),content_type='application/json')

# multi product
@csrf_exempt
def sendrazor(request):
  payload = json.loads(request.body.decode('utf-8'))
  payment_id=payload["payment_id"]
  amount=payload["amount"]
  client = razorpay.Client(auth=("rzp_live_2A3otkvCaR2SIR", "rNjgz5MeXpp8tQ0uPSUaY19s"))
  paymentdata = client.payment.capture(payment_id, (str(amount)+'00'))
  return Payment_Update(payload,paymentdata['status'])

def Payment_Update(request1,status1):
  requests = request1
  request = requests['payment']
  status = status1
  discount = requests['disc_amount']
  today = datetime.date.today()
  fulldata = []
  if status == 'captured':
    for i in range(0, len(request)):
      if request[i]['type'] == 'month':
        pricing_data = models.MdPaymentPricing.objects.filter(Q(payment_pricing_n_key=request[i]['data']['payment_pricing_n_key']))
        expire_date=datetime.date.today()
        final_expiry_date=datetime.date.today()
        for j in pricing_data:
          expire_date=j.expire_date
        if expire_date <= today:
          final_expiry_date = today + datetime.timedelta(days=30)
        else:
          final_expiry_date = expire_date + datetime.timedelta(days=30)
        plan_data = models.PlanDetails.objects.filter(Q(produt_name=request[i]['data']['project_name']))
        planlist_class = serializer1.PlanDetailsSerializer(plan_data, many=True)
        plan_name=''
        price=''
        final_price=''
        for k in plan_data:
          plan_name=k.plan_name
          price=k.price
        splited_planname=plan_name.split(',')
        splited_price=price.split(',')
        for n in range(0, len(splited_planname)):
          if splited_planname[n] == request[i]['plan_name']:
            final_price=int(splited_price[n])
        adjustment=final_price - request[i]['amount']
        payment_pricing = models.MdPaymentPricing.objects.filter(payment_pricing_n_key=request[i]['data']['payment_pricing_n_key']).update(project_name=request[i]['data']['project_name'],
         plan_name=request[i]['plan_name'], current_plan=request[i]['plan_name'],org_n_key=requests['org_n_key'], 
         payment_date=datetime.datetime.today(), subscrib_type=request[i]['type'], currentplan_ammount=final_price,  
         paid_ammount=request[i]['amount'], gst=18,status='Payment Success', full_name=request[i]['data']['full_name'], short_name=request[i]['data']['short_name'],
         expire_date=final_expiry_date,adjustments=adjustment,reason='Current Plan',
         modified_by_id=request[i]['created_by_id'], modified_by_name=request[i]['created_by_name'], modified_on=datetime.datetime.today())
        payment_history = models.MdPaymentHistory.objects.create(project_name=request[i]['data']['project_name'],
         plan_name=request[i]['plan_name'], current_plan=request[i]['plan_name'],org_n_key=requests['org_n_key'],
         payment_date=datetime.datetime.today(), subscrib_type=request[i]['type'], currentplan_ammount=final_price,
         paid_ammount=request[i]['amount'], gst=18,status='Payment Success',discount_amount=discount, full_name=request[i]['data']['full_name'], short_name=request[i]['data']['short_name'],
         expire_date=final_expiry_date,adjustments=adjustment,reason='Current Plan', created_by_id=request[i]['created_by_id'], created_by_name=request[i]['created_by_name'], created_on=DefaultTimeZone())
      elif request[i]['type'] == 'year':
        pricing_data1 = models.MdPaymentPricing.objects.filter(Q(payment_pricing_n_key=request[i]['data']['payment_pricing_n_key']))
        expire_date1=datetime.date.today()
        final_expiry_date1=datetime.date.today()
        for j in pricing_data1:
          expire_date1=j.expire_date
        if expire_date1 <= today:
          final_expiry_date1 = today + datetime.timedelta(days=365)
        else:
          final_expiry_date1 = expire_date1+ datetime.timedelta(days=365)
        plan_data1 = models.PlanDetails.objects.filter(Q(produt_name=request[i]['data']['project_name']))
        planlist_class1 = serializer1.PlanDetailsSerializer(plan_data1, many=True)
        plan_name1=''
        price1=''
        final_price1=''
        for k in plan_data1:
          plan_name1=k.plan_name
          price1=k.price
        splited_planname1=plan_name1.split(',')
        splited_price1=price1.split(',')
        for n in range(0, len(splited_planname1)):
          if splited_planname1[n] == request[i]['plan_name']:
            final_price1=splited_price1[n]
        final_year = int(final_price1)*12
        adjustments = final_year - request[i]['amount']
        payment_pricing = models.MdPaymentPricing.objects.filter(payment_pricing_n_key=request[i]['data']['payment_pricing_n_key']).update(project_name=request[i]['data']['project_name'],
         plan_name=request[i]['plan_name'], current_plan=request[i]['plan_name'],org_n_key=requests['org_n_key'], 
         payment_date=datetime.datetime.today(), subscrib_type=request[i]['type'], currentplan_ammount=final_year, 
         paid_ammount=request[i]['amount'], gst=18,status='Payment Success', full_name=request[i]['data']['full_name'], short_name=request[i]['data']['short_name'],
         expire_date=final_expiry_date1,adjustments=adjustments,reason='Current Plan', 
         modified_by_id=request[i]['created_by_id'], modified_by_name=request[i]['created_by_name'], modified_on=datetime.datetime.today())
        payment_history = models.MdPaymentHistory.objects.create(project_name=request[i]['data']['project_name'],
         plan_name=request[i]['plan_name'], current_plan=request[i]['plan_name'],org_n_key=requests['org_n_key'], 
         payment_date=datetime.datetime.today(), subscrib_type=request[i]['type'], currentplan_ammount=final_year, 
         paid_ammount=request[i]['amount'], gst=18,status='Payment Success',discount_amount=discount, full_name=request[i]['data']['full_name'], short_name=request[i]['data']['short_name'],
         expire_date=final_expiry_date1,adjustments=adjustments,reason='Current Plan', created_by_id=request[i]['created_by_id'], created_by_name=request[i]['created_by_name'], created_on=DefaultTimeZone())
    return HttpResponse(json.dumps({"status":"Payment Success"}),content_type="application/json")
  else:
    for i in range(0, len(request)):
      if request[i]['type'] == 'month':
        pricing_data = models.MdPaymentPricing.objects.filter(Q(payment_pricing_n_key=request[i]['data']['payment_pricing_n_key']))
        expire_date=datetime.date.today()
        final_expiry_date=datetime.date.today()
        for j in pricing_data:
          expire_date=j.expire_date
        if expire_date <= today:
          final_expiry_date = today + datetime.timedelta(days=30)
        else:
          final_expiry_date = expire_date + datetime.timedelta(days=30)
        plan_data = models.PlanDetails.objects.filter(Q(produt_name=request[i]['data']['project_name']))
        planlist_class = serializer1.PlanDetailsSerializer(plan_data, many=True)
        plan_name=''
        price=''
        final_price=''
        for k in plan_data:
          plan_name=k.plan_name
          price=k.price
        splited_planname=plan_name.split(',')
        splited_price=price.split(',')
        for n in range(0, len(splited_planname)):
          if splited_planname[n] == request[i]['plan_name']:
            final_price=int(splited_price[n])
        adjustment = final_price - request[i]['amount']
        payment_history = models.MdPaymentHistory.objects.create(project_name=request[i]['data']['project_name'],
         plan_name=request[i]['plan_name'], current_plan=request[i]['plan_name'],org_n_key=requests['org_n_key'], 
         payment_date=datetime.datetime.today(), subscrib_type=request[i]['type'], currentplan_ammount=final_price, 
         paid_ammount=request[i]['amount'], gst=18,status='Payment Faild',discount_amount=discount, full_name=request[i]['data']['full_name'], short_name=request[i]['data']['short_name'],
         expire_date=final_expiry_date,adjustments=adjustment,reason='Current Plan', created_by_id=request[i]['created_by_id'], created_by_name=request[i]['created_by_name'], created_on=DefaultTimeZone())
      elif request[i]['type'] == 'year':
        pricing_data1 = models.MdPaymentPricing.objects.filter(Q(payment_pricing_n_key=request[i]['data']['payment_pricing_n_key']))
        expire_date1=datetime.date.today()
        final_expiry_date1=datetime.date.today()
        for j in pricing_data1:
          expire_date1=j.expire_date
        if expire_date1 <= today:
          final_expiry_date1 = today + datetime.timedelta(days=365)
        else:
          final_expiry_date1 = expire_date1+ datetime.timedelta(days=365)
        plan_data1 = models.PlanDetails.objects.filter(Q(produt_name=request[i]['data']['project_name']))
        planlist_class1 = serializer1.PlanDetailsSerializer(plan_data1, many=True)
        plan_name1=''
        price1=''
        final_price1=''
        for k in plan_data1:
          plan_name1=k.plan_name
          price1=k.price
        splited_planname1=plan_name1.split(',')
        splited_price1=price1.split(',')
        for n in range(0, len(splited_planname1)):
          if splited_planname1[n] == request[i]['plan_name']:
            final_price1=splited_price1[n]
        final_year = int(final_price1)*12
        adjustments = final_year - request[i]['amount']
        payment_history = models.MdPaymentHistory.objects.create(project_name=request[i]['data']['project_name'],
         plan_name=request[i]['plan_name'], current_plan=request[i]['plan_name'],org_n_key=requests['org_n_key'],
         payment_date=datetime.datetime.today(), subscrib_type=request[i]['type'], currentplan_ammount=final_year,
         paid_ammount=request[i]['amount'], gst=18,status='Payment Faild',discount_amount=discount, full_name=request[i]['data']['full_name'], short_name=request[i]['data']['short_name'],
         expire_date=final_expiry_date1,adjustments=adjustments,reason='Current Plan', created_by_id=request[i]['created_by_id'], created_by_name=request[i]['created_by_name'], created_on=DefaultTimeZone())
    return HttpResponse(json.dumps({"status":"Payment Failed"}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def discountcalculate(request):
    payload = json.loads(request.body.decode('utf-8'))
    fulldata = []
    today=models.Discounts.objects.filter(Q(discount_code=payload['discount_code']) & Q(discount_status='Active') & Q(org_n_key=payload['org_n_key'])).values('discount_percentage')
    
    if today:
      amount = ((float(payload['sub_total'])) * float(today[0]['discount_percentage']) / 100)
      final_amount = int(payload['sub_total']) - int(amount)
      gst_amount = int((int(final_amount) * 18) / 100)
      total_amount = round(gst_amount + int(final_amount))
      return HttpResponse(json.dumps({"status":"success","amount":total_amount,"discount_amount":int(amount)}), content_type='application/json')
    else:
      final_amount = payload['sub_total']
      gst_amount = int((final_amount * 18) / 100)
      total_amount = round(gst_amount + final_amount)
      return HttpResponse(json.dumps({"status": "No Coupan Code Found", "amount": total_amount}), content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def upgradeplanchecking(request):
    payload = json.loads(request.body.decode('utf-8'))
    fulldata = []
    future_plan = payload['future_plan']
    businessdata=models.MdPaymentPricing.objects.filter(Q(clinical_short_name=payload['clinical_short_name'])).order_by('-payment_pricing_id')[:1]
    current_plan =''
    
    for i in businessdata:
      current_plan = i.current_plan
    if current_plan == 'business' and future_plan == 'growing' or future_plan == 'enterprise':
      return HttpResponse(json.dumps({"status":serializer1.MdPaymentPricingSerializer(businessdata,many=True).data}), content_type='application/json')
    elif current_plan == 'free' and future_plan == 'business' or future_plan == 'growing' or future_plan == 'enterprise':
      return HttpResponse(json.dumps({"status":serializer1.MdPaymentPricingSerializer(businessdata,many=True).data}), content_type='application/json')
    elif current_plan == 'growing' and future_plan == 'enterprise':
      return HttpResponse(json.dumps({"status":serializer1.MdPaymentPricingSerializer(businessdata,many=True).data}), content_type='application/json')
    elif current_plan == 'growing' and future_plan == 'business':
      return HttpResponse(json.dumps({"status":"Cannot Degrade"}), content_type='application/json')
    elif (current_plan == 'enterprise' and (future_plan == 'growing' or future_plan == 'business' or future_plan == 'free')):
      return HttpResponse(json.dumps({"status":"Cannot Degrade"}), content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def Discount_Details(request):
    payload = json.loads(request.body.decode('utf-8'))
    fulldata = []
    discount_details=models.Discounts.objects.filter(Q(discount_status='Active') & Q(org_n_key=payload['org_n_key']))
    if discount_details:
      serializer = serializers.serialize('json',discount_details)
      return HttpResponse(serializer, content_type='application/json')
    else:
      return HttpResponse(json.dumps(""), content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def buy_expire_calculate(request):
    payload = json.loads(request.body.decode('utf-8'))
    fulldata = []
    fulldata1 = []
    keys = 'rzp_live_2A3otkvCaR2SIR'
    key_values = 'rNjgz5MeXpp8tQ0uPSUaY19s'
    today = datetime.date.today()
    seven_days = today + relativedelta(days=7)
    history=[]
    paydata=models.MdPaymentHistory.objects.filter(Q(created_by_id=payload['employee_n_key']) & Q(org_n_key=payload['org_n_key']))
    history=serializer1.MdPaymentHistorySerializer(paydata, many=True)
    todaydata=[]
    if payload['payment_n_key'] != '' and payload['payment_n_key'] != None:
      todaydata = models.MdPaymentPricing.objects.filter(Q(payment_pricing_n_key=payload['payment_n_key']) & Q(org_n_key=payload['org_n_key']))
    payment_n_key = ''
    if len(todaydata) > 0:
      class_data = serializer1.MdPaymentPricingSerializer(todaydata, many=True)
      full_name = ''
      short_name = ''
      subscrib_type = ''
      expire_date = ''
      project_name = ''
      current_plan = ''
      for j in todaydata:
        full_name = j.full_name
        short_name = j.short_name
        subscrib_type = j.subscrib_type
        expire_date = j.expire_date
        project_name = j.project_name
        payment_n_key = j.payment_pricing_n_key
        current_plan = j.current_plan
      plan_data = models.PlanDetails.objects.filter(
          Q(produt_name=project_name))
      planlist_class = serializer1.PlanDetailsSerializer(plan_data, many=True)
      plan_name = ''
      price = ''
      final_price = ''
      for k in plan_data:
        plan_name = k.plan_name
        price = k.price
      splited_planname = plan_name.split(',')
      splited_price = price.split(',')
      for n in range(0, len(splited_planname)):
        if splited_planname[n] == current_plan:
          final_price = splited_price[n]
      amount = int(final_price)*12
      s = expire_date
      expire_date_final1 = s.strftime("%d/%m/%Y")
      gst_amount = int((amount * 18) / 100)
      total_amount = round(gst_amount + amount)
      if subscrib_type == 'free':
        if expire_date <= today:
          fulldata.append({"data": class_data.data, "amount": total_amount, "sub_total": amount, "plan_list": planlist_class.data,
                           "message": "You are currently using our " + subscrib_type+" plan "+full_name+" your subscription expired on "+str(expire_date_final1)})
        else:
          fulldata.append({"data": class_data.data, "amount": total_amount, "sub_total": amount, "plan_list": planlist_class.data, "message": "Your " +
                           full_name+" is getting expires on "+str(expire_date_final1)+" do you want to add it your existing purchase cart"})
      else:
        expire_date = ''
        for i in todaydata:
          expire_date = i.expire_date
        if expire_date > today:
          futureplan_ammount = amount
          subscrib_types = 'year'
          payment_date = datetime.date.today()
          expire_date = datetime.date.today()
          price = ''
          subscrib_type = ''
          perday_costof_currentplan = ''
          perday_costof_futureplan = ''
          currentplan_ammount=''
          for i in todaydata:
            finalpayment_date = i.payment_date
            payment_date = finalpayment_date
            currentplan_ammount =i.currentplan_ammount
            finalexpire_date = i.expire_date
            expire_date = finalexpire_date
            subscrib_type = i.subscrib_type
            price = i.paid_ammount
          new_plandate = datetime.date.today()
          paid_ammount = price
          upgrade_date = expire_date - new_plandate
          upgrade = upgrade_date.days
          currentplan_days = new_plandate - payment_date
          current = currentplan_days.days
          if subscrib_type == 'month':
            perday_costof_currentplan = (currentplan_ammount/30)
          if subscrib_type == 'year':
            perday_costof_currentplan = (currentplan_ammount/365)
          if subscrib_types == 'year':
            perday_costof_futureplan = (futureplan_ammount/365)
          if subscrib_type == 'month' and subscrib_types == 'year':
            costof_currentplan = current * perday_costof_currentplan
            monthandyearammount = paid_ammount - costof_currentplan
            monthandyear = futureplan_ammount - monthandyearammount
            amount = round(monthandyear)
          if subscrib_type == 'year' and subscrib_types == 'year':
            costof_currentplan = current * perday_costof_currentplan
            costof_futureplan = upgrade * perday_costof_futureplan
            final_ammount1 = (costof_currentplan+costof_futureplan)
            final_ammount = final_ammount1 - paid_ammount
            final_round_ammount = round(final_ammount)
            amount = final_round_ammount
          if subscrib_type == 'month' and subscrib_types == 'month':
            costof_currentplan = current * perday_costof_currentplan
            monthandmonthammount = paid_ammount - costof_currentplan
            monthandmonth = futureplan_ammount - monthandmonthammount
            amount = round(monthandmonth)
        gst_amount = int((amount * 18) / 100)
        total_amount = round(gst_amount + amount)
        if expire_date <= today:
          fulldata.append({"data": class_data.data, "amount": total_amount, "sub_total": amount, "plan_list": planlist_class.data,
                           "message": "You are currently using our " + subscrib_type+" plan "+full_name+" your subscription expired on "+str(expire_date_final1)})
        else:
          fulldata.append({"data": class_data.data, "amount": total_amount, "sub_total": amount, "plan_list": planlist_class.data, "message": "Your " +
                           full_name+" is getting expires on "+str(expire_date_final1)+" do you want to add it your existing purchase cart"})

    #Expiring List
    expiringdata = models.MdPaymentPricing.objects.filter(
        Q(created_by_id=payload['employee_n_key']) & Q(org_n_key=payload['org_n_key']))
    first_days = today + relativedelta(days=30)
    startyear = today + relativedelta(days=365)
    full_name1 = ''
    short_name1 = ''
    subscrib_type1 = ''
    expire_date1 = ''
    current_plan1 = ''
    for i in expiringdata:
      expire_date1 = i.expire_date
      full_name1 = i.full_name
      short_name1 = i.short_name
      subscrib_type1 = i.subscrib_type
      current_plan1 = i.current_plan
      if payment_n_key != i.payment_pricing_n_key:
        plans = models.PlanDetails.objects.filter(
            Q(produt_name=i.project_name))
        planlist_data = serializer1.PlanDetailsSerializer(plans, many=True)
        plan_name1 = ''
        price1 = ''
        final_price1 = ''
        for k in plans:
          plan_name1 = k.plan_name
          price1 = k.price
        splited_planname1 = plan_name1.split(',')
        splited_price1 = price1.split(',')
        for n in range(0, len(splited_planname1)):
          if splited_planname1[n] == current_plan1:
            final_price1 = splited_price1[n]
        amount1 = int(final_price1)*12
        s1 = expire_date1
        expire_date_final = s1.strftime("%d/%m/%Y")
        if expire_date1 <= today:
          expiringdata1 = models.MdPaymentPricing.objects.filter(
              Q(payment_pricing_n_key=i.payment_pricing_n_key) & Q(org_n_key=payload['org_n_key']))
          serializer_data = serializer1.MdPaymentPricingSerializer(
              expiringdata1, many=True)
          msg = 'expired'
          if expire_date1 == today:
            msg = 'expires'
            fulldata1.append({"data": serializer_data.data, "amount": amount1, "plan_list": planlist_data.data, "message": "Your " + full_name1 +
                              " is getting "+msg + " on "+str(expire_date_final)+" do you want to add it your existing purchase cart"})
          else:
            if subscrib_type1 == 'free':
              fulldata1.append({"data": serializer_data.data, "amount": amount1, "plan_list": planlist_data.data,
                                "message": "You are currently using our " + subscrib_type1+" plan "+full_name1+" your subscription expired on "+str(expire_date_final)})
            else:
              fulldata1.append({"data": serializer_data.data, "amount": amount1, "plan_list": planlist_data.data,
                                "message": "You are currently using our " + subscrib_type1+"ly plan "+full_name1+" your subscription expired on "+str(expire_date_final)})
        elif expire_date1 <= first_days:
          expiringdata1 = models.MdPaymentPricing.objects.filter(
              Q(payment_pricing_n_key=i.payment_pricing_n_key) & Q(org_n_key=payload['org_n_key']))
          serializer_data = serializer1.MdPaymentPricingSerializer(
              expiringdata1, many=True)
          fulldata1.append({"data": serializer_data.data, "amount": amount1, "plan_list": planlist_data.data, "message": "Your "+full_name1 +
                            " is getting expires on " + str(expire_date_final)+" do you want to add it your existing purchase cart"})

    return HttpResponse(json.dumps({"Expired": fulldata, "Expiring_List": fulldata1, "key_id": keys, "url": 'https://'+keys+':'+key_values+'@api.razorpay.com/v1/payments/', 'history': history.data}), content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def monthlyyearcalculations(request):
    request1 = json.loads(request.body.decode('utf-8'))
    fulldata = []
    today=datetime.date.today()
    amount=0
    amount1=0
    
    for j in range(0, len(request1)):
      plan_data = models.PlanDetails.objects.filter(Q(produt_name=request1[j]['data']['project_name']))
      
      pricing_data=models.MdPaymentPricing.objects.filter(Q(payment_pricing_n_key=request1[j]['data']['payment_pricing_n_key']) )
      
      plan_name=''
      price1=''
      final_price=0
      for k in plan_data:
        plan_name=k.plan_name
        price1=k.price
      splited_plan_name=plan_name.split(',')
      splited_price=price1.split(',')
      for n in range(0, len(splited_plan_name)):
        if splited_plan_name[n] == request1[j]['plan_name']:
          final_price=splited_price[n]
      if request1[j]['type'] == 'month':
        amount1=int(final_price)
      else:
        amount1=int(final_price)*12

      expire_date=''
      for i in pricing_data:
        expire_date=i.expire_date
      if expire_date > today:
        futureplan_ammount = amount1
        subscrib_types = request1[j]['type']
        payment_date = datetime.date.today()
        expire_date = datetime.date.today()
        price = ''
        subscrib_type = ''
        perday_costof_currentplan = ''
        perday_costof_futureplan = ''
        currentplan_ammount = ''
        for i in pricing_data:
          
          finalpayment_date = i.payment_date
          payment_date = finalpayment_date
          currentplan_ammount =i.currentplan_ammount
          finalexpire_date =i.expire_date
          expire_date =finalexpire_date
          subscrib_type =i.subscrib_type
          price = i.paid_ammount
        new_plandate = datetime.date.today()
        paid_ammount = price
        upgrade_date = expire_date - new_plandate
        upgrade = upgrade_date.days
        currentplan_days = new_plandate - payment_date
        current = currentplan_days.days
        if subscrib_type == 'month':
          perday_costof_currentplan = (currentplan_ammount/30)
        if subscrib_type == 'year':
          perday_costof_currentplan = (currentplan_ammount/365)
        if subscrib_types == 'month':
          perday_costof_futureplan = (futureplan_ammount/30)
        if subscrib_types == 'year':
          perday_costof_futureplan = (futureplan_ammount/365)
        if subscrib_type == 'month' and subscrib_types == 'year':          
          costof_currentplan = current * perday_costof_currentplan
          monthandyearammount = paid_ammount - costof_currentplan
          monthandyear = futureplan_ammount - monthandyearammount
          amount1 = round(monthandyear)
        if subscrib_type == 'year' and subscrib_types == 'year':
          costof_currentplan = current * perday_costof_currentplan
          costof_futureplan = upgrade * perday_costof_futureplan
          final_ammount1 = (costof_currentplan+costof_futureplan)
          final_ammount = final_ammount1 - paid_ammount
          final_round_ammount = round(final_ammount)
          amount1 = final_round_ammount
        if subscrib_type == 'month' and subscrib_types == 'month':
          costof_currentplan = current * perday_costof_currentplan
          monthandmonthammount =  paid_ammount - costof_currentplan
          monthandmonth = futureplan_ammount - monthandmonthammount
          amount1 = round(monthandmonth)
      if request1[j]['type'] == 'month':
        amount = amount + amount1
      else:
        amount = amount + amount1
      fulldata.append({"amount":amount1})

    sub_total=amount
    gst_amount = int((sub_total * 18) / 100)
    total_amount = round(gst_amount + sub_total)
    return HttpResponse(json.dumps({"Data":fulldata,"sub_total":sub_total,"total":total_amount}), content_type='application/json')

# sign up
@csrf_exempt
def EmployeeLogin(request):
  payload = json.loads(request.body.decode('utf-8'))
  fulldata=[]
  percentage=0
  if payload:
    employee=models.EmployeesMaster.objects.filter(Q(user_name=payload['username']) & Q(user_name__startswith=payload['username'])).filter(Q(password=payload['password']) & Q(password__startswith=payload['password']))
    n_key = ''
    created_key = ''
    org_n_key = ''
    twofactor = ''
    phonenum =''
    user_name =''
    is_new_user=''
    if employee:
      product = OrgProduct(employee[0].org_n_key)
      check_condition = 'hospital' if 'Mrecs' in product else 'bloodbank' if 'DigiBlood' in product else None
      if employee[0].is_active == 0 or employee[0].is_active == '0':
        fulldata.append('https://synapstics.com/login')
        return HttpResponse(json.dumps({"status":"Your account is deactivated. Please contact your admin","emp":{},"urls":fulldata,"twofactor":None}),content_type='application/json')    
      emp = serializers.serialize('json',employee)    
      for o in employee:
        phonenum=o.phone_number
        user_name=o.user_name
        n_key = o.employee_n_key
        created_key =o.created_by_id
        org_n_key=o.org_n_key
        role=o.role
        is_new_user=o.is_new_user
      if is_new_user == None or is_new_user =='':
        fulldata.append('https://synapstics.com/resetpassword')
        return HttpResponse(json.dumps({"status":"change_password","urls":fulldata,"emp":json.loads(emp),"setting_menu":check_condition}),content_type='application/json')
      if user_name != None:
        phonenum = user_name
      user = authenticate(username=phonenum, password=payload['password'])
      if not user:
        return HttpResponse('{"status":"The Username or password you entered is incorrect."}',content_type='application/json')
      token, created = Token.objects.get_or_create(user=user)
      for o in employee:
        o.token=token.key
      emp = serializers.serialize('json',employee)
      product = models.MdPaymentPricing.objects.filter(Q(org_n_key=employee[0].org_n_key))
      if not product:
        fulldata.append('https://synapstics.com/buyproduct')
        return HttpResponse(json.dumps({"status":"success","emp":json.loads(emp),"urls":fulldata,"twofactor":None,"setting_menu":check_condition}),content_type='application/json')    
      setting_check = settingscheck(employee[0].org_n_key,product)
      if setting_check != 'success':
        fulldata.append('https://synapstics.com/onboarding')
        return HttpResponse(json.dumps({"status":"success","emp":json.loads(emp),"urls":fulldata,"twofactor":None,"setting_menu":check_condition}),content_type='application/json') 
        
      payment_pricing = models.MdPaymentPricing.objects.filter(Q(created_by_id = n_key) | Q(created_by_id=created_key)).order_by('-payment_pricing_id')[:1]
      sms  = models.SmsSettings.objects.filter(Q(org_n_key=org_n_key))
      for a in sms:
        twofactor = a.twofactor_globally
      
      edu = models.Empeducationaldetails.objects.filter(Q(org_n_key=org_n_key) & Q(employee_n_key=n_key))
      employee = models.EmployeesMaster.objects.filter(Q(org_n_key=org_n_key) & Q(employee_n_key=n_key))
      
      if employee:
        for i in employee:
          if i.age!=None and i.age !='' and i.blood_group!=None and i.blood_group!= '' and i.emergency_person_name!=None and i.emergency_person_name!=''  and i.emergency_contact_no!= None and i.emergency_contact_no!='':
            pass
          else:
            percentage += 1
      if not edu:
        percentage += 1
      require = []
      roles = models.GERoles.objects.filter(Q(org_n_key=org_n_key) & Q(roles_name=employee[0].role))
      if roles and roles[0].document!=None:
        require = (roles[0].document).split(',')
      for x in require:
        docs = models.EmployeeOtherDocument.objects.filter(Q(employee_n_key=n_key)&Q(document_name=x))
        if not docs:
          percentage += 1 

      if percentage != 0:
        fulldata.append('https://synapstics.com/userprofile')
      else:
        fulldata.append('https://synapstics.com/landing')
      if employee[0].hospital_n_key != '' and employee[0].hospital_n_key != None:
        if 'token' in payload:
          login = Employeelog_post(employee[0].employee_n_key,payload['token'])    
      if payment_pricing:
        for i in payment_pricing:
          class_data = serializer1.MdPaymentPricingSerializer( payment_pricing, many=True)
          return HttpResponse(json.dumps({"status":"success","emp":json.loads(emp),"urls":fulldata,"twofactor":twofactor,"payment":class_data.data,"setting_menu":check_condition}),content_type='application/json')
      else:
        return HttpResponse(json.dumps({"status":"success","emp":json.loads(emp),"urls":fulldata,"twofactor":twofactor,"payment":[],"setting_menu":check_condition}),content_type='application/json')  
    else:
      return HttpResponse(json.dumps({"status":"Incorrect email or password To reset, click on 'Forgot Password?'"}),content_type='application/json')

def settingscheck(org_n_key,product):
  if 'Mrecs' in product:
    hospital = models.HospitalMaster.objects.filter(Q(org_n_key=org_n_key))
    if not hospital:
      return 'hospital'
    clinic = models.ClinicalMaster.objects.filter(Q(org_n_key=org_n_key))
    if not clinic:
      return 'clinic'
  if 'DigiBlood' in product:
    blood = models.BloodBank_Master.objects.filter(Q(org_n_key=org_n_key))
    if not blood:
      return 'bloodbank'
  roles = models.GERoles.objects.filter(Q(org_n_key=org_n_key))
  if not roles:
    return 'roles'
  employee = models.EmployeesMaster.objects.filter(Q(org_n_key=org_n_key))
  if len(employee)<=1:
    return 'employee'
  enable_sms =  models.SmsSettings.objects.filter(Q(org_n_key = org_n_key) & Q(enable_sms = 'Yes'))
  if not enable_sms:
    return 'sms'
  return 'success'

@csrf_exempt
def verify(request):
  conn = http.client.HTTPConnection("2factor.in")
  payload = json.loads(request.body.decode('utf-8'))
  sendOTP = payload.get("sendOTP")
  typedOTP= payload.get("typedOTP")
  conn.request("POST", "https://2factor.in/API/V1/19ff5a0a-b0eb-11e7-94da-0200cd936042/SMS/VERIFY/" + sendOTP + '/' + typedOTP )
  res = conn.getresponse()
  data = res.read()
  return HttpResponse(data,content_type='application/json')


@csrf_exempt
def checkemployee(request):
  request = json.loads(request.body.decode('utf-8'))
  donor_details = models.EmployeesMaster.objects.filter(phone_number=request['username'])
  if donor_details:
    return HttpResponse(json.dumps({"status":"failed", "data":"Employee not found"}), content_type='application/json')
  employee_data = serializer1.EmployeesMasterSerializer(donor_details, many=True)
  employee_n_key = ''
  phone_number = ''
  expire_date = ''
  
  if donor_details:
    for i in donor_details:
      employee_n_key = i.employee_n_key
      phone_number = i.phone_number
    payment_details = models.MdPaymentPricingSerializer.objects.filter(created_by_id=employee_n_key).order_by('-payment_pricing_id')[:1]
    for j in payment_details:
      expire_date = j.expire_date
    if expire_date !='' and expire_date > datetime.date.today():
      return HttpResponse(json.dumps({"status":"success", "employees": employee_data.data}), content_type='application/json')
    else:
      return HttpResponse(json.dumps({"status": "Please Make The Payment", "employees": []}), content_type='application/json')
  else:
    return HttpResponse(json.dumps({"status": "No Record Found"}), content_type='application/json')

@csrf_exempt
def sendOTP(request):
  conn = http.client.HTTPConnection("2factor.in")
  payload = json.loads(request.body.decode('utf-8'))
  phoneno=payload["username"]
  conn.request("POST", "https://2factor.in/API/V1/19ff5a0a-b0eb-11e7-94da-0200cd936042/SMS/+91" + str(phoneno) + "/AUTOGEN/Mrecs")
  res = conn.getresponse()
  data = res.read()
  return HttpResponse(data,content_type='application/json')

# sms setting
@csrf_exempt
@api_view(["POST"])
def SmsTemplate(request):
  data = JSONParser().parse(request)
  data['created_on']=DefaultTimeZone()
  serializer =serializer1.SmsTemplateSerializer(data=data)
  if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=204)
  return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def SmsTemplateEdit(request, pk):
  """
  Retrieve, update or delete a code snippet.
  """
  try:
    snippet =models.SmsTemplateSettings.objects.get(pk=pk)
  except models.SmsTemplateSettings.DoesNotExist:
    return HttpResponse(json.dumps({"data":"no data found"}),content_type="application/json")
  if request.method == 'GET':
    serializer =serializer1.SmsTemplateSerializer(snippet)
    return JsonResponse(serializer.data)
  elif request.method == 'PUT':
    request.data['modified_on']=DefaultTimeZone()
    serializer =serializer1.SmsTemplateSerializer(snippet, data=request.data,partial=True)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE': 
    snippet.delete()
    return HttpResponse(json.dumps({"data":"data deleted successfully"}),content_type="application/json")  


@csrf_exempt
def smspayment(request):
  payload = json.loads(request.body.decode('utf-8'))
  payment_id=payload["payment_id"]
  amount=payload["amount"]
  client = razorpay.Client(auth=("rzp_live_2A3otkvCaR2SIR", "rNjgz5MeXpp8tQ0uPSUaY19s"))
  paymentdata = client.payment.capture(payment_id, (str(amount)+'00'))

  return AmountPayment(payload,paymentdata['status'])

@csrf_exempt
@api_view(['POST'])
def SMSAmountCalculation(request):
  request = json.loads(request.body.decode('utf-8'))

  if request:
    original_amount = int(request['no_sms']) * 0.20
    
    gst_amount =(original_amount * 18) / 100
    
    total_amount = round(original_amount + gst_amount)
    
    if total_amount >= 500:
      return HttpResponse(json.dumps({'status':total_amount}), content_type="application/json")
    else:
      return HttpResponse(json.dumps({'status':total_amount}), content_type="application/json")
  return HttpResponse("error occured", content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def SmsPost(request):
  data = JSONParser().parse(request)
  data['created_on']=DefaultTimeZone()
  serializer =serializer1.SMSSerializer(data=data)
  if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=204)
  return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["POST"])
def SmsGetDetails(request):
  data = JSONParser().parse(request)
  sms=models.SmsSettings.objects.filter(Q(org_n_key=data['org_n_key']))
  serializer =serializer1.SMSSerializer(sms, many=True)
  return HttpResponse(json.dumps(serializer.data), content_type="application/json")

@csrf_exempt
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def Sms_detail(request, pk):
  data = JSONParser().parse(request)
  """
  Retrieve, update or delete a code snippet.
  """
  try:
    snippet =models.SmsSettings.objects.get(pk=pk)
  except models.SmsSettings.DoesNotExist:
    return HttpResponse(json.dumps({"data":"no data found"}),content_type="application/json")
  if request.method == 'GET':
    serializer =serializer1.SMSSerializer(snippet)
    return JsonResponse(serializer.data)
  elif request.method == 'PUT':
    employee=models.EmployeesMaster.objects.filter((Q(employee_n_key=data['employee_n_key'])))
    data['modified_on']=DefaultTimeZone()
    serializer =serializer1.SMSSerializer(snippet, data=data)
    if serializer.is_valid():
      serializer.save()
      if employee[0].role == 'Master':
        role_name = "Master"
      elif employee[0].role != "Physician" and role[0].role_check != "Yes":
        role_name = employee[0].role
      else:
        role_name = "Physician"
      return HttpResponse(json.dumps({"role":role_name}),content_type="application/json")
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    snippet.delete()
    return HttpResponse(json.dumps({"data":"data deleted successfully"}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def sms_history_detail(request):
  request = json.loads(request.body.decode('utf-8'))
  sms = models.SmsHistory.objects.filter(org_n_key= request['org_n_key'])
  sms_serializer = serializer1.SmsHistorySerializer(sms, many=True).data
  for index,i in enumerate(sms_serializer):
    i['created_time']=sms[index].created_time.strftime('%I:%M %p')
  return HttpResponse(json.dumps({"smshistory":sms_serializer,"key_id":"rzp_live_2A3otkvCaR2SIR"}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def RechargeSms(request):
  request = json.loads(request.body.decode('utf-8'))
  sms_payment = models.SmsPaymentHistory.objects.filter(org_n_key= request['org_n_key'])
  sms_payment_serializer = serializer1.SmsPaymentSerializer(sms_payment, many=True)
  return HttpResponse(json.dumps(sms_payment_serializer.data),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def SmsTemplateFilter(request):
  request = json.loads(request.body.decode('utf-8'))
  sms = models.SmsTemplateSettings.objects.filter(Q(org_n_key = request['org_n_key']))
  sms_class = serializer1.SmsTemplateSerializer(sms, many=True)
  return HttpResponse(json.dumps(sms_class.data), content_type="application/json")


#sign in
@csrf_exempt
def TwoFactorsendOTP(request):
  conn = http.client.HTTPConnection("2factor.in")
  payload = json.loads(request.body.decode('utf-8'))
  emp = models.EmployeesMaster.objects.filter(Q(user_name=payload['username']))
  if not emp:
    return HttpResponse(json.dumps({"status":"no user found"}),content_type='application/json')
  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  check_sms =  models.SmsSettings.objects.filter(Q(org_n_key=emp[0].org_n_key)&Q(remaining_sms__gt= 1) & Q(enable_sms='Yes'))
  if check_sms:
    # phoneno=payload["phone_number"]
    phoneno=emp[0].dial_code+str(emp[0].phone_number)
    conn.request("POST", "https://2factor.in/API/V1/19ff5a0a-b0eb-11e7-94da-0200cd936042/SMS/" + str(phoneno) + "/AUTOGEN/Mrecs")
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if json_data['Status']== 'Success':
      remaining_sms = int(check_sms[0].remaining_sms) - 1
      models.SmsSettings.objects.filter(org_n_key=emp[0].org_n_key).update(remaining_sms =remaining_sms)
      models.SmsHistory.objects.create(hospital_n_key = emp[0].hospital_n_key,org_n_key = emp[0].org_n_key,
        phone_number = emp[0].phone_number,sms_status = json_data['Status'],
        sms_type = 'OTP',created_on = datetime.date.today(),created_time =current_time
        )
    else:
      models.SmsHistory.objects.create(hospital_n_key = emp[0].hospital_n_key,org_n_key = emp[0].org_n_key,
        phone_number = emp[0].phone_number,sms_status = json_data['Status'],
        sms_type = 'OTP',created_on = datetime.date.today(),created_time =current_time
        )
    return HttpResponse(data,content_type='application/json')
  else:
    return HttpResponse(json.dumps({"status":"no data found or sms not enabled"}),content_type='application/json')

@csrf_exempt
def TwoFactorverifyOTP(request):
  conn = http.client.HTTPConnection("2factor.in")
  payload = json.loads(request.body.decode('utf-8'))
  sendOTP = payload.get("sendOTP")
  typedOTP= payload.get("typedOTP")
  conn.request("POST", "https://2factor.in/API/V1/19ff5a0a-b0eb-11e7-94da-0200cd936042/SMS/VERIFY/" + sendOTP + '/' + typedOTP )
  res = conn.getresponse()
  data = res.read()
  return HttpResponse(data,content_type='application/json')

# roles
@csrf_exempt
@api_view(["POST"])
def GeUnique_roles(request):
  request = json.loads(request.body.decode('utf-8'))
  unique_list=[]
  alldata = []
  list1 = []
  payment_values = OrgProduct(request['org_n_key'])
  if 'Mrecs' in payment_values:
    list1=list(models.GERoles.objects.filter(Q(org_n_key = request['org_n_key'])&Q(product_name='Mrecs')).values_list('roles_name', flat=True))
  bloodbank_roles = []
  if 'DigiBlood' in payment_values:
    bloodbank_roles = list(models.GERoles.objects.filter(Q(org_n_key = request['org_n_key'])&Q(product_name='DigiBlood')).values_list('roles_name', flat=True))
  for i in list1:
    if i in unique_list:
      pass
    else:
      unique_list.append(i)
  spec_data = []
  speciality = models.MedicalSpecialty.objects.all()
  for i in speciality:
    spec_data.append(i.speciality)
  
  all_docs = ["Professional Degree","Address Proof","Bank Account Details","Previous Employment Documents","Others"]
  roles = models.GERoles.objects.filter(Q(roles_name=request['roles_name'])&Q(org_n_key = request['org_n_key']))
  if roles and roles[0].document != None:
    doc = (roles[0].document).split(',')
    for i in doc:
      alldata.append({"name":i,"type":"*"})
      all_docs.remove(i) if i in all_docs else None
  for j in all_docs:
    alldata.append({"name":j,"type":""})
  docs_data = []
  docs = models.EmployeeOtherDocument.objects.filter(Q(employee_n_key=request['employee_n_key']))
  if docs:
    docs_data = serializer1.EmployeeOtherDocumentSerializer(docs, many=True).data
    for index,i in enumerate(docs_data):
      i['date'] = docs[index].created_on.strftime("%d/%m/%Y")
  return HttpResponse(json.dumps({"Unique_roles":unique_list,"specialities":spec_data,"document_list":alldata,"documents":docs_data,'bloodbank_roles':list(set(bloodbank_roles))}),content_type="application/json")

@csrf_exempt
# @api_view(["POST"])
def GECategorylist(request):
  request = json.loads(request.body.decode('utf-8'))
  module = models.GERoles.objects.filter(Q(product_name =request['product_name']) & Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(roles_name=request['roles_name']))
  serializer_class=serializer1.GERolesSerializer(module, many=True).data
  return_data = serializer_class
  for i in return_data:
    i['role_check'] = [] if i['role_check'] == None or i['role_check'] == '' else i['role_check']
  return HttpResponse(json.dumps(return_data),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def RolesUpdate(request):
  request = json.loads(request.body.decode('utf-8'))
  delete_records = models.GERoles.objects.filter(Q(hospital_n_key = request[0]['hospital_n_key']) & Q(roles_name = request[0]['roles_name']))
  for i in delete_records:
    a = models.GERoles.objects.filter(role_id = i.role_id).delete()
  try:
    for index,j in enumerate(request):
      if request[index]['product_name'] == 'DigiBlood':
        bloodbank = models.BloodBank_Master.objects.filter(Q(org_n_key=request[index]['org_n_key']))
        request[index]['created_on'] = TimeZoneBloodbank(bloodbank[0].bloodbank_n_key)
      if request[index]['product_name'] == 'Mrecs':
        request[index]['created_on']=TimeZoneConvert(request[index]['hospital_n_key'])

      serializer = serializer1.GERolesSerializer(data=request[index])
      if serializer.is_valid():
        serializer.save()
      else:
        return HttpResponse(json.dumps({"status":"update failed1","data":serializer.errors}), content_type="application/json")      
  except:
    return HttpResponse(json.dumps({"status":"update failed2"}), content_type="application/json")  
  return HttpResponse(json.dumps({"status":"successfully updated"}), content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Role_search(request):
  request = json.loads(request.body.decode('utf-8'))
  modules_details=models.RoleNames.objects.filter(roles__istartswith = request['roles'])
  serializer_class=serializer1.RoleNamesSerializer(modules_details, many=True)
  return HttpResponse(json.dumps(serializer_class.data),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def RolesWorkingUpdate(request):
  request = json.loads(request.body.decode('utf-8'))
  module = models.GERoles.objects.filter(Q(product_name =request['product_name']) & Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(roles_name=request['roles_name']))
  if module:
    module.update(working_enable=request['working_enable'])
    return HttpResponse(json.dumps({"status":"successfully updated"}), content_type="application/json")
  return HttpResponse(json.dumps({"status":"Role Not Found"}), content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def Role_post(request):
  request=json.loads(request.body.decode('utf-8')) 
  fulldata=[]
  role_check = models.GERoles.objects.filter(Q(roles_name=request[0]['roles_name']) & Q(org_n_key=request[0]['org_n_key']) & Q(product_name=request[0]['product_name']))
  if role_check:
    return HttpResponse(json.dumps({"status":"Role Name Already exist","roles":[]}), content_type="application/json")
  for index,i in enumerate(request):
    if request[index]['product_name'] == 'DigiBlood':
      bloodbank = models.BloodBank_Master.objects.filter(Q(org_n_key=request[index]['org_n_key']))
      request[index]['created_on'] = TimeZoneBloodbank(bloodbank[0].bloodbank_n_key)
    if request[index]['product_name'] == 'Mrecs':
      request[index]['created_on']=TimeZoneConvert(request[index]['hospital_n_key'])

    if request[index]['othersroles_name']=='':
      rolename=request[index]['roles_name']
      role_details=models.GERoles.objects.create(roles_name=rolename,description=request[index]['description'],category=request[index]['category'],product_name=request[index]['product_name'],
        page_name=request[index]['page_name'],urls=request[index]['urls'],hospital_n_key=request[index]['hospital_n_key'],
        org_n_key=request[index]['org_n_key'],created_by_id=request[index]['created_by_id'],created_by_name=request[index]['created_by_name'],role_check=request[index]['role_check'],
        created_on=request[index]['created_on'],document=request[0]['document'],working_enable=request[0]['working_enable'],pdashboard_appointment=request[0]['pdashboard_appointment'],calendar_appointment=request[0]['calendar_appointment'])
    else:
      rolename=request[index]['roles_name']
      role=request[index]['othersroles_name']
      role_details=models.GERoles.objects.create(roles_name=role,description=request[index]['description'],category=request[index]['category'],product_name=request[index]['product_name'],
        page_name=request[index]['page_name'],urls=request[index]['urls'],hospital_n_key=request[index]['hospital_n_key'],
        org_n_key=request[index]['org_n_key'],created_by_id=request[index]['created_by_id'],created_by_name=request[index]['created_by_name'],role_check=request[index]['role_check'],
        created_on=request[index]['created_on'],document=request[0]['document'],working_enable=request[0]['working_enable'],pdashboard_appointment=request[0]['pdashboard_appointment'],calendar_appointment=request[0]['calendar_appointment'])
    serializer_class=serializer1.GERolesSerializer(role_details)
    fulldata.append(serializer_class.data)
  return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")  

@csrf_exempt
def Modules(request):
  request = json.loads(request.body.decode('utf-8'))
  module = models.GeModules.objects.filter(Q(product_name=request['product_name']))
  serializer_class=serializer1.GeModulesSerializer(module, many=True)
  return HttpResponse(json.dumps(serializer_class.data),content_type="application/json")

# otp setting
@csrf_exempt
@api_view(["POST"])
def Get_Employeerole(request):
  request = json.loads(request.body.decode('utf-8'))
  employee=models.EmployeesMaster.objects.filter((Q(employee_n_key=request['employee_n_key'])))
  role=models.GERoles.objects.filter((Q(roles_name=employee[0].role)))
  if employee[0].role == 'Master':
    return HttpResponse(json.dumps({"role":"Master"}),content_type="application/json")
  elif employee[0].role != "Physician" and role[0].role_check != "Yes":
    return HttpResponse(json.dumps({"role":employee[0].role}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({"role":"Physician"}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Get_Smspost_Details(request):
  request = json.loads(request.body.decode('utf-8'))
  sms = models.SmsSettings.objects.filter(org_n_key= request['org_n_key'])
  sms_serializer = serializer1.SMSSerializer(sms, many=True)
  return HttpResponse(json.dumps(sms_serializer.data),content_type="application/json")


# hospital details
@permission_classes((AllowAny,))  
class TimeZoneViewSet(viewsets.ModelViewSet):
  queryset=models.MdTimeZone.objects.all().order_by('timezone_name') 
  serializer_class=serializer1.TimeZoneSerializer
  lookup_field = 'timezone_id'

@csrf_exempt
@api_view(["POST"])
def Hospital_Working_Details_Update(request):
  request = json.loads(request.body.decode('utf-8'))
  hospit = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']))
  if hospit:
    request['modified_on'] = TimeZoneConvert(request['hospital_n_key'])
    hos_create = serializer1.HospitalMasterSerializer(instance=hospit[0], data=request, partial=True)
    if hos_create.is_valid():
      hos_create.save()
    else:
      return HttpResponse(json.dumps({"data":hos_create.errors}),content_type="application/json")
  work_filter = models.HospitalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']))
  if work_filter:
    work_filter_del = work_filter.delete()
  workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
  if request['twenty_four_hours'] != "Yes":
    # workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'])
    if len(workingdetails['working_days']) > 0:      
      for i in workingdetails['working_days']:
        if (i['start_time'] !='') and (i['start_time'] != None):
          hospital_working = models.HospitalWorkingDetails.objects.create(hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],end_time=i['end_time'],
            created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
  spec_filter = models.HospitalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']))
  if spec_filter:
    spec_filter_del = spec_filter.delete()
  if len(workingdetails['special_hours']) > 0:
    for j in workingdetails['special_hours']:  
      special_hours = models.HospitalSpecialHours.objects.create(hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],
        end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
  return HttpResponse(json.dumps('success'),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Logo_hospital_update(request):
  find = models.HospitalMaster.objects.filter(hospital_n_key=request.POST['hospital_n_key'])
  https_address = 'https://synapstics.com'
  http_address = 'http://'
  if find:
    if request.method == 'POST' and 'hospital_logo' in request.FILES and request.FILES['hospital_logo']:
      myfile = request.FILES['hospital_logo']
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
      http_address = ''
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001':        
        find.update(hospital_logo=http_address + request.get_host()+ uploaded_file_url)
      else:
        find.update(hospital_logo=https_address +"/api"+ uploaded_file_url)
      # return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
    if request.method == 'POST' and 'banner_image' in request.FILES and request.FILES['banner_image']:
      myfile = request.FILES['banner_image']
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001':
        find.update(banner_image=http_address + request.get_host()+ uploaded_file_url)
      else:
        find.update(banner_image=https_address +"/api"+ uploaded_file_url)
    return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
  return HttpResponse(json.dumps({"status":"Failed"}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Logo_hos_get(request):
  request = json.loads(request.body.decode('utf-8'))
  img = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']))
  return HttpResponse(json.dumps({"logo":str(img[0].hospital_logo),"banner":str(img[0].banner_image)}),content_type="application/json")




# @csrf_exempt
# @api_view(["POST"])
# def Hospital_Master_Post(request):
#   request = json.loads(request.body.decode('utf-8'))
#   data = []
#   clinic = request['hospital_name']
#   split_clinic = clinic.split(' ')
#   short = ''
#   if len(split_clinic) >= 3:
#     for i in range(0,len(split_clinic)):
#       if i <= 2:
#         data.append(split_clinic[i][0])
#     s = [str(i) for i in data]
#     short = str("".join(s)).upper()
#   if len(split_clinic) > 1 and len(split_clinic) <= 2:
#     for i in range(0,len(split_clinic)):
#       if i == 1:
#         data.append(split_clinic[i][0])
#       else:
#         data.append(split_clinic[i][:2])
#     s = [str(i) for i in data]
#     short = str("".join(s)).upper()
#   if len(split_clinic) == 1:
#     s = [str(i) for i in split_clinic]
#     short = str("".join(s)).upper()
#     short = short[:3]
#   time_zone = request.get('time_zone')
#   now_time = datetime.datetime.now(timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')
#   hos_create = models.HospitalMaster.objects.create(org_n_key=request.get('org_n_key'),hospital_name=request.get('hospital_name'),hospital_short=short,hospital_phoneno=request.get('hospital_phoneno'),
#     employee_n_key=request.get('employee_n_key'),licence_no=request.get('licence_no'),hospital_logo=request.get('hospital_logo'),gst_no=request.get('gst_no'),hospital_address_line_one=request.get('hospital_address_line_one'),
#     state=request.get('state'),city=request.get('city'),pincode=request.get('pincode'),hospital_address_line_two=request.get('hospital_address_line_two'),
#     bloodbank=request.get('bloodbank'),g_ehr=request.get('g_ehr'),suburb=request.get('suburb'),country=request.get('country'),
#     created_by_id=request.get('created_by_id'),created_by_name=request.get('created_by_name'),created_on=now_time,accreditation=request.get('accreditation'),provider_type=request.get('provider_type'),
#     telephone_no=request.get('telephone_no'),emergency_no=request.get('emergency_no'),ambulance_no=request.get('ambulance_no'),foreign_patientcare=request.get('foreign_patientcare'),
#     tollfree_no=request.get('tollfree_no'),helpline=request.get('helpline'),hospital_fax_no=request.get('hospital_fax_no'),pri_email_id=request.get('pri_email_id'),sec_email_id=request.get('sec_email_id'),
#     website=request.get('website'),total_doctors=request.get('total_doctors'),total_experts=request.get('total_experts'),total_beds=request.get('total_beds'),total_wards=request.get('total_wards'),facilities_others=request.get('facilities_others'),
#     establised_year=request.get('establised_year'),medical_specialty=request.get('medical_specialty'),facilities=request.get('facilities'),aayush=request.get('aayush'),medical_insurance=request.get('medical_insurance'),
#     twenty_four_hours=request.get('twenty_four_hours'),provider_type_others=request.get('provider_type_others'),specialties_others=request.get('specialties_others'),medical_insurance_others=request.get('medical_insurance_others'),dial_code=request.get('dial_code'),time_zone=request.get('time_zone'))

#   if request['twenty_four_hours'] != "Yes":
#     if len(request['working_days']) > 0:
#       for i in request['working_days']:
#         if (i['start_time'] !='') and (i['start_time'] != None):
#           hospital_working = models.HospitalWorkingDetails.objects.create(hospital_n_key=hos_create.hospital_n_key,org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],end_time=i['end_time'],
#             created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
#   if len(request['special_hours']) > 0:
#     for j in request['special_hours']:
#       special_hours = models.HospitalSpecialHours.objects.create(hospital_n_key=hos_create.hospital_n_key,org_n_key=request['org_n_key'],special_date=j['spl_date'],available=j['available'],start_time=j['spl_start_time'],
#         end_time=j['spl_end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
#   hos_check = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
#   if len(hos_check)==1:
#     models.EmployeesMaster.objects.filter(employee_n_key=hos_create.employee_n_key).update(hospital_n_key=hos_create.hospital_n_key)
#   hos_data = serializer1.HospitalMasterSerializer(hos_check[0]).data
#   hos_last = serializer1.HospitalMasterSerializer(hos_check[len(hos_check)-1]).data
#   return HttpResponse(json.dumps({"status":"success","last_details":hos_last,"details":hos_data,"time_zone":request.get('time_zone')}),content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def Doctor_Master_update(request):
  request = json.loads(request.body.decode('utf-8'))
  employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=request['employee_n_key']) & Q(org_n_key=request['org_n_key']))
  if employee:
    hospital = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
    if len(hospital) == 1:
      employee_up = employee.update(hospital_n_key=request['hospital_n_key'],hospital_short_name=request['hospital_short_name'])
      return HttpResponse(json.dumps('Success'),content_type="application/json")
  return HttpResponse(json.dumps(''),content_type="application/json")

@csrf_exempt
# @api_view(["POST"])
def Check_Plan_CentreDetails(request):
  payload = json.loads(request.body.decode('utf-8'))
  final_centre=0
  payment= models.MdPaymentPricing.objects.filter(Q(org_n_key=payload['org_n_key'])).order_by('-payment_pricing_id')
  if payment:
    plans= models.PlanDetails.objects.filter(Q(product_name=payment[0].product_name))
    for k in plans:
      plan_name = k.plan_name
      centres = k.centres
    splited_planname = plan_name.split(',')
    splited_centres = centres.split(',')
    for n in range(0, len(splited_planname)):
      if splited_planname[n] == payment[0].current_plan:
        final_centre = splited_centres[n]
    hospital = models.HospitalMaster.objects.filter(Q(org_n_key=payload['org_n_key'])).count()
    if final_centre == hospital:
      count = 0
      status = 'You cannot add centres'
    else:
      count = int(final_centre) - hospital
      status = 'You cannot add centres'
    return HttpResponse(json.dumps({"status":status,"count":count,"hospital_count":final_centre}),content_type='application/json')
  else:
    return HttpResponse(json.dumps({"status":"","count":0,"hospital_count":0}),content_type='application/json')

@csrf_exempt
def HospitalInfo(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital_info = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
  if hospital_info:
    hospital_serializer = serializer1.HospitalMasterSerializer(hospital_info, many=True)
    return HttpResponse(json.dumps(hospital_serializer.data), content_type="application/json")
  else:
    return HttpResponse(json.dumps([]), content_type="application/json")

# home price
class PaymentPricingViewSet(viewsets.ModelViewSet):
  queryset=models.MdPaymentPricing.objects.all()
  serializer_class=serializer1.MdPaymentPricingSerializer
  lookup_field = 'payment_pricing_n_key'

@csrf_exempt
def Employee_Product_Set(request):
    payload = json.loads(request.body.decode('utf-8'))
    if payload:
      employee=models.EmployeesMaster.objects.filter((Q(employee_n_key=payload['employee_n_key'])))
      n_key = ''
      created_key = ''
      user_name=''
      password=''
      phonenum=''
      if employee:
        for o in employee:
          phonenum=o.phone_number
          user_name=o.user_name
          password=o.password
          n_key = o.employee_n_key
          created_key =o.created_by_id
        if user_name != None:
          phonenum = user_name

        user = authenticate(username=phonenum, password=password)
        token, created = Token.objects.get_or_create(user=user)
        for o in employee:
          o.token=token.key
        emp = serializers.serialize('json',employee)
        payment_pricing = models.MdPaymentPricing.objects.filter(Q(created_by_id = n_key) | Q(created_by_id=created_key)).order_by('-payment_pricing_id')
        products = models.PlanDetails.objects.filter(Q(status='Active'))
        products_data = serializer1.PlanDetailsSerializer(products, many=True)
        
        if not payment_pricing:
          return HttpResponse(json.dumps({"status": "success", "emp": json.loads(emp), "payment": [], "product": products_data.data}), content_type='application/json')
        for i in payment_pricing:
          class_data = serializer1.MdPaymentPricingSerializer( payment_pricing, many=True)
          return HttpResponse(json.dumps({"status":"success","emp":json.loads(emp),"payment":class_data.data,"product":products_data.data}),content_type='application/json')
      else:
        return HttpResponse('{"status":"The Username or password you entered is incorrect."}',content_type='application/json')

# home page
@csrf_exempt
def Payment_History(request):
  payload = json.loads(request.body.decode('utf-8'))
  fulldata=[]
  return_data = {}
  paydata1 = models.MdPaymentPricing.objects.filter(org_n_key=payload['org_n_key'])
  products=models.PlanDetails.objects.all()
  products_data = serializer1.PlanDetailsSerializer(products, many=True)
  employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=payload['employee_n_key']))
  today = datetime.date.today()
  thirty_days = today + relativedelta(days=30)
  for i in paydata1:
    fullname = products.filter(Q(product_name=i.product_name))
    if i.expire_date >= datetime.date.today():
      paydata=models.MdPaymentPricing.objects.filter(payment_pricing_id=i.payment_pricing_id)
      paymentdetaildata=serializer1.MdPaymentPricingSerializer(paydata[0]).data
      expiry=''
      expire_date_final = (i.expire_date).strftime("%d/%m/%Y")
      paymentdetaildata['expiry']="your plan is expires on "+str(expire_date_final) if i.expire_date <= thirty_days else ''
      paymentdetaildata['fullname'] = fullname[0].full_name
      paymentdetaildata['status'] = 'success'
      fulldata.append(paymentdetaildata)
      products = products.exclude(product_name=i.product_name)
    else:
      paydata=models.MdPaymentPricing.objects.filter(payment_pricing_id=i.payment_pricing_id)
      paymentdetaildata=serializer1.MdPaymentPricingSerializer(paydata[0]).data
      paymentdetaildata['fullname'] = fullname[0].full_name
      paymentdetaildata['status'] = 'expired'
      paymentdetaildata['expiry'] = ''
      fulldata.append(paymentdetaildata)
      products = products.exclude(product_name=i.product_name)
    blood_des = 'A blood bank management system designed for your success with various modules essential for managing your blood bank Front Office,Lab Bulk Upload,Blood Issues,Component Bulk Upload.'
    mrecs_des='Practice management, and medical billing software system for the smallest of private medical practices'
    paymentdetaildata['description']=blood_des if i.product_name == 'DigiBlood' else mrecs_des
    paymentdetaildata['access'] = True
    paymentdetaildata['coming_soon']=True if i.product_name == 'DigiBlood' else False
    fill = settingscheck(payload['org_n_key'],[i.product_name])
    # print(fill)
    paymentdetaildata['setup'] = True if fill != 'success' and (employee and employee[0].role == 'Master' or employee[0].role == 'Careteam') else False 
    employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=payload['employee_n_key']))
    if employee[0].role != 'Master':
      if employee[0].product_name == None or i.product_name not in employee[0].product_name:
        paymentdetaildata['access'] = False
  other_product = serializer1.PlanDetailsSerializer(products,many=True).data
  for k in other_product:
    k['status'] = 'Inactive' if k['status'] == 'InActive' else 'Active'
    k['plan_details'] = {"product_name":k['product_name'],"plan":{"plan_name":"Starter","plan_display_name":"Basic","current_plan":"Starter","full_name":k['full_name'],"currentplan_ammount":(k['price'].split(','))[0],"coming_soon":True if k['product_name'] == 'DigiBlood' else False}}
  product_access = True if employee and employee[0].role == 'Master' or employee[0].role == 'Careteam' else False 
  return HttpResponse(json.dumps({'payment_status':fulldata,'other_product':other_product,'product_access':product_access}),content_type='application/json')

@csrf_exempt
@api_view(['POST'])
def CheckAllDetail(request):
  request = json.loads(request.body.decode('utf-8'))
  employee = models.EmployeesMaster.objects.filter(employee_n_key =request['employee_n_key'])
  product = OrgProduct(request['org_n_key'])
  if 'Mrecs' in product:
    hospital = models.HospitalMaster.objects.filter(org_n_key =request['org_n_key'])
    if not hospital:
      return HttpResponse(json.dumps({'status':'Hospital Details are not filled','role':employee[0].role,'bloodbank':'Yes' if 'DigiBlood' in product else 'No',"gehr":'Yes' if 'Mrecs' in product else 'No'}),content_type='application/json')    
  if 'DigiBlood' in product:
    blood = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
    if not blood:
      return HttpResponse(json.dumps({'status':'Bloodbank Details are not filled','role':employee[0].role,'bloodbank':'Yes' if 'DigiBlood' in product else 'No',"gehr":'Yes' if 'Mrecs' in product else 'No'}),content_type='application/json')
  return HttpResponse(json.dumps({'status':'success','role':employee[0].role,'bloodbank':'Yes' if 'DigiBlood' in product else 'No',"gehr":'Yes' if 'Mrecs' in product else 'No'}),content_type='application/json')
  
  # org = models.OrganizationMaster.objects.filter(org_n_key =request['org_n_key'])
  # role = ''
  # fulldata = []
  # bloodbank = ''
  # gehr = ''
  # hospitals=''

  
  # for j in employee:
  #   role = j.role
  #   bloodbank = j.bloodbank
  #   gehr = j.g_ehr
  
  # fulldata.append({'bloodbank':bloodbank,"gehr":gehr})
  # if bloodbank == 'Yes':
  #   blood = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
  #   if not blood:
  #     return HttpResponse(json.dumps({'status':'Bloodbank Details are not filled','role':role,'hospital':hospitals,'bloodbank':bloodbank,"gehr":gehr}),content_type='application/json')
  # if gehr=='Yes':
  #   hospital = models.HospitalMaster.objects.filter(org_n_key =request['org_n_key'])
  #   if not hospital:
  #     return HttpResponse(json.dumps({'status':'Hospital Details are not filled','role':role,'hospital':hospitals,'bloodbank':bloodbank,"gehr":gehr}),content_type='application/json')   
  # if role == 'Master':
  #   return HttpResponse(json.dumps({'status':'success','role':role,'hospital':hospitals,'bloodbank':bloodbank,"gehr":gehr}),content_type='application/json')
  # else:
  #   return HttpResponse(json.dumps({'status':'success','role':role,'hospital':hospitals,'bloodbank':bloodbank,"gehr":gehr}),content_type='application/json')


@csrf_exempt
@api_view(["POST"])
def SettingsCondition(request):
  request = json.loads(request.body.decode('utf-8'))
  product = OrgProduct(request['org_n_key'])
  if request['type']=='hospital':
    if 'Mrecs' in product:
      hospital = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
      if hospital:
        return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
    return HttpResponse(json.dumps({"status":"Failure"}),content_type="application/json")
  if request['type']=='bloodbank':
    if 'DigiBlood' in product:
      blood = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
      if blood:
        return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
    return HttpResponse(json.dumps({"status":"Failure"}),content_type="application/json")
  elif (request['type']=='clinic'):
    clinic = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']))
    if clinic:
      return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
    else:
      return HttpResponse(json.dumps({"status":"Failure","info":"hospital details not filled"}),content_type="application/json")
  elif (request['type']=='roles'):
    if 'Mrecs' in product:
      roles = models.ClinicalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
      if roles:
        return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
      else:
        return HttpResponse(json.dumps({"status":"Failure","info":"clinical details not filled"}),content_type="application/json")
    if 'DigiBlood' in product:
      roles = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
      if roles:
        return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
      else:
        return HttpResponse(json.dumps({"status":"Failure","info":"bloodbank details not filled"}),content_type="application/json")
  elif (request['type']=='employee'):
    employee = models.GERoles.objects.filter(Q(org_n_key=request['org_n_key']))
    if employee:
      return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
    else:
      return HttpResponse(json.dumps({"status":"Failure","info":"roles details not filled"}),content_type="application/json")
  elif (request['type']=='sms'):
    sms = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']))
    if len(sms)>1:
      return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
    else:
      return HttpResponse(json.dumps({"status":"Failure","info":"employee details not filled"}),content_type="application/json")
  elif (request['type']=='otp'):
    sms = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']))
    if sms:
      return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
    else:
      return HttpResponse(json.dumps({"status":"Failure","info":"employee details not filled"}),content_type="application/json")
  return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")


def OrgProduct(org_n_key):
  product = []
  pricing = list(models.MdPaymentPricing.objects.filter(Q(org_n_key=org_n_key)).values('product_name'))
  if pricing:
    product = [d['product_name'] for d in pricing]
  return product

@csrf_exempt
def CheckGeneralSettings(request):
  request  = json.loads(request.body.decode('utf-8'))
  product = OrgProduct(request['org_n_key'])
  if not product:
    return HttpResponse(json.dumps({"status":"failed","info":"No Product details found"}), content_type="application/json")
  roles = models.GERoles.objects.filter(Q(org_n_key=request['org_n_key']))
  employee = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']))
  enable_sms =  models.SmsSettings.objects.filter(Q(org_n_key = request['org_n_key']) & Q(enable_sms = 'Yes'))

  if 'DigiBlood' in product:
    bloodbank = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
    if not bloodbank:
      return HttpResponse(json.dumps({"status":"failed","info":"bloodbank details not found"}), content_type="application/json")
  if 'Mrecs' in product:
    hospital = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
    clinic = models.ClinicalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
    if not hospital:
      return HttpResponse(json.dumps({"status":"failed","info":"hospital details not found"}), content_type="application/json")
    clinic = models.ClinicalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
    if not clinic:
      return HttpResponse(json.dumps({"status":"failed","info":"clinical details not found"}), content_type="application/json")
  roles = models.GERoles.objects.filter(Q(org_n_key=request['org_n_key']))
  if not roles:
    return HttpResponse(json.dumps({"status":"failed","info":"roles details not found"}), content_type="application/json")
  employee = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']))
  if len(employee)<2:
    return HttpResponse(json.dumps({"status":"failed","info":"employee details not found"}), content_type="application/json")
  sms = models.SmsSettings.objects.filter(Q(org_n_key=request['org_n_key']))
  if not sms:
    return HttpResponse(json.dumps({"status":"failed","info":"sms details not found"}), content_type="application/json")
  return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")
def RandomString():
  res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 10))
  return res
@csrf_exempt
def Checkpayment_home(request):
    payload = json.loads(request.body.decode('utf-8'))
    # employee=models.EmployeesMaster.objects.filter((Q(org_n_key=payload['org_n_key']) & Q(role='Master')))
    # n_key = ''
    # created_key = ''
    # phonenum=''
    # user_name=''
    # if employee:
      # phonenum=employee[0].phone_number
      # user_name=employee[0].user_name
      # password=employee[0].password
      # n_key = employee[0].employee_n_key
      # created_key =employee[0].created_by_id
      # if user_name !=None:
      #   phonenum=user_name
      # user = authenticate(username=phonenum, password=password)
      # token, created = Token.objects.get_or_create(user=user)
    user_employee=models.EmployeesMaster.objects.filter(Q(org_n_key=payload['org_n_key']) & Q(employee_n_key=payload['employee_n_key']))
    # for o in user_employee:
    #   o.token=token.key
    emp = serializers.serialize('json',user_employee)
    emp_data = json.loads(emp)
    emp_n_key = encrypt(b'1234567890synaps',emp_data[0]['fields']['employee_n_key'])
    keys = emp_n_key+"/"+RandomString()
    payment_pricing = models.MdPaymentPricing.objects.filter(Q(org_n_key = payload['org_n_key'])&Q(product_name=payload['product_name'])).order_by('-payment_pricing_id')[:1]
    if not payment_pricing:
      return HttpResponse(json.dumps({"status":"payment not found","emp":json.loads(emp),"payment":[],"url":'https://synapstics.com/landing'}),content_type='application/json')
    # employee_details = models.EmployeesMaster.objects.filter(Q(employee_n_key = n_key))
    # bloodbank=''
    # ayush=''
    # hivcare=''
    # gehr=''
    # tm=''
    # for j in employee_details:
    #   bloodbank =j.bloodbank
    #   gehr=j.g_ehr
    # product = OrgProduct(payload['org_n_key'])
    # fill = settingscheck(payload['org_n_key'],product)
    # setting_menu = True if fill != 'success' and (employee and employee[0].role == 'Master' or employee[0].role == 'Careteam') else False
    # print(user_employee[0].role,user_employee[0].product_name)
    if user_employee[0].role != 'Master':
      if user_employee[0].product_name == None or payload['product_name'] not in user_employee[0].product_name:
        return HttpResponse(json.dumps({"status":"You don't have the access for this product.","emp":json.loads(emp),"payment":[],"url":'https://synapstics.com/landing'}),content_type='application/json')
    if payload['product_name'] == 'DigiBlood' or payload['product_name'] == 'bloodbank':
      # if bloodbank=='Yes':
        # if not payment_pricing:
        #   return HttpResponse(json.dumps({"status":"payment not found","emp":json.loads(emp),"payment":[],"url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
        for i in payment_pricing:
          class_data = serializer1.MdPaymentPricingSerializer( payment_pricing, many=True)
          if i.expire_date >= datetime.date.today():
            if payload['product_name'] == 'DigiBlood' or payload['product_name'] == 'bloodbank':
              # return HttpResponse(json.dumps({"status":"success","emp":json.loads(emp),"payment":class_data.data,"url":"https://getdigiblood.synapstics.com/validator/"+payload['employee_n_key']+"/"}),content_type='application/json')
              return HttpResponse(json.dumps({"status":"success","emp":emp_data,"payment":class_data.data,"url":"https://getdigiblood.synapstics.com/validator/"+keys+"/"}),content_type='application/json')
          else:
            sk ='The Payment date expired'
            if i.subscrib_type=='free':
              sk='Your Free Trial Period has Expired. Please Upgrade the Plan'
            return HttpResponse(json.dumps({"status":sk,"emp":emp_data,"payment":class_data.data,"url":'https://synapstics.com/admin_billing'}),content_type='application/json')
      # else:
      #   return HttpResponse(json.dumps({"status":'You did not subscribe this plan please subscribe',"emp":json.loads(emp),"payment":"payment expired","url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
    elif payload['product_name'] == 'ayush':
      # if bloodbank=='Yes':
        # if not payment_pricing:
        #   return HttpResponse(json.dumps({"status":"payment not found","emp":json.loads(emp),"payment":[],"url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
        for i in payment_pricing:
          class_data = serializer1.MdPaymentPricingSerializer( payment_pricing, many=True)
          if i.expire_date >= datetime.date.today():
            if payload['product_name'] == 'ayush':
              return HttpResponse(json.dumps({"status":"success","emp":emp_data,"payment":class_data.data,"url":"https://getayush.synapstics.com/validator/"+keys+"/"}),content_type='application/json')
          else:
            sk ='The Payment date expired'
            if i.subscrib_type=='free':
              sk='Your Free Trial Period has Expired. Please Upgrade the Plan'
            return HttpResponse(json.dumps({"status":sk,"emp":emp_data,"payment":class_data.data,"url":'https://synapstics.com/admin_billing'}),content_type='application/json')
      # else:
      #   return HttpResponse(json.dumps({"status":'You did not subscribe this plan please subscribe',"emp":json.loads(emp),"payment":"payment expired","url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
    elif payload['product_name'] == 'tansacs':
      # if hivcare=='Yes':
        # if not payment_pricing:
        #   return HttpResponse(json.dumps({"status":"payment not found","emp":json.loads(emp),"payment":[],"url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
        for i in payment_pricing:
          class_data = serializer1.MdPaymentPricingSerializer( payment_pricing, many=True)
          if i.expire_date >= datetime.date.today():
            if payload['product_name'] == 'tansacs':
              return HttpResponse(json.dumps({"status":"success","emp":emp_data,"payment":class_data.data,"url":"https://gethivcare.synapstics.com/validator/"+keys+"/"}),content_type='application/json')
          else:
            sk ='The Payment date expired'
            if i.subscrib_type=='free':
              sk='Your Free Trial Period has Expired. Please Upgrade the Plan'
            return HttpResponse(json.dumps({"status":sk,"emp":emp_data,"payment":class_data.data,"url":'https://synapstics.com/admin_billing'}),content_type='application/json')
      # else:
      #   return HttpResponse(json.dumps({"status":'You did not subscribe this plan please subscribe',"emp":json.loads(emp),"payment":"payment expired","url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
    elif payload['product_name'] == 'Mrecs' or payload['product_name'] == 'ehr':
      # if gehr=='Yes':
        # if not payment_pricing:
        #   return HttpResponse(json.dumps({"status":"payment not found","emp":json.loads(emp),"payment":[],"url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
        for i in payment_pricing:
          class_data = serializer1.MdPaymentPricingSerializer( payment_pricing, many=True)
          if i.expire_date >= datetime.date.today():
            if payload['product_name'] == 'Mrecs' or payload['product_name'] == 'ehr':
              return HttpResponse(json.dumps({"status":"success","emp":emp_data,"payment":class_data.data,"url":"https://getehr.synapstics.com/validator/"+keys+"/"}),content_type='application/json')
          else:
            sk ='The Payment date expired'
            if i.subscrib_type=='free':
              sk='Your Free Trial Period has Expired. Please Upgrade the Plan'
            return HttpResponse(json.dumps({"status":sk,"emp":emp_data,"payment":class_data.data,"url":'https://synapstics.com/admin_billing'}),content_type='application/json')
      # else:
      #   return HttpResponse(json.dumps({"status":'You did not subscribe this plan please subscribe',"emp":json.loads(emp),"payment":"payment expired","url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
    elif payload['product_name'] == 'tm':
      # if tm=='Yes':
        # if not payment_pricing:
        #   return HttpResponse(json.dumps({"status":"payment not found","emp":json.loads(emp),"payment":[],"url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
        for i in payment_pricing:
          class_data = serializer1.MdPaymentPricingSerializer( payment_pricing, many=True)
          if i.expire_date >= datetime.date.today():
            if payload['product_name'] == 'bloodbank':
              return HttpResponse(json.dumps({"status":"success","emp":emp_data,"payment":class_data.data,"url":"https://getdigiblood.synapstics.com/validator/"+keys+"/"}),content_type='application/json')
          else:
            sk ='The Payment date expired'
            if i.subscrib_type=='free':
              sk='Your Free Trial Period has Expired. Please Upgrade the Plan'
            return HttpResponse(json.dumps({"status":sk,"emp":emp_data,"payment":class_data.data,"url":'https://synapstics.com/admin_billing'}),content_type='application/json')
      # else:
      #   return HttpResponse(json.dumps({"status":'You did not subscribe this plan please subscribe',"emp":json.loads(emp),"payment":"payment expired","url":'https://synapstics.com/landing','setting_button':setting_button}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({"status":'went wrong',"emp":emp_data,"payment":"payment expired","url":'https://synapstics.com/landing'}),content_type='application/json')
    # else:
    #   return HttpResponse('{"status":"The Username or password you entered is incorrect."}',content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def PaymentandHistoryUpdate(request):
  request = json.loads(request.body.decode('utf-8'))
  data = {"org_n_key":request['org_n_key'],
          "employee_n_key":request['employee_n_key'],
          "created_by_id":request['employee_n_key'],
          "created_by_name":request['employee_name'],
          "paid_amount": 0,
          "product_name":request['product_name'],
          "subscrib_type":"Trial",
          "currentplan_amount":request['plan']['currentplan_ammount'],
          "current_plan":request['plan']['current_plan']
          }
  pricing = PaymentPricingPost(data)
  if request['product_name'] == 'bloodbank':
    hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key']).update(bloodbank='Yes')
    employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=request['employee_n_key']).update(bloodbank='Yes')
  elif request['product_name'] == 'ayush':
    hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key']).update(ayush='Yes')
    employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=request['employee_n_key']).update(ayush='Yes')
  elif request['product_name'] == 'tansacs':
    hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key']).update(hivcare='Yes')
    employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=request['employee_n_key']).update(hivcare='Yes')
  elif request['product_name'] == 'Mrecs':
    hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key']).update(g_ehr='Yes')
    employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=request['employee_n_key']).update(g_ehr='Yes')
  elif request['product_name'] == 'tm':
    hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key']).update(tm='Yes')
    employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=request['employee_n_key']).update(tm='Yes')
  return HttpResponse(json.dumps({"status":"Successfully Saved"}),content_type="application/json")


# generate otp
@csrf_exempt
def ForgotPassword(request):
  request = json.loads(request.body.decode('utf-8'))
  username = models.EmployeesMaster.objects.filter(user_name = request['user_name'])
  if username:
    if username[0].is_active == 0 or username[0].is_active == '0':
      return HttpResponse(json.dumps({"status":"Your account is deactivated. Please contact your admin","emp":{}}),content_type='application/json')    
    serializer_class=serializer1.EmployeesMasterSerializer(username, many=True)
    conn = http.client.HTTPConnection("2factor.in")
    phoneno=username[0].phone_number
    conn.request("POST", "https://2factor.in/API/V1/19ff5a0a-b0eb-11e7-94da-0200cd936042/SMS/+91" + str(phoneno) + "/AUTOGEN/Mrecs")
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    return HttpResponse(json.dumps({"emp":serializer_class.data,"status":"found user_name","data":json_data['Details']}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"Your are entered wrong user name. Please go back and try again"}), content_type="application/json")
  return HttpResponse(json.dumps({"status":"something went wrong"}), content_type="application/json")

@csrf_exempt
def ForgotUsername(request):
  request = json.loads(request.body.decode('utf-8'))
  
  emp_master = models.EmployeesMaster.objects.filter(email =request['email'])
  
  if emp_master:
    for i in emp_master:
      
      sendgrid_client = SendGridAPIClient(
                  api_key='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')
      message = Mail(
            from_email='support@synapstics.com',
            to_emails=i.email,
            subject='',
            html_content='<strong>Verification Mail</strong>')
      message.dynamic_template_data = {
            'user_name':i.user_name           
      }
      message.template_id = 'd-2599cdb69ff942c39c338fc4264a777a'
      response = sendgrid_client.send(message=message)
    return HttpResponse(json.dumps({"status":"User ID has been sent to registed Email id"}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"Email Id not found"}), content_type="application/json")  
  return HttpResponse(json.dumps(""), content_type="application/json")

# forget password  
@csrf_exempt
# @api_view(["POST"])
def ForgotChangePassword(request):
  request = json.loads(request.body.decode('utf-8'))
  check = User.objects.filter(username = request['username'])
  fulldata = []
  if check:
    u = User.objects.get(username=request['username'])
    u.set_password(request['password'])
    u.save()
    models.EmployeesMaster.objects.filter(user_name=request['username']).update(password =request['password'], is_new_user='No')
    return HttpResponse(json.dumps({'status': "Password Changed Successfully Updated"}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"Username is not exist"}),content_type="application/json")


# employee register
class EmployeeDetailsViewSet(viewsets.ModelViewSet):
  queryset=models.EmployeesMaster.objects.all()
  serializer_class=serializer1.EmployeesMasterSerializer
  lookup_field = 'employee_n_key'

@csrf_exempt
@api_view(["POST"])
def Employee_active(request):
  request = json.loads(request.body.decode('utf-8'))
  employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=request['employee_n_key']))
  if employee:
    user = User.objects.get(username = employee[0].user_name)
    user.is_active=request['active']
    user.save()
    employee.update(is_active=request['active'])
    return HttpResponse(json.dumps({'status':'success'}),content_type="application/json")
  return HttpResponse(json.dumps({'status':'failed'}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def GetImage(request):
  request = json.loads(request.body.decode('utf-8'))
  donor_image = models.Attachments.objects.filter(donor_employee_id = request['n_key'])
  
  a = ''
  for i in donor_image:
    a = i.document_attachment
  image_serializer = serializer1.Attachmentsserializer(donor_image, many=True)
  return HttpResponse(json.dumps({"image":str(a)}),content_type="application/json")  

def DoctorWorkCheck(request):
  if 'working_days' not in request:
    return {'success':'success'}
  if 'special_hours' not in request or 'special_hours_closed' not in request:
    return {'success':'success'}
  workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
  if len(workingdetails['working_days']) > 0:
    clinic = models.ClinicalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(clinical_n_key=request['clinical_n_key']))
    if clinic:
     if clinic[0].twenty_four_hours == 'No':
        for i in workingdetails['working_days']: 
          clinic_avail = models.ClinicalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(clinical_n_key=request['clinical_n_key']) & Q(working_days=i['day']) & Q(start_time__lte=i['start_time']) & Q(end_time__gte=i['start_time']) & Q(start_time__lte=i['end_time']) & Q(end_time__gte=i['end_time']))
          if not clinic_avail:
            return {'success':'failed','Data':'Clinics working time not available'}
        for m in workingdetails['special_hours']:
          spec_cli = models.ClinicalSpecialHours.objects.filter(Q(clinical_n_key=request['clinical_n_key']) & Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(special_date=m['date']))
          if spec_cli:
            if m['available'] != 'Closed':
              spec_avail = models.ClinicalSpecialHours.objects.filter(Q(clinical_n_key=request['clinical_n_key']) & Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(special_date=m['date']) & Q(start_time__lte=m['start_time']) & Q(end_time__gte=m['start_time']) & Q(start_time__lte=m['end_time']) & Q(end_time__gte=m['end_time']))
              if not spec_avail:
                return {'success':'failed','data':'Clinic special hours not available'}
  return {'success':'success'}

@csrf_exempt
def EmployeeMasterNew(request):
    request=json.loads(request.body.decode('utf-8'))
    product_name = []
    for j in (request['product_details']):
      product_name.append(j['product_name'])
      if j['product_name'] == 'Mrecs':
        request = {**request, **j}
      if j['product_name'] == 'DigiBlood':
        request['bloodbank_n_key'] = j['bloodbank_n_key']
        request['bloodbank_role'] = j['role']
    request['product_name'] = product_name
    time_check = DoctorWorkCheck(request)
    planing = models.MdPaymentPricing.objects.filter(Q(org_n_key = request['org_n_key']) & Q(product_name__in=product_name)).values('product_name','current_plan')
    for i in planing:
      user = models.EmployeesMaster.objects.filter(Q(org_n_key = request['org_n_key'])&Q(product_name__icontains=j['product_name']))
      plan = models.PlanDetails.objects.filter(Q(product_name = j['product_name']))
      total = user.count()
      plans = plan[0].plan_name.split(',')
      limit = plan[0].employees.split(',')
      plan_name1 = plans.index(i['current_plan'])
      limitz = int(limit[plan_name1])
    if time_check['success'] == 'failed':
      return HttpResponse(json.dumps(time_check),content_type='application/json')
    lettersAndDigits = string.ascii_letters + string.digits
    request['password'] = ''.join(random.choice(lettersAndDigits) for i in range(8))
    phone_check = employee_phone_validate(request['phone_number'],request['org_n_key'],"phone")
    email_check = employee_phone_validate(request['email'],request['org_n_key'],"email")
    if phone_check == "failed":
      if email_check == "failed":
        return HttpResponse(json.dumps({"success":"Phone number and email id already exist","Data":{}}),content_type='application/json')
      return HttpResponse(json.dumps({"success":"Phone number already exist","Data":{}}),content_type='application/json')
    if email_check == "failed":
      return HttpResponse(json.dumps({"success":"email id already exist","Data":{}}),content_type='application/json')
    request['is_active']=1
    try:
      request['created_on'] = TimeZoneConvert(request['hospital_n_key'])
    except Exception as e:
      request['created_on'] = TimeZoneBloodbank(request['bloodbank_n_key'])
    if total >= limitz:
      return HttpResponse(json.dumps({"status":"failed"}),content_type='application/json')
    # value.append({'maximum_count':limitz,'total_user':total})
    employeecreate = serializer1.EmployeesMasterSerializer(data = request)
    if employeecreate.is_valid():
      employeecreate.save()
    else:
      return HttpResponse(json.dumps({"success":"failed","Data":employeecreate.errors}),content_type='application/json')
          
    user_add=User.objects.create_user(password=request['password'], username=employeecreate.data['user_name'], email=request['email'],is_superuser=1,is_staff=1,is_active=1,first_name=request['first_name'],last_name=request['last_name'])
    if user_add:
      token, created = Token.objects.get_or_create(user=user_add)
    sendgrid_client = SendGridAPIClient(
            api_key='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')
    message = Mail(
          from_email='support@synapstics.com',
          to_emails=request['email'],
          subject='',
          html_content='<strong>Verification Mail</strong>')
    message.dynamic_template_data = {
          'username':employeecreate.data['user_name'],
          'password':request['password']
    }
    message.template_id = 'd-8f04908d44814d769e440604b63bd990'
    response = sendgrid_client.send(message=message)
    employee_n_key = employeecreate.data['employee_n_key']
    doc_role = DoctorRoleQuery(request['org_n_key'])
    if (request['role'] in doc_role) or (request['role'] == 'Physician'):
      request['employee_n_key']=employee_n_key
      access = AccessRole(request)
      doctor_post = DoctorEmployee_Post(request)
      work_post = Employee_working_post(request)
    return HttpResponse(json.dumps({"success":"User Created Successfully","Data":employeecreate.data}),content_type='application/json')

def DoctorEmployee_Post(request):
  doctor = models.GeDoctorDetails.objects.filter(Q(employee_n_key=request['employee_n_key']))
  request['phone_number'] = int(request['phone_number'])
  if not doctor:
    request['created_on']=TimeZoneConvert(request['hospital_n_key'])    
    serializer = serializer1.GeDoctorDetailsSerializer(data=request)
    if serializer.is_valid():
      serializer.save()
      return {"status":"success","data":serializer.data}
    else:
      return {"status":"failed","data":serializer.errors}
  else:
    request['modified_on']=TimeZoneConvert(request['hospital_n_key'])
    serializer = serializer1.GeDoctorDetailsSerializer(doctor[0], data=request, partial=True)
    if serializer.is_valid():
      serializer.save()
      # print("doctor updated")
      return {"status":"success","data":serializer.data}
    else:
      return {"status":"failed","data":serializer.errors}

def Employee_working_post(request):
  request['created_on']=TimeZoneConvert(request['hospital_n_key'])
  calendar = serializer1.CalendarSettingsSerializer(data=request)
  if calendar.is_valid():
    calendar.save()
    workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
    if len(workingdetails['working_days']) > 0:
      clinic = models.ClinicalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(clinical_n_key=request['clinical_n_key']))
      if clinic:
        if clinic[0].twenty_four_hours == 'Yes':
          for i in workingdetails['working_days']:
            doctor_work = models.DoctorWorkingDetails.objects.create(doctor_n_key=request['employee_n_key'],clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],
              end_time=i['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=request['created_on'])
        if clinic[0].twenty_four_hours == 'No':
          for i in workingdetails['working_days']: 
            clinic_avail = models.ClinicalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(clinical_n_key=request['clinical_n_key']) & Q(working_days=i['day']) & Q(start_time__lte=i['start_time']) & Q(end_time__gte=i['start_time']) & Q(start_time__lte=i['end_time']) & Q(end_time__gte=i['end_time']))
            if not clinic_avail:
              return {'status':'failed','data':'Clinics working time not available'}
          for j in workingdetails['working_days']:
            doctor_work = models.DoctorWorkingDetails.objects.create(doctor_n_key=request['employee_n_key'],clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'],working_days=j['day'],start_time=j['start_time'],
              end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
          for k in workingdetails['special_hours']:
            special_hours = models.DoctorSpecialHours.objects.create(doctor_n_key=request['employee_n_key'],clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'],special_date=k['date'],available=k['available'],
              start_time=k['start_time'],end_time=k['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
      return ('success')
    return ('')
  else:
    return (calendar.errors)

@csrf_exempt
@api_view(["POST"])
def Delete_employees(request):
  payload = json.loads(request.body.decode('utf-8'))
  cal_delete=models.CalendarSettings.objects.filter(Q(employee_n_key=payload['employee_n_key'])).delete()
  access_delete=models.MdAccess.objects.filter(Q(emp_n_key=payload['employee_n_key'])).delete()
  doc_delete=models.GeDoctorDetails.objects.filter(Q(employee_n_key=payload['employee_n_key'])).delete()
  emp_delete=models.EmployeesMaster.objects.filter(Q(employee_n_key=payload['employee_n_key'])).delete()
  return HttpResponse(json.dumps({"status":"Deleted Successfully"}), content_type="application/json")

def employee_phone_update(value,hospital_n_key,key,employee_n_key):
  if key == "phone":
    employee = models.EmployeesMaster.objects.filter(Q(hospital_n_key=hospital_n_key)&Q(phone_number=value)& ~Q(employee_n_key=employee_n_key))
    if employee:
      return "failed"
    return "success"
  if key == "email":
    employee = models.EmployeesMaster.objects.filter(Q(hospital_n_key=hospital_n_key)&Q(email=value)& ~Q(employee_n_key=employee_n_key))
    if employee:
      return "failed"
    return "success"

@csrf_exempt
def EmployeeUpdateRegister(request):
  request = json.loads(request.body.decode('utf-8'))
  check = User.objects.filter(username = request['user_name'])
  emp = models.EmployeesMaster.objects.filter(employee_n_key=request['employee_n_key'])
  fulldata = []
  if check:
    product_name = []
    if 'product_details' in request and len(request['product_details']):
      for j in request['product_details']:
        product_name.append(j['product_name'])
        if j['product_name'] == 'Mrecs':
          request = {**request, **j}
        if j['product_name'] == 'DigiBlood':
          request['bloodbank_n_key'] = j['bloodbank_n_key']
          request['bloodbank_role'] = j['role']
      request['product_name'] = product_name

    time_check = DoctorWorkCheck(request)
    if time_check['success'] == 'failed':
      return HttpResponse(json.dumps(time_check),content_type='application/json')

    phone_check = employee_phone_update(request['phone_number'],request['hospital_n_key'],"phone",request['employee_n_key'])
    email_check = employee_phone_update(request['email'],request['hospital_n_key'],"email",request['employee_n_key'])
    if phone_check == "failed":
      if email_check == "failed":
        return HttpResponse(json.dumps({"status":"Phone number and email id already exist"}),content_type='application/json')
      return HttpResponse(json.dumps({"status":"Phone number already exist"}),content_type='application/json')
    if email_check == "failed":
      return HttpResponse(json.dumps({"status":"email id already exist"}),content_type='application/json')

    u = User.objects.get(username=request['user_name'])
    u.set_password(request['password'])
    u.save()
    request['modified_on'] = TimeZoneConvert(request['hospital_n_key'])
    serializer = serializer1.EmployeesMasterSerializer(emp[0], data = request, partial=True)
    if serializer.is_valid():
      serializer.save()
    doc_role = DoctorRoleQuery(request['org_n_key'])
    if (request['role'] in doc_role) or (request['role'] == 'Physician'):
      access = AccessRole(request)
      doctor_post = DoctorEmployee_Post(request)
      work_post = Employee_working_update(request,emp)
    return HttpResponse(json.dumps({'status': "Successfully Updated"}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"User not found"}),content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def Doctordetails_update(request):
  request = json.loads(request.body.decode('utf-8'))
  access=models.GeDoctorDetails.objects.all()
  fulldata=[]
  fits = access.filter(employee_n_key=request['employee_n_key']).values_list('doct_id',flat=True)
  if fits:
    fits1=access.get(doct_id=fits[0])
    request['modified_on']=DefaultTimeZone()
    serializer = serializer1.GeDoctorDetailsSerializer(instance=fits1,data=request, partial=True)
    if serializer.is_valid():
      serializer.save()
      fulldata.append({'list': serializer.data,'status': "Updated Successfully"})
  return HttpResponse(json.dumps(fulldata),content_type="application/json")

@csrf_exempt
@api_view(['POST'])
def EmployeeRegisterSMS(request):
  request = json.loads(request.body.decode('utf-8'))
  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  enable_sms =  models.SmsSettings.objects.filter(Q(org_n_key = request['org_n_key']) & Q(enable_sms = 'Yes') & Q(total_count__gt= 1) &Q(enable_registration_sms='Yes'))
  if enable_sms:
    for i in enable_sms:
      json_data= {"Status":"Success"}
      if json_data['Status'] =='Success':
        if len(i.registration_sms_content) <=140:
          remaining_sms = int(i.total_count) - 1
        else:
          remaining_sms = int(i.total_count) - 2
        models.SmsSettings.objects.filter(org_n_key = request['org_n_key']).update(remaining_sms =remaining_sms)
        models.SmsHistory.objects.create(org_n_key = request['org_n_key'],
            phone_number = request["phone_number"],sms_status = json_data['Status'],
            sms_type = 'Transactional Message',created_on = datetime.date.today(),created_time =current_time
            )
        return HttpResponse(json.dumps({'status':'sms send successfully'}),content_type='application/json')
      else:
        models.SmsHistory.objects.create(org_n_key = request['org_n_key'],
            phone_number = request["phone_number"],sms_status = json_data['Status'],
            sms_type = 'Transactional Message',created_on = datetime.date.today(),created_time =current_time
            )
        return HttpResponse(json.dumps({'status':'send sms failed'}),content_type='application/json')
  else:
    return HttpResponse(json.dumps({'status':'sms is not enabled'}),content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def organiz_products(request):
  request = json.loads(request.body.decode('utf-8'))
  alldata = []
  organiz = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(role='Master'))
  if organiz:
    if organiz[0].bloodbank == 'Yes':
      alldata.append("bloodbank")
    if organiz[0].g_ehr == 'Yes':
      alldata.append("g_ehr")
  return HttpResponse(json.dumps({"products":alldata}),content_type='application/json')
@csrf_exempt
@api_view(["POST"])
def ImageUpload(request):
  if request.method == 'POST' and request.FILES['document_attachment']:
    myfile = request.FILES['document_attachment']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    find = models.Attachments.objects.filter(donor_employee_id = request.POST['n_key'])
    http_address = ''
    if find:
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        http_address = 'http://'
        models.Attachments.objects.filter(donor_employee_id = request.POST['n_key']).update(document_attachment=http_address + request.get_host() + uploaded_file_url)
        return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
      else:
        http_address = 'https://'
        models.Attachments.objects.filter(donor_employee_id = request.POST['n_key']).update(document_attachment=http_address + request.get_host() + "/api"+ uploaded_file_url)
        return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
    else:
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        http_address = 'http://'
        donor_image = models.Attachments.objects.create(document_attachment= http_address + request.get_host() + uploaded_file_url,donor_employee_id = request.POST['n_key'])
        return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
      else:
        http_address = 'https://'
        donor_image = models.Attachments.objects.create(document_attachment= http_address + request.get_host() + "/api" + uploaded_file_url,donor_employee_id = request.POST['n_key'])
        return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
    donor_image = models.Attachments.objects.create(document_attachment=request.get_host() + uploaded_file_url,donor_employee_id = request.POST['n_key'])
    return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
  return HttpResponse("")
    
def EmpWorkingFormat(employee_n_key):
  emp_work = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=employee_n_key)).values('working_days','start_time','end_time')
  today = datetime.datetime.today().date()
  emp_spec = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=employee_n_key) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
  working_format = []
  non_working = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
  for z in non_working:
    slots = {}
    daycheck = emp_work.filter(working_days=z)
    if daycheck:
      slots['day'] = z
      slots['count'] = len(daycheck)
      slots['work_hours'] = []
      for l in daycheck:
        slots['work_hours'].append({'start_time':l['start_time'].strftime('%I:%M %p'),'end_time':l['end_time'].strftime('%I:%M %p')})
      working_format.append(slots)
  return working_format

@csrf_exempt
@api_view(["POST"])
def EmployeesListForHospital(request):
  request = json.loads(request.body.decode('utf-8'))
  def addRole(data):
    for k in data:
      role = []
      role.append(k['role']) if k['role'] != None and k['role'] != '' else None
      role.append(k['bloodbank_role']) if k['bloodbank_role'] != None and k['bloodbank_role'] != '' else None
      k['role'] = ','.join(role)
    return data
  if request:
    all_emp = addRole(list(models.EmployeesMaster.objects.filter(Q(org_n_key = request['org_n_key'])).values('employee_id','employee_n_key','first_name','role','gender','phone_number','org_n_key','hospital_n_key','is_active','product_name','bloodbank_role')))
    active = addRole(list(models.EmployeesMaster.objects.filter(Q(org_n_key = request['org_n_key']) & Q(is_active='1')).values('employee_id','employee_n_key','first_name','role','gender','phone_number','org_n_key','hospital_n_key','is_active','product_name','bloodbank_role')))
    inactive = addRole(list(models.EmployeesMaster.objects.filter(Q(org_n_key = request['org_n_key']) & Q(is_active='0')).values('employee_id','employee_n_key','first_name','role','gender','phone_number','org_n_key','hospital_n_key','is_active','product_name','bloodbank_role')))
    today = datetime.datetime.today().date()
    for j in active:
      if j['role'] != 'Master':
        role = models.GERoles.objects.filter(roles_name = j['role'])
        j['role_check'] = 'Yes' if j['role'] == 'Physician' else role[0].role_check if role and role[0].role_check != None and role[0].role_check != '' else 'No'
      else:
        j['role_check'] = 'No'
    all_emp = json.dumps(all_emp, default = decimal_default)
    active = json.dumps(active, default = decimal_default)
    inactive = json.dumps(inactive, default = decimal_default)
    return HttpResponse(json.dumps({"Alldata_status":json.loads(all_emp),"Active_status":json.loads(active),"Inactive_status":json.loads(inactive)}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"no request"}), content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def GetEmployeeWorkinghours(request):
  request = json.loads(request.body.decode('utf-8'))
  return_data = {}
  today = datetime.datetime.today().date()
  return_data['working_hours'] = EmpWorkingFormat(request['employee_n_key'])
  emp_work = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=request['employee_n_key'])).values('working_days','start_time','end_time')
  emp_spec = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=request['employee_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
  convert = ReArrangeWorking(emp_work,emp_spec)
  for k in convert['special_hours']:
    k['count'] = len(k['times'])
  return_data['special_hours'] = convert['special_hours']
  return_data['special_hours_closed'] = convert['special_hours_closed']
  return_data['total_hours'] = convert['total_hours']
  return HttpResponse(json.dumps({"status":"success","data":return_data}), content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def GeDoctorDetailsPost(request):
  data = JSONParser().parse(request)
  data['created_on']=TimeZoneConvert(data['hospital_n_key'])
  serializer =serializer1.GeDoctorDetailsSerializer(data=data)
  if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=204)
  return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def GeDoctorDetails_detail(request, pk):
  """
  Retrieve, update or delete a code snippet.
  """
  try:
    snippet =models.GeDoctorDetails.objects.get(pk=pk)
  except models.GeDoctorDetails.DoesNotExist:
    return HttpResponse(json.dumps({"data":"no data found"}),content_type="application/json")
  if request.method == 'GET':
    serializer =serializer1.GeDoctorDetailsSerializer(snippet)
    return JsonResponse(serializer.data)
  elif request.method == 'PUT':
    hospital = models.HospitalMaster.objects.filter(hospital_n_key=request.data['hospital_n_key'])
    request.data['modified_on']=DefaultTimeZone()
    serializer =serializer1.GeDoctorDetailsSerializer(snippet, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    snippet.delete()
    return HttpResponse(json.dumps({"data":"data deleted successfully"}),content_type="application/json")

@csrf_exempt
def Employeelog_delete(request):
  request  = json.loads(request.body.decode('utf-8'))
  log = models.EmployeeLogs.objects.filter(Q(employee_n_key=request['employee_n_key']))
  if log:
    log.delete()
  return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")


# currency details
@csrf_exempt
@api_view(["POST"])
def Currency_Detail_Search(request):
    payload = json.loads(request.body.decode('utf-8'))
    currency=models.CurrencyTable.objects.filter(Q(currency_country_name=payload['currency_country_info']) | Q(currency_country_name__startswith=payload['currency_country_info']) | Q (currency_country_name__icontains=payload['currency_country_info']))
    if currency:
        currencydetails=serializers.serialize('json', currency)
        return HttpResponse(currencydetails,content_type='application/json')
    else:
        return HttpResponse(" ")

@csrf_exempt
@api_view(["POST"])
def CurrencyDetailsPost(request):
  data = JSONParser().parse(request)
  data['created_on']=DefaultTimeZone()
  serializer =serializer1.CurrencyDetailsSerializer(data=data)
  if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=204)
  return Response(serializer.data, status=status.HTTP_201_CREATED)
@csrf_exempt
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def CurrencyDetails(request, pk):
  """
  Retrieve, update or delete a code snippet.
  """
  try:
    snippet =models.CurrencyDetails.objects.get(pk=pk)
  except models.CurrencyDetails.DoesNotExist:
    return HttpResponse(json.dumps({"data":"no data found"}),content_type="application/json")
  if request.method == 'GET':
    serializer =serializer1.CurrencyDetailsSerializer(snippet)
    return JsonResponse(serializer.data)
  elif request.method == 'PUT':
    request.data['modified_on']=DefaultTimeZone()
    serializer =serializer1.CurrencyDetailsSerializer(snippet, data=request.data,partial=True)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    snippet.delete()
    return HttpResponse(json.dumps({"data":"data deleted successfully"}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Currencyhospital_details(request):
  payload = json.loads(request.body.decode('utf-8'))
  currency= models.CurrencyDetails.objects.filter(Q(hospital_n_key=payload['hospital_n_key']))
  currency_key= models.CurrencyDetails.objects.filter(Q(hospital_n_key=payload['hospital_n_key'])).values('currency_id')
  if currency:
    serializer_class = serializer1.CurrencyDetailsTableSerializer(currency, many=True).data
    return HttpResponse(json.dumps(serializer_class), content_type="application/json")
  return HttpResponse(json.dumps([]), content_type="application/json")


# clinic details
@csrf_exempt
@api_view(["POST"])
def Clinic_Timing_Validation(request):
  request = json.loads(request.body.decode('utf-8'))
  hos_work_data = []
  hos_spec_data = []
  hospital = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']))
  if hospital:
    today = datetime.datetime.now(timezone(hospital[0].time_zone)).date()
    twen_four = hospital[0].twenty_four_hours
    hospital_work = models.HospitalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key'])).values('working_days','start_time','end_time')
    hospital_spec = models.HospitalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
    hospital_data = serializer1.HospitalMasterSerializer(hospital, many=True).data
    hospital_data[0]['working_days'] = {}
    hospital_data[0]['special_hours'] = []
    if hospital[0].twenty_four_hours == 'Yes':
      work_details = {"sunday":[],"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[]}
      return HttpResponse(json.dumps({'status':twen_four,'working_details':work_details,'special_hours':[],"check_days":[],"special_hours_closed":[]}),content_type="application/json")
    convert = ReArrangeWorking(hospital_work,hospital_spec)
    return HttpResponse(json.dumps({'status':twen_four,'working_details':convert['working_days'],'special_hours':convert['special_hours'],'special_hours_closed':convert['special_hours_closed'],"check_days":convert['avail_date']}),content_type="application/json")
  return HttpResponse(json.dumps({'status':'No Hospital Details Found'}),content_type="application/json")

@csrf_exempt
def HospitalDetails(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital = models.HospitalMaster.objects.filter(org_n_key= request['org_n_key'])
  hospital_serializer = serializer1.HospitalSerializer(hospital, many=True)
  return HttpResponse(json.dumps({'hospital_information':hospital_serializer.data}),content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def clinicalworkpost(request):
  request = json.loads(request.body.decode('utf-8'))
  data = []
  clinic = request['clinical_name']
  split_clinic = clinic.split(' ')
  short = ''
  hospital = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(hospital_n_key=request['hospital_n_key']))
  workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
  if hospital[0].twenty_four_hours == 'No':
    if request['twenty_four_hours'] == "Yes":
      return HttpResponse(json.dumps({'status':'Hospital working time not available'}),content_type="application/json")
    if len(workingdetails['working_days']) > 0:
      for k in workingdetails['working_days']:
        if (k['start_time'] !='') and (k['start_time'] != None):
          hospital_avail = models.HospitalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(working_days=k['day']) & Q(start_time__lte=k['start_time']) & Q(end_time__gte=k['start_time']) & Q(start_time__lte=k['end_time']) & Q(end_time__gte=k['end_time']))
          if not hospital_avail:
            return HttpResponse(json.dumps({'status':'Hospital working time not available'}),content_type="application/json")
    if len(workingdetails['special_hours']) > 0:
      for m in workingdetails['special_hours']:
        if (m['start_time'] !='') and (m['end_time'] != None):
          spec_hos = models.HospitalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(special_date=m['date']))
          if spec_hos:
            spec_avail = models.HospitalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(special_date=m['date']) & Q(start_time__lte=m['start_time']) & Q(end_time__gte=m['start_time']) & Q(start_time__lte=m['end_time']) & Q(end_time__gte=m['end_time']))
            if not spec_avail:
              return HttpResponse(json.dumps({'status':'Hospital special hours not available'}),content_type="application/json")
  if len(split_clinic) >= 3:
    for i in range(0,len(split_clinic)):
      if i <= 2:
        data.append(split_clinic[i][0])
    s = [str(i) for i in data]
    short = str("".join(s)).upper()
  if len(split_clinic) > 1 and len(split_clinic) <= 2:
    for i in range(0,len(split_clinic)):
      if i == 1:
        data.append(split_clinic[i][0])
      else:
        data.append(split_clinic[i][:2])
    s = [str(i) for i in data]
    short = str("".join(s)).upper()
  if len(split_clinic) == 1:
    s = [str(i) for i in split_clinic]
    short = str("".join(s)).upper()
    short = short[:3]

  clin_create = models.ClinicalMaster.objects.create(hospital_n_key=request.get('hospital_n_key'),org_n_key=request.get('org_n_key'),clinical_name=request.get('clinical_name'),clinical_short=short,
    clinical_phone_number=int(request.get('clinical_phone_number')),licence_number=request.get('licence_number'),gst_number=request.get('gst_number'),speciality=request.get('speciality'),allow_online_appointments=request.get('allow_online_appointments'),
    clinical_address=request.get('clinical_address'),state=request.get('state'),twenty_four_hours=request.get('twenty_four_hours'),
    district=request.get('district'),taluk=request.get('taluk'),city=request.get('city'),pincode=0,created_by_id=request.get('created_by_id'),created_by_name=request.get('created_by_name'),created_on=DefaultTimeZone())
  clinical = models.ClinicalMaster.objects.filter(Q(org_n_key=request['org_n_key'])).order_by('-clinical_id')
  clinic_key = clinical[0].clinical_n_key

  if hospital:
    if hospital[0].twenty_four_hours == 'Yes':
      if request['twenty_four_hours'] != "Yes":
        if len(workingdetails['working_days']) > 0:
          for i in workingdetails['working_days']:
            if (i['start_time'] !='') and (i['start_time'] != None):
              clinic_working = models.ClinicalWorkingDetails.objects.create(clinical_n_key=clin_create.clinical_n_key,hospital_n_key=request['hospital_n_key'],working_days=i['day'],start_time=i['start_time'],org_n_key=request['org_n_key'],
                end_time=i['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=request['created_on'])

    if hospital[0].twenty_four_hours == 'No':
      if len(workingdetails['working_days']) > 0:
        for i in workingdetails['working_days']:
          if (i['start_time'] !='') and (i['start_time'] != None):
            clinic_working = models.ClinicalWorkingDetails.objects.create(clinical_n_key=clin_create.clinical_n_key,hospital_n_key=request['hospital_n_key'],working_days=i['day'],start_time=i['start_time'],org_n_key=request['org_n_key'],
              end_time=i['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
      for j in workingdetails['special_hours']:
        special_hours = models.ClinicalSpecialHours.objects.create(clinical_n_key=clin_create.clinical_n_key,hospital_n_key=request['hospital_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],org_n_key=request['org_n_key'],
          end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
  return HttpResponse(json.dumps({"status":"success","clinical_n_key":clinic_key}),content_type='application/json') 

@csrf_exempt
def Clinical_Working_Details_Edit(request):
  request = json.loads(request.body.decode('utf-8'))
  clinical = models.ClinicalMaster.objects.filter(clinical_n_key=request['clinical_n_key'])
  hospital = models.HospitalMaster.objects.filter(Q(hospital_n_key=clinical[0].hospital_n_key))
  today = datetime.datetime.now(timezone(hospital[0].time_zone)).date()
  hos_work_data = []
  hos_spec_data = []
  clinical_work = models.ClinicalWorkingDetails.objects.filter(Q(clinical_n_key=request['clinical_n_key'])).values('working_days','start_time','end_time')
  clinical_spec = models.ClinicalSpecialHours.objects.filter(Q(clinical_n_key=request['clinical_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
  clinical_data = serializer1.ClinicalMasterSerializer(clinical, many=True).data
  clinical_data[0]['working_days'] = {}
  clinical_data[0]['special_hours'] = []
  if clinical[0].twenty_four_hours == 'Yes':
    work_details = {"sunday":[],"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[]}
    return HttpResponse(json.dumps({"clinical":clinical_data,"working_details":work_details,"special_hours":[],"check_days":[],"special_hours_closed":[]}),content_type="application/json")
  convert = ReArrangeWorking(clinical_work,clinical_spec)
  return HttpResponse(json.dumps({"clinical":clinical_data,"working_details":convert['working_days'],"special_hours":convert['special_hours'],'special_hours_closed':convert['special_hours_closed'],"check_days":convert['avail_date']}),content_type="application/json")
  
 
@csrf_exempt
@api_view(["POST"])
def Clinic_working_Update(request):
  request = json.loads(request.body.decode('utf-8'))
  clinic = models.ClinicalMaster.objects.filter(Q(clinical_n_key=request['clinical_n_key']))
  if clinic:
    clinic_up = clinic.update(clinical_phone_number=request.get('clinical_phone_number'),licence_number=request.get('licence_number'),gst_number=request.get('gst_number'),speciality=request.get('speciality'),allow_online_appointments=request.get('allow_online_appointments'),twenty_four_hours=request.get('twenty_four_hours'),
    clinical_address=request.get('clinical_address'),state=request.get('state'),district=request.get('district'),taluk=request.get('taluk'),city=request.get('city'),pincode=request.get('pincode'),modified_by_id=request.get('modified_by_id'),modified_by_name=request.get('modified_by_name'),modified_on=TimeZoneConvert(request['hospital_n_key']))

    workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
    hospital = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(hospital_n_key=request['hospital_n_key']))
    if hospital[0].twenty_four_hours == 'No':
      if request['twenty_four_hours'] == "Yes":
        return HttpResponse(json.dumps({'status':'Hospital working time not available'}),content_type="application/json")
      if len(workingdetails['working_days']) > 0:
        for k in workingdetails['working_days']:
          if (k['start_time'] !='') and (k['start_time'] != None):
            hospital_avail = models.HospitalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(working_days=k['day']) & Q(start_time__lte=k['start_time']) & Q(end_time__gte=k['start_time']) & Q(start_time__lte=k['end_time']) & Q(end_time__gte=k['end_time']))
            if not hospital_avail:
              return HttpResponse(json.dumps({'status':'Hospital working time not available'}),content_type="application/json")
      if len(workingdetails['special_hours']) > 0:
        for m in workingdetails['special_hours']:
          if (m['start_time'] !='') and (m['end_time'] != None):
            spec_hos = models.HospitalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(special_date=m['date']))
            if spec_hos:
              spec_avail = models.HospitalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(special_date=m['date']) & Q(start_time__lte=m['start_time']) & Q(end_time__gte=m['start_time']) & Q(start_time__lte=m['end_time']) & Q(end_time__gte=m['end_time']))
              if not spec_avail:
                return HttpResponse(json.dumps({'status':'Hospital special hours not available'}),content_type="application/json")      
    if hospital:
      work_filter = models.ClinicalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(clinical_n_key=request['clinical_n_key']))
      if work_filter:
        work_del = work_filter.delete()
      if hospital[0].twenty_four_hours == 'Yes':
        if request['twenty_four_hours'] != "Yes":
          if len(workingdetails['working_days']) > 0:            
            for i in workingdetails['working_days']:
              if (i['start_time'] !='') and (i['start_time'] != None):
                clinic_working = models.ClinicalWorkingDetails.objects.create(clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],working_days=i['day'],start_time=i['start_time'],org_n_key=request['org_n_key'],
                  end_time=i['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=TimeZoneConvert(request['hospital_n_key']))
      if hospital[0].twenty_four_hours == 'No':
        if len(workingdetails['working_days']) > 0:
          for k in workingdetails['working_days']:
            if (k['start_time'] !='') and (k['start_time'] != None):
              hospital_avail = models.HospitalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(working_days=k['day']) & Q(start_time__lte=k['start_time']) & Q(end_time__gte=k['start_time']) & Q(start_time__lte=k['end_time']) & Q(end_time__gte=k['end_time']))
              if not hospital_avail:
                return HttpResponse(json.dumps({'status':'Hospital working time not available'}),content_type="application/json")           
          for i in workingdetails['working_days']:
            if (i['start_time'] !='') and (i['start_time'] != None):
              clinic_working = models.ClinicalWorkingDetails.objects.create(clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],working_days=i['day'],start_time=i['start_time'],org_n_key=request['org_n_key'],end_time=i['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=TimeZoneConvert(request['hospital_n_key']))

      spec_filter = models.ClinicalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(org_n_key=request['org_n_key']) & Q(clinical_n_key=request['clinical_n_key']))
      if spec_filter:
        spec_del = spec_filter.delete()
      for j in workingdetails['special_hours']:
        special_hours = models.ClinicalSpecialHours.objects.create(clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],org_n_key=request['org_n_key'],end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=TimeZoneConvert(request['hospital_n_key']))
      return HttpResponse(json.dumps({'status':'success'}),content_type="application/json")       
    else:
      return HttpResponse(json.dumps({'status':'no hospital found'}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({'status':'no clinic found'}),content_type="application/json")
  return HttpResponse(json.dumps({'status':'success'}),content_type="application/json")

@csrf_exempt
def Clinical_List(request):
    request = json.loads(request.body.decode('utf-8'))
    clinic=models.ClinicalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
    if clinic:
        clinicdetails = serializer1.ClinicalMasterSerializer(clinic, many=True).data
        return HttpResponse(json.dumps(clinicdetails),content_type='application/json')
    else:
        return HttpResponse(json.dumps(""),content_type='application/json')

# change plan
@csrf_exempt
def ChangePasswordRegister(request):
  request = json.loads(request.body.decode('utf-8'))
  check = User.objects.filter(username = request['username'])
  fulldata = []
  if check:
      u = User.objects.get(username=request['username'])
      u.set_password(request['password'])
      u.save()
      models.EmployeesMaster.objects.filter(user_name=request['username']).update(password =request['password'], is_new_user='No')
      return HttpResponse(json.dumps({'status': "Password Changed Successfully Updated"}),content_type="application/json")
  else:
      return HttpResponse(json.dumps({"status":"Username is not exist"}),content_type="application/json")

# buy product
@csrf_exempt
@api_view(["POST"])
def Payment_Hospital_Update(request):
  request = json.loads(request.body.decode('utf-8'))
  today = datetime.date.today()
  expiry_date = today + datetime.timedelta(days=7)
  fulldata = []
  for i in request:
    if i['plan'] != [] and i['plan'] != {}:
      data = {"org_n_key":i['org_n_key'],
              "employee_n_key":i['employee_n_key'],
              "created_by_id":i['employee_n_key'],
              "created_by_name":i['employee_name'],
              "paid_amount": 0,
              "product_name":i['name'],
              "subscrib_type":"Trial",
              "currentplan_amount":i['plan']['currentplan_ammount'],
              "current_plan":i['plan']['current_plan']
              }
      pricing = PaymentPricingPost(data)
      payment_pricing = serializer1.MdPaymentPricingSerializer(data=request)
      
      # payment_pricing = models.MdPaymentPricing.objects.create(project_name=request[i]['search'],org_n_key=request[i]['org_n_key'],plan_name=request[i]['plan']['plan_name'], current_plan=request[i]['plan']['current_plan'],
      #    payment_date=datetime.datetime.today(),
      #  subscrib_type='free', currentplan_ammount=request[i]['plan']['currentplan_ammount'],  paid_ammount='0', gst=18,
      #  expire_date=expiry_date,adjustments='0',status='Completed',full_name=request[i]['plan']['full_name'], short_name=request[i]['plan']['short_name'], created_by_id=request[i]['employee_n_key'], created_by_name=request[i]['employee_name'], created_on=DefaultTimeZone())

      # payment_history = models.MdPaymentHistory.objects.create(project_name=request[i]['search'],plan_name=request[i]['plan']['plan_name'], current_plan=request[i]['plan']['current_plan'],
      #  org_n_key=request[i]['org_n_key'], payment_date=datetime.datetime.today(),
      #  subscrib_type='free', currentplan_ammount=request[i]['plan']['currentplan_ammount'],  paid_ammount='0', gst=18,
      #  expire_date=expiry_date,adjustments='0',reason='',status='Completed',full_name=request[i]['plan']['full_name'], short_name=request[i]['plan']['short_name'], created_by_id=request[i]['employee_n_key'], created_by_name=request[i]['employee_name'], created_on=DefaultTimeZone())
      if i['name'] == 'DigiBlood':
        hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=i['org_n_key']).update(bloodbank='Yes')
        employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=i['employee_n_key']).update(bloodbank='Yes')
      elif i['name'] == 'ayush':
        hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=i['org_n_key']).update(ayush='Yes')
        employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=i['employee_n_key']).update(ayush='Yes')
      elif i['name'] == 'tansacs':
        hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=i['org_n_key']).update(hivcare='Yes')
        employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=i['employee_n_key']).update(hivcare='Yes')
      elif i['name'] == 'Mrecs':
        hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=i['org_n_key']).update(g_ehr='Yes')
        employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=i['employee_n_key']).update(g_ehr='Yes')
      elif i['name'] == 'tm':
        hospital_detail = models.OrganizationMaster.objects.filter(org_n_key=i['org_n_key']).update(tm='Yes')
        employee_detail = models.EmployeesMaster.objects.filter(employee_n_key=i['employee_n_key']).update(tm='Yes')
  # product = OrgProduct(request[0]['org_n_key'])
  # fill = settingscheck(request[0]['org_n_key'],product)
  product = OrgProduct(request[0]['org_n_key'])
  check_condition = 'hospital' if 'Mrecs' in product else 'bloodbank' if 'DigiBlood' in product else None
  return HttpResponse(json.dumps({"status":"Successfully Saved","setting_menu":check_condition}),content_type="application/json")


# new page
@permission_classes((AllowAny,))
class SubscribersViewSet(viewsets.ModelViewSet):
  queryset = models.SubscribersMaster.objects.all()
  serializer_class = serializer1.SubScribersSerializer
  lookup_field = 'subscribers_id'



def AmountPayment(request1,status1):
  requests = request1

  status = status1

  today = datetime.date.today()
  fulldata = []
  if status == 'captured':
    sms_setting = models.SmsSettings.objects.filter(clinical_short_name = requests['hospital_short_name'])
    remaining = 0
    total =''
    for i in sms_setting:
        remaining = i.remaining_sms
        total = i.total_count
    total  = int(remaining) + int(requests['purchase_sms'])
    update = models.SmsSettings.objects.filter(clinical_short_name=requests['hospital_short_name']).update(remaining_sms=0,total_count=total)
    sms_payment_history = models.SmsPaymentHistory.objects.create(payment_amount=requests['amount'],purchased_sms = requests['purchase_sms'],
                                                   payment_date = datetime.date.today(),created_by_id=requests['created_by_id'],payment_status ='Payment Success',
                                                   created_by_name = requests['created_by_name'],created_on = datetime.date.today())
    return HttpResponse(json.dumps({"status":"Payment Success"}),content_type="application/json")
  else:
      sms_payment_history = models.SmsPaymentHistory.objects.create(payment_amount=requests['amount'],purchased_sms = requests['purchase_sms'],
                                                   payment_date = datetime.date.today(),created_by_id=requests['created_by_id'],payment_status ='Payment Failed',
                                                   created_by_name = requests['created_by_name'],created_on = datetime.date.today())
      return HttpResponse(json.dumps({"status": "Payment Failed"}), content_type="application/json")
  return HttpResponse(json.dumps({"status": ""}), content_type="application/json")
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()        
        return HttpResponse('<h3>Thank you for your email confirmation. Now you can login your account.<a href="https://synapstics.com/login">Click Me</a></h3>')
    else:
        return HttpResponse('Activation link is invalid!')



# profile
@permission_classes((AllowAny,))  
class SmsSettingsViewSet(viewsets.ModelViewSet):
  queryset=models.SmsSettings.objects.all()
  serializer_class=serializer1.SMSSerializer
  lookup_field = 'org_n_key'

@permission_classes((AllowAny,))
class EmpeducationaldetailsViewSet(viewsets.ModelViewSet):
  queryset=models.Empeducationaldetails.objects.all()
  serializer_class=serializer1.EmpeducationaldetailsSerializer
  lookup_field = 'edu_n_key'
@permission_classes((AllowAny,))  
class EmployeeProfessionalViewSet(viewsets.ModelViewSet):
  queryset=models.EmployeeProfessional.objects.all()
  serializer_class=serializer1.EmployeeProfessionalSerializer
  lookup_field = 'pro_n_key'
@permission_classes((AllowAny,))  
class EmployeeTrainingViewSet(viewsets.ModelViewSet):
  queryset=models.EmployeeTraining.objects.all()
  serializer_class=serializer1.EmployeeTrainingSerializer
  lookup_field = 'training_n_key'
@permission_classes((AllowAny,))  
class EmployeeTeachExperienceViewSet(viewsets.ModelViewSet):
  queryset=models.EmployeeTeachExperience.objects.all()
  serializer_class=serializer1.EmployeeTeachExperienceSerializer
  lookup_field = 'exp_teach_n_key'


@permission_classes((AllowAny,))  
class EmployeeExperienceViewSet(viewsets.ModelViewSet):
  queryset=models.EmployeeExperience.objects.all()
  serializer_class=serializer1.EmployeeExperienceSerializer
  lookup_field = 'exp_n_key'


@permission_classes((AllowAny,))  
class EmployeeRestrictionViewSet(viewsets.ModelViewSet):
  queryset=models.EmployeeRestriction.objects.all()
  serializer_class=serializer1.EmployeeRestrictionSerializer
  lookup_field = 'practice_n_key'  

@csrf_exempt
@api_view(["POST"])
def Check_Employee_forms(request):
  request  = json.loads(request.body.decode('utf-8'))
  percentage=0
  fulldata=[]
  edu = models.Empeducationaldetails.objects.filter(Q(org_n_key=request['org_n_key']) & Q(employee_n_key=request['employee_n_key']))
  emp = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(employee_n_key=request['employee_n_key']))
  
  if emp:
    for i in emp:
      if i.age!=None and i.age !='' and i.blood_group!=None and i.blood_group!= '' and i.emergency_person_name!=None and i.emergency_person_name!=''  and i.emergency_contact_no!= None and i.emergency_contact_no!='':
        pass
      else:
        percentage += 1
        fulldata.append('Employee Profile')
  if not edu:
    percentage += 1
    fulldata.append('Education')
  require = []
  roles = models.GERoles.objects.filter(Q(org_n_key=request['org_n_key']) & Q(roles_name=request['roles_name']))
  if roles and roles[0].document!=None and roles[0].document!='':
    require = (roles[0].document).split(',')
  for x in require:
    docs = models.EmployeeOtherDocument.objects.filter(Q(employee_n_key=request['employee_n_key'])&Q(document_name=x))
    if not docs:
      percentage += 1
      if 'Documents' not in fulldata:
        fulldata.append('Documents')
  doc_role = DoctorRoleQuery(request['org_n_key'])
  if (emp[0].role in doc_role) or (emp[0].role == 'Physician'):
    emp_work = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=request['employee_n_key']))
    if not emp_work:
      percentage += 1
      fulldata.append('Working Details')
  if percentage != 0:
    info = ','.join(fulldata)
    return HttpResponse(json.dumps({"status":"failed","percentage":percentage,"info":"User need to update this {} Detail(s) to proceed further".format(info)}), content_type="application/json")    
  else:
    return HttpResponse(json.dumps({"status":"success","percentage":percentage}), content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def Emp_educational_details(request):
  if request.method == 'POST':
    myfile = request.FILES.get('document_attachment')
    if myfile!=None:
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
    hospital = models.HospitalMaster.objects.filter(hospital_n_key=request.POST['hospital_n_key'])
    if request.POST['edu_n_key'] =='':
      if request.POST['hospital_n_key'] != '' and request.POST['hospital_n_key'] != None:
        created_on = TimeZoneConvert(request.POST['hospital_n_key'])
      else:
        created_on = DefaultTimeZone()
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        http_address =  'http://'
        if myfile!=None:           
          aa=http_address + request.get_host() + uploaded_file_url
        else:
          aa=''              
        user_info = models.Empeducationaldetails.objects.create(document_attachment=aa,qualification_title=request.POST['qualification_title'],employee_n_key=request.POST['employee_n_key'],school=request.POST['school'],
        start_year=request.POST['start_year'],end_year=request.POST['end_year'],controlling_university=request.POST['controlling_university'],description=request.POST['description'],
        created_by_id=request.POST['created_by_id'],created_by_name=request.POST['created_by_name'],created_on=created_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      else:
        http_address = 'https://'
        if myfile!=None:
          bb=http_address + request.get_host() + "/api" + uploaded_file_url
        else:
          bb=''
        user_info = models.Empeducationaldetails.objects.create(document_attachment= bb,qualification_title=request.POST['qualification_title'],employee_n_key=request.POST['employee_n_key'],school=request.POST['school'],
        start_year=request.POST['start_year'],end_year=request.POST['end_year'],controlling_university=request.POST['controlling_university'],description=request.POST['description'],
        created_by_id=request.POST['created_by_id'],created_by_name=request.POST['created_by_name'],created_on=created_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      user_info1 = models.Empeducationaldetails.objects.all().order_by('-emp_edu_id')[:1]
    if request.POST['edu_n_key'] !='':
      if request.POST['hospital_n_key'] != '' and request.POST['hospital_n_key'] != None:
        modified_on = TimeZoneConvert(request.POST['hospital_n_key'])
      else:
        modified_on= DefaultTimeZone()
      dd = ''
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        if myfile!=None:
          dd='http://' + request.get_host() + uploaded_file_url
      else:
        if myfile!=None:
          dd='https://' + request.get_host() + "/api" + uploaded_file_url
      if myfile!=None:
        user_info = models.Empeducationaldetails.objects.filter(edu_n_key = request.POST['edu_n_key']).update(document_attachment= dd)
      user_info = models.Empeducationaldetails.objects.filter(edu_n_key = request.POST['edu_n_key']).update(qualification_title=request.POST['qualification_title'],employee_n_key=request.POST['employee_n_key'],school=request.POST['school'],
          start_year=request.POST['start_year'],end_year=request.POST['end_year'],controlling_university=request.POST['controlling_university'],description=request.POST['description'],
          modified_by_id=request.POST['created_by_id'],modified_by_name=request.POST['created_by_name'],modified_on=modified_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      user_info1 = models.Empeducationaldetails.objects.filter(edu_n_key = request.POST['edu_n_key'])
    a = ''
    for i in user_info1:
      a=i.document_attachment
      modified_on=i.modified_on
      created_on=i.created_on
      if modified_on != None and modified_on != '':
        modified_on=str(modified_on.strftime("%d/%m/%Y"))
      if created_on != None and created_on != '':
        created_on=str(created_on.strftime("%d/%m/%Y"))
    serializer_class = serializer1.EmpeducationaldetailsSerializer(user_info1, many=True).data
    for j in serializer_class:
      j['document_attachment']=str(a)
      j['modified_on']=modified_on
      j['created_on']=created_on
    return HttpResponse(json.dumps({"data":serializer_class,"status":"success"}), content_type="application/json")
  return HttpResponse("")

@csrf_exempt
@api_view(["POST"])
def Emp_professional(request):
  if request.method == 'POST':
    myfile = request.FILES.get('document_attachment')
    if myfile!=None:
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
    hospital = models.HospitalMaster.objects.filter(hospital_n_key=request.POST['hospital_n_key'])
    if request.POST['pro_n_key'] =='':
      if request.POST['hospital_n_key'] != '' and request.POST['hospital_n_key'] != None:
        created_on = TimeZoneConvert(request.POST['hospital_n_key'])
      else:
        created_on= DefaultTimeZone()
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        http_address =  'http://'
        if myfile!=None:           
          aa=http_address + request.get_host() + uploaded_file_url
        else:
          aa=''
        user_info = models.EmployeeProfessional.objects.create(document_attachment=aa,employee_n_key=request.POST['employee_n_key'],organisation=request.POST['organisation'],
        start_date=request.POST['start_date'],end_date=request.POST['end_date'],description=request.POST['description'],
        created_by_id=request.POST['created_by_id'],created_by_name=request.POST['created_by_name'],created_on=created_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      else:
        http_address = 'https://'
        if myfile!=None:           
          bb=http_address + request.get_host() + uploaded_file_url
        else:
          bb=''
        user_info = models.EmployeeProfessional.objects.create(document_attachment=bb,employee_n_key=request.POST['employee_n_key'],organisation=request.POST['organisation'],
        start_date=request.POST['start_date'],end_date=request.POST['end_date'],description=request.POST['description'],
        created_by_id=request.POST['created_by_id'],created_by_name=request.POST['created_by_name'],created_on=created_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      user_info1 = models.EmployeeProfessional.objects.all().order_by('-emp_pro_id')[:1]
    if request.POST['pro_n_key'] !='':
      if request.POST['hospital_n_key'] != '' and request.POST['hospital_n_key'] != None:
        modified_on = TimeZoneConvert(request.POST['hospital_n_key'])
      else:
        modified_on= DefaultTimeZone()
      dd = ''
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        if myfile!=None:
          dd='http://' + request.get_host() + uploaded_file_url
      else:
        if myfile!=None:
          dd='https://' + request.get_host() + "/api" + uploaded_file_url
      if myfile!=None:
        user_info = models.EmployeeProfessional.objects.filter(pro_n_key = request.POST['pro_n_key']).update(document_attachment= dd)
      user_info = models.EmployeeProfessional.objects.filter(pro_n_key = request.POST['pro_n_key']).update(employee_n_key=request.POST['employee_n_key'],organisation=request.POST['organisation'],
      start_date=request.POST['start_date'],end_date=request.POST['end_date'],description=request.POST['description'],
      modified_by_id=request.POST['created_by_id'],modified_by_name=request.POST['created_by_name'],modified_on=modified_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      user_info1 = models.EmployeeProfessional.objects.filter(pro_n_key = request.POST['pro_n_key'])
    a = ''
    for i in user_info1:
      a=i.document_attachment
      modified_on=i.modified_on
      created_on=i.created_on
      start_date=i.start_date
      end_date=i.end_date
      if modified_on != None and modified_on != '':
        modified_on=str(modified_on.strftime("%d/%m/%Y"))
      if created_on != None and created_on != '':
        created_on=str(created_on.strftime("%d/%m/%Y"))
      if start_date != None and start_date != '':
        start_date = str(start_date.strftime("%d/%m/%Y"))
      if end_date != None and end_date != '':
        end_date = str(end_date.strftime("%d/%m/%Y"))
    serializer_class = serializer1.EmployeeProfessionalSerializer(user_info1, many=True).data      
    for j in serializer_class:
      j['document_attachment']=str(a)
      j['modified_on']=modified_on
      j['created_on']=created_on
      j['start_date']=start_date
      j['end_date']=end_date  
    return HttpResponse(json.dumps({"data":serializer_class,"status":"success"}), content_type="application/json")
  return HttpResponse("")





@csrf_exempt
@api_view(["POST"])
def Emp_training(request):
  if request.method == 'POST':
    myfile = request.FILES.get('document_attachment')
    if myfile!=None:
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
    hospital = models.HospitalMaster.objects.filter(hospital_n_key=request.POST['hospital_n_key'])
    if request.POST['training_n_key'] =='':
      if request.POST['hospital_n_key'] != '' and request.POST['hospital_n_key'] != None:
        created_on = TimeZoneConvert(request.POST['hospital_n_key'])
      else:
        created_on= DefaultTimeZone()
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        http_address =  'http://'
        if myfile!=None:           
          aa=http_address + request.get_host() + uploaded_file_url
        else:
          aa=''
        user_info = models.EmployeeTraining.objects.create(document_attachment=aa,employee_n_key=request.POST['employee_n_key'],courses=request.POST['courses'],
        date=request.POST['date'],description=request.POST['description'],
        created_by_id=request.POST['created_by_id'],created_by_name=request.POST['created_by_name'],created_on=created_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      else:
        http_address = 'https://'
        if myfile!=None:           
          bb=http_address + request.get_host() + uploaded_file_url
        else:
          bb=''
        user_info = models.EmployeeTraining.objects.create(document_attachment=bb,employee_n_key=request.POST['employee_n_key'],courses=request.POST['courses'],
        date=request.POST['date'],description=request.POST['description'],
        created_by_id=request.POST['created_by_id'],created_by_name=request.POST['created_by_name'],created_on=created_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      user_info1 = models.EmployeeTraining.objects.all().order_by('-emp_training_id')[:1]
    if request.POST['training_n_key'] !='':
      if request.POST['hospital_n_key'] != '' and request.POST['hospital_n_key'] != None:
        modified_on = TimeZoneConvert(request.POST['hospital_n_key'])
      else:
        modified_on= DefaultTimeZone()
      dd = ''
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        if myfile!=None:
          dd='http://' + request.get_host() + uploaded_file_url
      else:
        if myfile!=None:
          dd='https://' + request.get_host() + "/api" + uploaded_file_url
      if myfile!=None:
        user_info = models.EmployeeTraining.objects.filter(training_n_key = request.POST['training_n_key']).update(document_attachment= dd)
      user_info = models.EmployeeTraining.objects.filter(training_n_key = request.POST['training_n_key']).update(employee_n_key=request.POST['employee_n_key'],courses=request.POST['courses'],
        date=request.POST['date'],description=request.POST['description'],
        modified_by_id=request.POST['created_by_id'],modified_by_name=request.POST['created_by_name'],modified_on=modified_on,hospital_n_key=request.POST['hospital_n_key'],org_n_key=request.POST['org_n_key'])
      user_info1 = models.EmployeeTraining.objects.filter(training_n_key = request.POST['training_n_key'])
    a = ''
    for i in user_info1:
      a=i.document_attachment
      date=i.date
      modified_on=i.modified_on
      created_on=i.created_on
      if date != None and date != '':
        date=str(date.strftime("%d/%m/%Y"))
      if modified_on != None and modified_on != '':
        modified_on=str(modified_on.strftime("%d/%m/%Y"))
      if created_on != None and created_on != '':
        created_on=str(created_on.strftime("%d/%m/%Y"))    
    serializer_class = serializer1.EmployeeTrainingSerializer(user_info1, many=True).data
    for j in serializer_class:
      j['document_attachment']=str(a)
      j['date']=date
      j['modified_on']=modified_on
      j['created_on']=created_on
    return HttpResponse(json.dumps({"data":serializer_class,"status":"success"}), content_type="application/json")
  return HttpResponse("")

@csrf_exempt
@api_view(["POST"])
def Emp_experience(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital = models.HospitalMaster.objects.filter(hospital_n_key=request['hospital_n_key'])
  if request['exp_n_key'] =='':
    if request['hospital_n_key'] != '' and request['hospital_n_key'] != None:
      created_on = TimeZoneConvert(request['hospital_n_key'])
    else:
      created_on= DefaultTimeZone()
    user_info = models.EmployeeExperience.objects.create(employee_n_key=request['employee_n_key'],title=request['title'],currently_working=request['currently_working'],
    start_date=request['start_date'],end_date=request['end_date'],description=request['description'],employment_type=request['employment_type'],location=request['location'],hos_name=request['hos_name'],
    created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=created_on,hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'])
    user_info1 = models.EmployeeExperience.objects.all().order_by('-emp_exp_id')[:1]
  if request['exp_n_key'] !='':
    if request['hospital_n_key'] != '' and request['hospital_n_key'] != None:
      modified_on = TimeZoneConvert(request['hospital_n_key'])
    else:
      modified_on= DefaultTimeZone()
    user_info = models.EmployeeExperience.objects.filter(exp_n_key = request['exp_n_key']).update(employee_n_key=request['employee_n_key'],title=request['title'],currently_working=request['currently_working'],
    start_date=request['start_date'],end_date=request['end_date'],description=request['description'],employment_type=request['employment_type'],location=request['location'],hos_name=request['hos_name'],
    modified_by_id=request['created_by_id'],modified_by_name=request['created_by_name'],modified_on=modified_on,hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'])
    user_info1 = models.EmployeeExperience.objects.filter(exp_n_key = request['exp_n_key'])
  serializer_class = serializer1.EmployeeExperienceSerializer(user_info1, many=True)
  created_on = str(user_info1[0].created_on.strftime("%d/%m/%Y"))
  serializer_class.data[0]['created_on'] = created_on
  if user_info1[0].modified_on !=None:
    modified_on=str(user_info1[0].modified_on.strftime("%d/%m/%Y"))
    serializer_class.data[0]['modified_on'] = modified_on
  if user_info1[0].start_date != None and user_info1[0].start_date != '':
    start_date = str(user_info1[0].start_date.strftime("%d/%m/%Y"))
    serializer_class.data[0]['start_date'] = start_date
  if user_info1[0].end_date != None and user_info1[0].end_date != 'Present' and user_info1[0].end_date !='':
    abcd=datetime.datetime.strptime(user_info1[0].end_date, "%Y-%m-%d").date()
    end_date=str(abcd.strftime("%d/%m/%Y"))
    serializer_class.data[0]['end_date'] = end_date
  return HttpResponse(json.dumps({"data":serializer_class.data,"status":"success"}), content_type="application/json")



@csrf_exempt
@api_view(["POST"])
def Emp_teach_exp(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital = models.HospitalMaster.objects.filter(hospital_n_key=request['hospital_n_key'])
  if request['exp_teach_n_key'] =='':
    if request['hospital_n_key'] != '' and request['hospital_n_key'] != None:
      created_on = TimeZoneConvert(request['hospital_n_key'])
    else:
      created_on= DefaultTimeZone()
    user_info = models.EmployeeTeachExperience.objects.create(employee_n_key=request['employee_n_key'],institution=request['institution'],
    start_date=request['start_date'],end_date=request['end_date'],description=request['description'],position=request['position'],
    created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=created_on,hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'])
    user_info1 = models.EmployeeTeachExperience.objects.all().order_by('-exp_teach_id')[:1]
  if request['exp_teach_n_key'] !='':
    if request['hospital_n_key'] != '' and request['hospital_n_key'] != None:
      modified_on = TimeZoneConvert(request['hospital_n_key'])
    else:
      modified_on= DefaultTimeZone()
    user_info = models.EmployeeTeachExperience.objects.filter(exp_teach_n_key = request['exp_teach_n_key']).update(employee_n_key=request['employee_n_key'],institution=request['institution'],
    start_date=request['start_date'],end_date=request['end_date'],description=request['description'],position=request['position'],
    modified_by_id=request['created_by_id'],modified_by_name=request['created_by_name'],modified_on=modified_on,hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'])
    user_info1 = models.EmployeeTeachExperience.objects.filter(exp_teach_n_key = request['exp_teach_n_key'])
  serializer_class = serializer1.EmployeeTeachExperienceSerializer(user_info1, many=True)
  created_on = str(user_info1[0].created_on.strftime("%d/%m/%Y"))
  serializer_class.data[0]['created_on'] = created_on
  if user_info1[0].modified_on !=None:
    modified_on=str(user_info1[0].modified_on.strftime("%d/%m/%Y"))
    serializer_class.data[0]['modified_on'] = modified_on
  if user_info1[0].start_date != None and user_info1[0].start_date != '':
    start_date = str(user_info1[0].start_date.strftime("%d/%m/%Y"))
    serializer_class.data[0]['start_date'] = start_date
  if user_info1[0].end_date != None and user_info1[0].end_date != '':
    end_date = str(user_info1[0].end_date.strftime("%d/%m/%Y"))
    serializer_class.data[0]['end_date'] = end_date  
  return HttpResponse(json.dumps({"data":serializer_class.data,"status":"success"}), content_type="application/json")



@csrf_exempt
@api_view(["POST"])
def Emp_restriction(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital = models.HospitalMaster.objects.filter(hospital_n_key=request['hospital_n_key'])
  if request['practice_n_key'] =='':
    if request['hospital_n_key'] != '' and request['hospital_n_key'] != None:
      created_on = TimeZoneConvert(request['hospital_n_key'])
    else:
      created_on= DefaultTimeZone()
    user_info = models.EmployeeRestriction.objects.create(employee_n_key=request['employee_n_key'],restriction_if_any=request['restriction_if_any'],
    inv_practice=request['inv_practice'],res_comments=request['res_comments'],inv_comments=request['inv_comments'],
    created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=created_on,hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'])
    user_info1 = models.EmployeeRestriction.objects.all().order_by('-emp_practice_id')[:1]
  if request['practice_n_key'] !='':
    if request['hospital_n_key'] != '' and request['hospital_n_key'] != None:
      modified_on = TimeZoneConvert(request['hospital_n_key'])
    else:
      modified_on= DefaultTimeZone()
    user_info = models.EmployeeRestriction.objects.filter(practice_n_key = request['practice_n_key']).update(employee_n_key=request['employee_n_key'],restriction_if_any=request['restriction_if_any'],
    inv_practice=request['inv_practice'],res_comments=request['res_comments'],inv_comments=request['inv_comments'],
    modified_by_id=request['created_by_id'],modified_by_name=request['created_by_name'],modified_on=modified_on,hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'])
    user_info1 = models.EmployeeRestriction.objects.filter(practice_n_key = request['practice_n_key'])
  serializer_class = serializer1.EmployeeRestrictionSerializer(user_info1, many=True)
  created_on = str(user_info1[0].created_on.strftime("%d/%m/%Y"))
  serializer_class.data[0]['created_on'] = created_on
  if user_info1[0].modified_on !=None:
    modified_on=str(user_info1[0].modified_on.strftime("%d/%m/%Y"))
    serializer_class.data[0]['modified_on'] = modified_on
  return HttpResponse(json.dumps({"data":serializer_class.data,"status":"success"}), content_type="application/json")
@csrf_exempt
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
@csrf_exempt
def Allform_details(request):
  request = json.loads(request.body.decode('utf-8'))
  database = connection.settings_dict['NAME']
  fulldata = []
  org_n_key = request['org_n_key']
  employee_n_key = request['employee_n_key']
  cursor = connection.cursor()
  def getData(tableName):
    cursor.execute('''SELECT * FROM '''+str(database)+'''.'''+str(tableName)+'''
        WHERE org_n_key="'''+str(org_n_key)+'''"  AND employee_n_key="'''+str(employee_n_key)+'''"  ''')
    check_in = dictfetchall(cursor)
    return check_in;
  table_name=['ge_emp_education_details','ge_emp_professional','ge_emp_training','ge_emp_experience','ge_emp_exp_teaching','ge_emp_practice_restriction','md_employees_master']
  for j in table_name:
    data = getData(j)
    for i in data:
      if 'date_of_birth' in i:
        if i['date_of_birth'] !=None:
          i['date_of_birth'] = i['date_ofbirth'] =str(i['date_of_birth'].strftime("%d/%m/%Y"))
      i['created_on']=str(i['created_on'].strftime("%d/%m/%Y"))
      if i['modified_on'] !=None:
        i['modified_on']=str(i['modified_on'].strftime("%d/%m/%Y"))
      if 'start_date' in i and  i['start_date']!= None and i['start_date']!= '':
        i['start_date']=str(i['start_date'].strftime("%d/%m/%Y"))
      if 'end_date' in i and  i['end_date']!= None and i['end_date'] != 'Present' and i['end_date'] !='' and j != 'ge_emp_experience':
        i['end_date']=str(i['end_date'].strftime("%d/%m/%Y"))
      elif 'end_date' in i and  i['end_date']!= None and i['end_date'] != 'Present' and i['end_date'] !='':
        abcd=datetime.datetime.strptime(i['end_date'], "%Y-%m-%d").date()
        i['end_date']=str(abcd.strftime("%d/%m/%Y")) 
      if 'date' in i and  i['date']!= None and i['date']!= '':
        i['date']=str(i['date'].strftime("%d/%m/%Y"))
      if 'phone_number' in i and  i['phone_number']!= None:
        i['phone_number']=str(i['phone_number'])
      if 'emergency_contact_no' in i and  i['emergency_contact_no']!= None and i['emergency_contact_no']!= '':
        i['emergency_contact_no']=str(i['emergency_contact_no'])
      elif 'emergency_contact_no' in i and  i['emergency_contact_no']== None:
        i['emergency_contact_no']=None
    fulldata.append(data)
  emp_details = fulldata[6]
  for i in emp_details:
    if i['speciality'] != None:
      i['speciality'] = ",".join(json.loads(i['speciality']))
  emp_work = []
  emp = models.EmployeesMaster.objects.filter(Q(employee_n_key=employee_n_key))
  doc_role = DoctorRoleQuery(org_n_key)
  if (emp[0].role in doc_role) or (emp[0].role == 'Physician'):
    emp_work = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=employee_n_key))
  return HttpResponse(json.dumps({"Education_details":fulldata[0],"Professional_details":fulldata[1],"Teaching_details":fulldata[2],"Experience_details":fulldata[3],
    "EmployeeTeachExperience_details":fulldata[4],"EmployeeRestriction":fulldata[5],"Employee_details":emp_details,"working_days":False if emp_work else True}), content_type="application/json")
@csrf_exempt
# @api_view(["POST"])
def Emp_profile_update(request):
  request  = json.loads(request.body.decode('utf-8'))
  fulldata=[]
  employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=request['employee_n_key']))
  if employee:
    if 'date_ofbirth' in request:
      request['date_of_birth'] = request['date_ofbirth']
    if request['hospital_n_key'] != '' and request['hospital_n_key'] != None:
      request['modified_on']=TimeZoneConvert(request['hospital_n_key'])
    else:
      request['modified_on']=DefaultTimeZone()
    serializer = serializer1.EmployeesMasterSerializer(employee[0], data=request, partial=True)
    if serializer.is_valid():
      serializer.save()
      fulldata.append({'list': serializer.data,'status': "Updated Successfully"})
  return HttpResponse(json.dumps(fulldata),content_type="application/json")
@csrf_exempt
@api_view(["POST"])
def Emp_edit_details(request):
  request = json.loads(request.body.decode('utf-8'))
  fulldata=[]
  employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=request['n_key']))
  if employee:
    emp_data = serializer1.EmployeesMasterSerializer(employee, many=True).data
    emp_data = emp_data[0]
    del emp_data['password'],emp_data['user_name']
    emp_image = models.Employeedocuments.objects.filter(doctor_n_key = request['n_key'])
    emp_data['date_ofbirth'] = emp_data['date_of_birth']
    del emp_data['date_of_birth']
    emp_data['image'] = None
    if emp_image:
      emp_data['image'] = str(emp_image[0].emp_attachment)
    return HttpResponse(json.dumps([emp_data]),content_type="application/json")
  else:
    return HttpResponse(json.dumps([]),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Empdocument(request):
  if request.method == 'POST' and request.FILES['emp_attachment']:
    myfile = request.FILES['emp_attachment']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    find = models.Employeedocuments.objects.filter(doctor_n_key = request.POST['doctor_n_key'])
    http_address = ''
    if find:
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        http_address = 'http://'
        a=models.Employeedocuments.objects.filter(doctor_n_key = request.POST['doctor_n_key']).update(emp_attachment=http_address + request.get_host() + uploaded_file_url)
        imaa=models.Employeedocuments.objects.filter(doctor_n_key = request.POST['doctor_n_key'])
        b = ''
        for i in imaa:
          b = i.emp_attachment
        image_serializer = serializer1.EmployeedocumentsSerializer(imaa, many=True)
        return HttpResponse(json.dumps({"status":"uploaded successfully","image":str(b)}),content_type="application/json")
      else:
        http_address = 'https://'
        a=models.Employeedocuments.objects.filter(doctor_n_key = request.POST['doctor_n_key']).update(emp_attachment=http_address + request.get_host() + "/api"+ uploaded_file_url)
        imaa=models.Employeedocuments.objects.filter(doctor_n_key = request.POST['doctor_n_key'])
        b = ''
        for i in imaa:
          b = i.emp_attachment
        image_serializer = serializer1.EmployeedocumentsSerializer(imaa, many=True)
        return HttpResponse(json.dumps({"status":"uploaded successfully","image":str(b)}),content_type="application/json")
    else:
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001' :
        http_address = 'http://'
        donor_image = models.Employeedocuments.objects.create(emp_attachment= http_address + request.get_host() + uploaded_file_url,doctor_n_key = request.POST['doctor_n_key'])
        imaa=models.Employeedocuments.objects.filter(doctor_n_key = request.POST['doctor_n_key'])
        b = ''
        for i in imaa:
          b = i.emp_attachment
        image_serializer = serializer1.EmployeedocumentsSerializer(imaa, many=True)
        return HttpResponse(json.dumps({"status":"uploaded successfully","image":str(b)}),content_type="application/json")
      else:
        http_address = 'https://'
        donor_image = models.Employeedocuments.objects.create(emp_attachment= http_address + request.get_host() + "/api" + uploaded_file_url,doctor_n_key = request.POST['doctor_n_key'])
        imaa=models.Employeedocuments.objects.filter(doctor_n_key = request.POST['doctor_n_key'])
        b = ''
        for i in imaa:
          b = i.emp_attachment
        image_serializer = serializer1.EmployeedocumentsSerializer(imaa, many=True)
        return HttpResponse(json.dumps({"status":"uploaded successfully","image":str(b)}),content_type="application/json")
  return HttpResponse("")

def AccessRole(request):
    fulldata=[]
    request['emp_n_key']=request['employee_n_key']
    request['role_name']=request['role']
    access=models.MdAccess.objects.all()
    if 'product_name' in request:
      for i in request['product_name']:
        request['product_name'] = i
        fits = access.filter(Q(emp_n_key=request['employee_n_key'])&Q(product_name=i)).values_list('access_id',flat=True)
        if fits:
          fits1=access.get(access_id=fits[0])
          request['modified_on']=TimeZoneConvert(request['hospital_n_key'])
          serializer = serializer1.MdAccessSerializer(instance=fits1,data=request, partial=True)
          if serializer.is_valid():
            serializer.save()
            # print("access updated")
            fulldata.append({'list': serializer.data,'status': "Updated Successfully"})
          else:
            print(serializer.errors)
        else:
          request['created_on']=TimeZoneConvert(request['hospital_n_key'])
          serializer = serializer1.MdAccessSerializer(data=request)
          if serializer.is_valid():
            serializer.save()
            fulldata.append({'list': serializer.data,
                               'status': "Created Successfully"})
          else:
            print(serializer.errors)
    return fulldata

@csrf_exempt
@api_view(["POST"])
def Hospitallist(request):
    request = json.loads(request.body.decode('utf-8'))
    if request:
        employee = models.HospitalMaster.objects.filter(org_n_key = request['org_n_key'])
        serialize_class = serializer1.HospitalSerializer(employee, many=True)
        return HttpResponse(json.dumps({"hospital":serialize_class.data}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status":"no request"}), content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Clinic_Details(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital_n_key=request['hospital_n_key']
  if request:
      employee = models.HospitalMaster.objects.filter(hospital_n_key = request['hospital_n_key'])
      clinical = models.ClinicalMaster.objects.filter(hospital_n_key = hospital_n_key)
      serialize_class = serializer1.HospitalSerializer(employee, many=True)
      serialize_class1 = serializer1.ClinicalMasterSerializer(clinical, many=True)
      return HttpResponse(json.dumps({"hospital":serialize_class.data,"clinical":serialize_class1.data}), content_type="application/json")
  else:
      return HttpResponse(json.dumps({"status":"no request"}), content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Role_checkdetails(request):
  request = json.loads(request.body.decode('utf-8'))
  list1=models.GERoles.objects.filter(Q(roles_name = request['roles_name']) & Q(hospital_n_key=request['hospital_n_key']))
  if list1:
    return HttpResponse(json.dumps({"role_check": [list1[0].role_check]}),content_type="application/json")
  return HttpResponse(json.dumps({"role_check": 'No'}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Employee_working_edit(request):
  request = json.loads(request.body.decode('utf-8'))
  doctor_data = []
  doc_work_data = []
  doc_spec_data = []
  work_filter = []
  employee_data=[]
  calendar = models.CalendarSettings.objects.filter(Q(employee_n_key=request['doctor_n_key']))
  if calendar:
    calendar_data = serializer1.CalendarSettingsSerializer(calendar, many=True).data
    doctor_data.append(calendar_data)
  working = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=request['doctor_n_key']))
  emp_master = models.EmployeesMaster.objects.filter(Q(employee_n_key=request['doctor_n_key']))
  if not working:
    
    if emp_master:
      work_filter.append(emp_master[0].clinical_n_key)
  for i in working:
    if i.clinical_n_key not in work_filter:
      work_filter.append(i.clinical_n_key)
  for j in work_filter:
    temp_work = []
    temp_spec = []
    non_working = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    working_days = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=request['doctor_n_key']) & Q(clinical_n_key=j))
    if working_days:
      for l in working_days:
        if l.working_days in non_working:
          non_working.remove(l.working_days)
      for k in working_days:
        temp_work.append({'working_days':k.working_days,'start_time':str(k.start_time),'end_time':str(k.end_time)})
    for m in non_working:
      temp_work.append({'working_days':m,'start_time':None,'end_time':None})
    spec_days = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=request['doctor_n_key']) & Q(clinical_n_key=j))
    if spec_days:
      for n in spec_days:
        spec_days_data = serializer1.DoctorSpecialHoursSerializer(n).data
        if spec_days_data['available']=='Closed':
          spec_days_data['start_time']=''
          spec_days_data['end_time']=''
        temp_spec.append(spec_days_data)
    hospital_n_key = emp_master[0].hospital_n_key
    clinical_n_key = emp_master[0].clinical_n_key
    if working_days:
      hospital_n_key = working_days[0].hospital_n_key
      clinical_n_key = working_days[0].clinical_n_key
    doc_work_data.append({'clinical_n_key':clinical_n_key,'hospital_n_key':hospital_n_key,'working_days':temp_work,'special_hours':temp_spec})
  return HttpResponse(json.dumps({'calendar':doctor_data,'doctor_working':doc_work_data}),content_type="application/json")


def Employee_working_update(request,employee):
  today = datetime.datetime.now().date()
  calendar = models.CalendarSettings.objects.get(cal_n_key=request['cal_n_key'])
  request['modified_on']=TimeZoneConvert(request['hospital_n_key'])
  cal_serializer = serializer1.CalendarSettingsSerializer(instance=calendar, data=request, partial=True)
  if cal_serializer.is_valid():
    cal_serializer.save()
    clinic = models.ClinicalMaster.objects.filter(Q(clinical_n_key=request['clinical_n_key']))
    workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
    if clinic[0].twenty_four_hours == 'No':
      for i in workingdetails['working_days']: 
        clinic_avail = models.ClinicalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(clinical_n_key=request['clinical_n_key']) & Q(working_days=i['day']) & Q(start_time__lte=i['start_time']) & Q(end_time__gte=i['start_time']) & Q(start_time__lte=i['end_time']) & Q(end_time__gte=i['end_time']))
        if not clinic_avail:
          return {'status':'failed','data':'Clinics working time not available'}
    roles = models.GERoles.objects.filter(Q(roles_name=employee[0].role))
    modified = models.EmployeesMaster.objects.filter(Q(employee_n_key=request['modified_by_id']))
    if (roles and roles[0].working_enable == 'Yes') or (modified and modified[0].role=='Master'):
      docwork = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=request['employee_n_key']))
      if docwork:
        docwork_del = docwork.delete()
      if len(workingdetails['working_days']) > 0: 
        for i in workingdetails['working_days']:
          # print("doctor working updated")
          doctor_work = models.DoctorWorkingDetails.objects.create(doctor_n_key=request['employee_n_key'],clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],
            end_time=i['end_time'],modified_by_id=request['modified_by_id'],modified_by_name=request['modified_by_name'],modified_on=request['modified_on'])

    docspec = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=request['employee_n_key'])& Q(special_date__gte=today))
    if docspec:
      docspec_del = docspec.delete()

    if len(workingdetails['special_hours']) > 0:
      for k in workingdetails['special_hours']:
        # print("doctor special updated")
        special_hours = models.DoctorSpecialHours.objects.create(doctor_n_key=request['employee_n_key'],clinical_n_key=request['clinical_n_key'],hospital_n_key=request['hospital_n_key'],org_n_key=request['org_n_key'],special_date=k['date'],available=k['available'],
          start_time=k['start_time'],end_time=k['end_time'],modified_by_id=request['modified_by_id'],modified_by_name=request['modified_by_name'],modified_on=request['modified_on'])
      return ('success')
    return ('')
  else:
    return (cal_serializer.errors)

@csrf_exempt
@api_view(["POST"])
def Employeedoc_get(request):
  request = json.loads(request.body.decode('utf-8'))
  emp_image = models.Employeedocuments.objects.filter(doctor_n_key = request['doctor_n_key'])
  a = ''
  for i in emp_image:
    a = i.emp_attachment
  image_serializer = serializer1.EmployeedocumentsSerializer(emp_image, many=True)
  return HttpResponse(json.dumps({"image":str(a)}),content_type="application/json")


def Employeelog_post(employee_n_key,token):
  employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=employee_n_key))
  if employee:
    log = models.EmployeeLogs.objects.filter(Q(employee_n_key=employee_n_key))
    if log:
      log.delete()
    emp_data = serializer1.EmployeesMasterSerializer(employee[0]).data
    emp_data['last_login'] = TimeZoneConvert(employee[0].hospital_n_key)
    emp_data['firebase_token'] = token
    login = serializer1.EmployeeLogsSerializer(data = emp_data)
    if login.is_valid():
      login.save()
      return (json.dumps({"status":"success","data":login.data}))
    return (json.dumps({"status":"failed","data":login.errors}))
  return (json.dumps({"status":"failed","data":"Employee not found"}))

# token check
@csrf_exempt
def EmployeesTokenCheck(request):
  request = json.loads(request.body.decode('utf-8'))
  master_emp = models.EmployeesMaster.objects.filter(Q(employee_n_key =request['employee_n_key'])) 
  if master_emp:
    emp_data = master_emp.values('employee_n_key','first_name','last_name','token','role','phone_number','hospital_n_key','org_n_key')
    for i in emp_data:
      i['phone_number'] = str(i['phone_number'])
      i['token'] = request['token']
    emp_id = master_emp[0].user_id
    user = User.objects.filter(Q(username=master_emp[0].user_name))
    token = Token.objects.filter(Q(user_id=user[0].id))
    # print(master_emp,user,token,user[0].id)
    if token and token[0].key == request['token']:
      return HttpResponse(json.dumps({"status":"success","url":request['url'],"data":emp_data[0]}),content_type="application/json")
    else:
      return HttpResponse(json.dumps({"status":"failed","url":'https://synapstics.com/login'}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"invalid key","url":'https://synapstics.com/login'}),content_type="application/json")


def employee_phone_validate(value,org_n_key,key):
  if key == "phone":
    employee = models.EmployeesMaster.objects.filter(Q(org_n_key=org_n_key)&Q(phone_number=value))
    if employee:
      return "failed"
    return "success"
  if key == "email":
    employee = models.EmployeesMaster.objects.filter(Q(org_n_key=org_n_key)&Q(email=value))
    if employee:
      return "failed"
    return "success"

# currency
class CurrencyDetailViewSet(viewsets.ModelViewSet):
  queryset = models.CurrencyDetails.objects.all()
  serializer_class = serializer1.CurrencyDetailsTableSerializer
  lookup_field = 'currency_details_n_key'

@csrf_exempt
# @api_view(["POST"])
def GetUniqueList(request):
  request = json.loads(request.body.decode('utf-8'))
  fulldata=[]
  fulldata1=[]
  unique_list=[]
  list1=list(models.GERoles.objects.filter(Q(org_n_key=request['org_n_key']) ).values('roles_name','created_by_id','created_by_name','created_on','role_check','working_enable','product_name'))
  employee_detail = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(role='Master'))
  employee_serializer = serializer1.EmployeesMasterSerializer(employee_detail, many=True)
  a = str(employee_detail[0].created_on.date())
  employee_serializer.data[0]['created_on'] = a
  for i in list1:
    i['created_on'] = str(i['created_on'].date())
    if i in unique_list:
      pass
    else:
      unique_list.append(i)
  finaldata = json.dumps(unique_list, default = myconverter)
  return HttpResponse(json.dumps({"Unique_list":json.loads(finaldata),'master':employee_serializer.data}),content_type="application/json")
def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()

def Product_icon(myfile,request):
  try:
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000':
      http_address =  'http://'
      image_url = http_address + request.get_host() + uploaded_file_url
      return image_url
    else:
      http_address = 'https://'
      image_url = http_address + request.get_host() + "/api" + uploaded_file_url
      return image_url
  except Exception as e:
    return None
@csrf_exempt
@api_view(["POST"])
def AppProductDetailsPost(request):
  data = json.loads(request.POST['data'])
  product_image = None
  product_long_des_image = None
  data['created_on']=TimeZoneConvert(data['hospital_n_key'])
  if request.method == 'POST':
    fs = FileSystemStorage()
    try:
      if request.FILES.get('product_image') != None:
        myfile = request.FILES['product_image']
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000':
          http_address =  'http://'
          product_image = http_address + request.get_host() + uploaded_file_url
        else:
          http_address = 'https://'
          product_image = http_address + request.get_host() + "/api" + uploaded_file_url
    except Exception as e:
      pass

    if request.FILES.get('program_icon_one') != None:
      one = request.FILES['program_icon_one']
      data['program_icon_one'] = Product_icon(one,request)
    if request.FILES.get('program_icon_two') != None:
      two = request.FILES['program_icon_two']
      data['program_icon_two'] = Product_icon(two,request)
    if request.FILES.get('program_icon_three') != None:
      three = request.FILES['program_icon_three']
      data['program_icon_three'] = Product_icon(three,request)
    if request.FILES.get('program_icon_four') != None:
      four = request.FILES['program_icon_four']
      data['program_icon_four'] = Product_icon(four,request)
    if request.FILES.get('program_icon_five') != None:
      five = request.FILES['program_icon_five']
      data['program_icon_five'] = Product_icon(five,request)
    if request.FILES.get('program_icon_six') != None:
      six = request.FILES['program_icon_six']
      data['program_icon_six'] = Product_icon(six,request)

    data['product_image'] = product_image
    data['faqs'] = json.dumps(data['faqs'])
    data['single_plan'] = json.dumps(data['single_pay'])
    if len(data['subscription_plan']) > 0:
      data['plan_a'] = json.dumps(data['subscription_plan']['planA'])
      data['plan_b'] = json.dumps(data['subscription_plan']['planB'])
      data['plan_c'] = json.dumps(data['subscription_plan']['planC'])
    serializer =serializer1.AppProductDetailsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")
    return HttpResponse(json.dumps({"status":"failed","data":serializer.errors}), content_type="application/json")
  return HttpResponse(json.dumps({"status":"failed","data":"Method Not Allowed"}), content_type="application/json")


@csrf_exempt
@api_view(["GET","PUT","DELETE"])
def AppProductDetails_update(request, app_prod_n_key):
  try:
    snippet =models.AppProductDetails.objects.get(app_prod_n_key=app_prod_n_key)
  except models.AppProductDetails.DoesNotExist:
    return HttpResponse(json.dumps({"data":"no data found"}),content_type="application/json")

  if request.method == 'GET':
    serializer =serializer1.AppProductDetailsSerializer(snippet)
    serializer_data=serializer.data
    serializer_data['faqs']=json.loads(serializer_data['faqs'])
    serializer_data['single_pay']=json.loads((serializer_data['single_plan']))
    serializer_data['subscription_plan']={}
    if serializer_data['payment_type']=='Subscription Pay':
      serializer_data['subscription_plan']['planA']=json.loads(serializer_data['plan_a'])
      serializer_data['subscription_plan']['planB']=json.loads(serializer_data['plan_b'])
      serializer_data['subscription_plan']['planC']=json.loads(serializer_data['plan_c'])
    del serializer_data['single_plan'],serializer_data['plan_a'],serializer_data['plan_b'],serializer_data['plan_c']
    return JsonResponse(serializer_data)

  elif request.method == 'PUT':
    data = json.loads(request.POST['data'])
    product_image = snippet.product_image
    product_long_des_image = None
    data['modified_on']=TimeZoneConvert(data['hospital_n_key'])
    
    try:
      if request.FILES.get('product_image') != None:
        myfile = request.FILES['product_image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000':
          http_address =  'http://'
          product_image = http_address + request.get_host() + uploaded_file_url
        else:
          http_address = 'https://'
          product_image = http_address + request.get_host() + "/api" + uploaded_file_url
    except Exception as e:
      pass

    if request.FILES.get('program_icon_one') != None:
      one = request.FILES['program_icon_one']
      data['program_icon_one'] = Product_icon(one,request)
    if request.FILES.get('program_icon_two') != None:
      two = request.FILES['program_icon_two']
      data['program_icon_two'] = Product_icon(two,request)
    if request.FILES.get('program_icon_three') != None:
      three = request.FILES['program_icon_three']
      data['program_icon_three'] = Product_icon(three,request)
    if request.FILES.get('program_icon_four') != None:
      four = request.FILES['program_icon_four']
      data['program_icon_four'] = Product_icon(four,request)
    if request.FILES.get('program_icon_five') != None:
      five = request.FILES['program_icon_five']
      data['program_icon_five'] = Product_icon(five,request)
    if request.FILES.get('program_icon_six') != None:
      six = request.FILES['program_icon_six']
      data['program_icon_six'] = Product_icon(six,request)
    data['product_image'] = product_image
    data['faqs'] = json.dumps(data['faqs'])
    data['single_plan'] = json.dumps(data['single_pay'])
    if len(data['subscription_plan']) > 0:
      data['plan_a'] = json.dumps(data['subscription_plan']['planA'])
      data['plan_b'] = json.dumps(data['subscription_plan']['planB'])
      data['plan_c'] = json.dumps(data['subscription_plan']['planC'])
    else:
      data['subscription_plan']={}
    serializer =serializer1.AppProductDetailsSerializer(snippet, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return HttpResponse(json.dumps({"status":"success","data":{}}), content_type="application/json")
    return HttpResponse(json.dumps({"status":"failed","data":serializer.errors}), content_type="application/json")
    
  elif request.method == 'DELETE':
    snippet.delete()
    return HttpResponse(json.dumps({"data":"data deleted successfully"}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({"data":"Method Not Allowed"}),content_type="application/json")

@csrf_exempt
def List_Products_App(request):
  request = json.loads(request.body.decode('utf-8'))
  alldata = []
  product = models.AppProductDetails.objects.filter(Q(org_n_key=request['org_n_key']))
  if product:
    product_data = serializer1.AppProductDetailsSerializer(product, many=True).data
    for i in product_data:
      loop_data = {}
      loop_data['app_prod_n_key'] = i['app_prod_n_key']
      loop_data['product_title'] = i['product_title']
      loop_data['product_short_discription'] = i['product_short_discription']
      loop_data['created_by_name'] = i['created_by_name']
      loop_data['created_on'] = datetime.datetime.strptime(i['created_on'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y')
      alldata.append(loop_data)
  return HttpResponse(json.dumps({'status':'success','data':alldata}), content_type="application/json")

@csrf_exempt
def Product_Details_Get(request):
  alldata = []
  request = json.loads(request.body.decode('utf-8'))
  product = list(models.ProductGroupDetails.objects.filter(Q(org_n_key=request['org_n_key'])).values('app_prod_grp_key','title'))
  for i in product:
    i['app_prod_n_key']=i['app_prod_grp_key']
    i['product_title']=i['title']
  return HttpResponse(json.dumps({'status':'success','data':product}), content_type="application/json")
  
  # product = list(models.AppProductDetails.objects.filter(Q(org_n_key=request['org_n_key'])).values('app_prod_n_key','product_title','payment_type','single_plan','plan_a','plan_b','plan_c'))
  # for i in product:
  #   single = [{'promo_code': '', 'amount': None, 'percentage': None, 'discount_amount':None,'disabled':'Yes',"plan":"Plan A"}]
  #   subsc = [{'promo_code': '', 'amount': None, 'percentage': None, 'discount_amount':None,'disabled':'Yes',"plan":"Plan A"},{'promo_code': '', 'amount': None, 'percentage': None, 'discount_amount':None,'disabled':'Yes',"plan":"Plan B"},{'promo_code': '', 'amount': None, 'percentage': None, 'discount_amount':None,'disabled':'Yes',"plan":"Plan C"}]
  #   if i['payment_type']== 'Single Pay':
  #     i['single_plan'] = json.loads(i['single_plan'])
  #     single[0]['amount'] = i['single_plan']['amount']
  #     i['plan'] = single
  #   elif i['payment_type']== 'Subscription Pay':
  #     i['plan_a'],i['plan_b'],i['plan_c'] = json.loads(i['plan_a']),json.loads(i['plan_b']),json.loads(i['plan_c'])
  #     subsc[0]['amount'],subsc[1]['amount'],subsc[2]['amount'] = i['plan_a']['amount'],i['plan_b']['amount'],i['plan_c']['amount']
  #     i['plan'] = subsc
  #   del i['single_plan'],i['plan_a'],i['plan_b'],i['plan_c']
  #   alldata.append(i)
  # return HttpResponse(json.dumps({'status':'success','data':product}), content_type="application/json")

@csrf_exempt
def DoctorCalendarSearch(request):
    payload = json.loads(request.body.decode('utf-8'))
    doctor = models.GeDoctorDetails.objects.filter(Q(hospital_n_key__icontains=payload['hospital_n_key']) & Q(org_n_key=payload['org_n_key']))
    alldata=[]
    if doctor:
        for i in doctor:
            employee = models.EmployeesMaster.objects.filter(Q(employee_n_key=i.employee_n_key.employee_n_key))
            if employee[0].is_active != 0 and employee[0].is_active != '0':
                alldata.append(i)
        doctordetails=serializer1.GeDoctorDetailsSerializer(alldata, many=True).data
        return HttpResponse(json.dumps(doctordetails),content_type='application/json')
    else:
        return HttpResponse(json.dumps([]),content_type='application/json')

@csrf_exempt
def AddEmployeeLimit(request):
    request = json.loads(request.body.decode('utf-8'))
    pricing = models.MdPaymentPricing.objects.filter(Q(org_n_key=request['org_n_key']) & Q(product_name='Mrecs')).order_by('-payment_pricing_id')
    if pricing:
      employee = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']))
      total = employee.count()
      plan = pricing[0].plan_name
      limit = 0
      if plan == 'Growing':
        limit = 5
        if total >= limit:
          return HttpResponse(json.dumps({'status':'failed','total':total,'limit':limit,'plan':pricing[0].plan_name}),content_type='application/json')
      if plan == 'Business':
        limit = 15
        if total >= limit:
          return HttpResponse(json.dumps({'status':'failed','total':total,'limit':limit,'plan':pricing[0].plan_name}),content_type='application/json')
      if plan == 'Enterprise':
        limit = 30
        if total >= limit:
          return HttpResponse(json.dumps({'status':'failed','total':total,'limit':limit,'plan':pricing[0].plan_name}),content_type='application/json')
    return HttpResponse(json.dumps({'status':'success','total':total,'limit':limit,'plan':pricing[0].plan_name}),content_type='application/json')

@csrf_exempt
def AccessCheck(request):
  request =json.loads(request.body.decode('utf-8'))
  if request['roles_name'] == 'Master':
    return HttpResponse(json.dumps({"status":"success"}),content_type="application/json")
  access = models.GERoles.objects.filter(Q(roles_name= request['roles_name'])  & Q(org_n_key=request['org_n_key']) & Q(urls =request['urls']))
  if access:
    return HttpResponse(json.dumps({"status":"success"}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"failed"}),content_type="application/json")

@csrf_exempt
def MedicalCollegeSearch(request):
  request =json.loads(request.body.decode('utf-8'))
  alldata = []
  college = models.MedicalCollege.objects.filter(Q(medical_school_name__istartswith=request['college_name']))
  if college:
    data = serializer1.MedicalCollegeSerializer(college, many=True).data
    [alldata.append(i['medical_school_name']) for i in data]
    return HttpResponse(json.dumps({"status":"success","data":alldata}),content_type="application/json")
  return HttpResponse(json.dumps({"status":"failed","data":[]}),content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def BloodBank_Master_Post(request):
  request = json.loads(request.body.decode('utf-8'))
  time_zone = request.get('time_zone')
  now_time = datetime.datetime.now(timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')
  bloodbank_create = models.BloodBank_Master.objects.create(org_n_key = request.get('org_n_key'),bloodbank_name=request.get('bloodbank_name'),
    bloodbank_phoneno=request.get('bloodbank_phoneno'),licence_no=request.get('licence_no'),bloodbank_address_line_one=request.get('bloodbank_address_line_one'),bloodbank_address_line_two=request.get('bloodbank_address_line_two'),online_practice_status='Disable',
    bloodbank_logo=request.get('bloodbank_logo'),state=request.get('state'),suburb=request.get('suburb'),country=request.get('country'),pincode=request.get('pincode'),emergency_no=request.get('emergency_no'),city=request.get('city'),gst_no=request.get('gst_no'),helpline=request.get('helpline'),
    bloodbank_fax_no=request.get('bloodbank_fax_no'),pri_email_id=request.get('pri_email_id'),sec_email_id=request.get('sec_email_id'),website=request.get('website'),establised_year=request.get('establised_year'),dial_code=request.get('dial_code'),url=request.get('url'),time_zone=request.get('time_zone'),
    twenty_four_hours=request.get('twenty_four_hours'),created_on=now_time,created_by_id=request.get('created_by_id'),created_by_name=request.get('created_by_name'),facebook_link=request.get('facebook_link'),instagram_link=request.get('instagram_link'),about_us=request.get('about_us'),facility=request.get('facility'),
    twitter_link=request.get('twitter_link'),linkedin_link=request.get('linkedin_link'),googlemap_link=request.get('googlemap_link'),banner_image=request.get('banner_image'),whatsapp_number=request.get('whatsapp_number'),whatsapp_dialcode=request.get('whatsapp_dialcode'))
  workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
  print(request['special_hours'])
  if request['twenty_four_hours'] != "Yes":
    if len(workingdetails['working_days']) > 0:
      for i in workingdetails['working_days']:
        if (i['start_time'] !='') and (i['start_time'] != None):
          hospital_working = models.BloodBankWorkingDetails.objects.create(bloodbank_n_key=bloodbank_create.bloodbank_n_key,org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],end_time=i['end_time'],
            created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
  if len(workingdetails['special_hours']) > 0:
    for j in workingdetails['special_hours']:
      special_hours = models.BloodBankSpecialHours.objects.create(bloodbank_n_key=bloodbank_create.bloodbank_n_key,org_n_key=request['org_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],
        end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
  bloodbank_check = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
  if len(bloodbank_check)==1:
    models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(role='Master')).update(bloodbank_n_key=bloodbank_create.bloodbank_n_key)
  bloodbank_data = serializer1.BloodBankMasterSerializer(bloodbank_check[0]).data
  bloodbank_last = serializer1.BloodBankMasterSerializer(bloodbank_check[len(bloodbank_check)-1]).data
  return HttpResponse(json.dumps({"status":"success","bloodbank_n_key":bloodbank_create.bloodbank_n_key}),content_type='application/json')
  # return HttpResponse(json.dumps({"status":"success","last_details":bloodbank_last,"details":bloodbank_data,"time_zone":request.get('time_zone')}),content_type='application/json')

# bloodbank workingdetails edit
@csrf_exempt
def BloodBank_WorkingDetails_Edit(request):
  request = json.loads(request.body.decode('utf-8'))
  bloodbank = models.BloodBank_Master.objects.filter(bloodbank_n_key=request['bloodbank_n_key'])
  today = datetime.datetime.now(timezone(bloodbank[0].time_zone)).date()
  bb_work_data = []
  bb_spec_data = []
  bloodbank_work = models.BloodBankWorkingDetails.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key'])).values('working_days','start_time','end_time')
  bloodbank_spec = models.BloodBankSpecialHours.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
  bloodbank_data = serializer1.BloodBankMasterSerializer(bloodbank, many=True).data
  bloodbank_data[0]['working_days'] = {}
  bloodbank_data[0]['special_hours'] = []
  if bloodbank[0].twenty_four_hours == 'Yes':
    return HttpResponse(json.dumps({"status":"success","bloodbank":bloodbank_data,"working_details":{},"special_hours":[],"check_days":[],"special_hours_closed":[]}),content_type="application/json")
  convert = ReArrangeWorking(bloodbank_work,bloodbank_spec)
  return HttpResponse(json.dumps({"bloodbank":bloodbank_data,"working_details":convert['working_days'],"special_hours":convert['special_hours'],"special_hours_closed":convert['special_hours_closed'],"check_days":convert['avail_date']}),content_type="application/json")



# bloodbank workingdetails update
@csrf_exempt
@api_view(["POST"])
def BloodBank_WorkingDetails_Update(request):
  request = json.loads(request.body.decode('utf-8'))
  bloodbank = models.BloodBank_Master.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']))
  if bloodbank:
    request['modified_on'] = DefaultTimeZone()
    # request['modified_on'] = TimeZoneConvert(request['bloodbank_n_key'])
    bb_create = serializer1.BloodBankMasterSerializer(instance=bloodbank[0], data=request, partial=True)
    if bb_create.is_valid():
      bb_create.save()
    else:
      return HttpResponse(json.dumps({"data":bb_create.errors}),content_type="application/json")
  work_filter = models.BloodBankWorkingDetails.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']) & Q(org_n_key=request['org_n_key']))
  if work_filter:
    work_filter_del = work_filter.delete()
  workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
  if request['twenty_four_hours'] != "Yes":
    if len(workingdetails['working_days']) > 0:      
      for i in workingdetails['working_days']:
        if (i['start_time'] !='') and (i['start_time'] != None):
          bloodbank_working = models.BloodBankWorkingDetails.objects.create(bloodbank_n_key=request['bloodbank_n_key'],org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],end_time=i['end_time'],
            created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
  spec_filter = models.BloodBankSpecialHours.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']) & Q(org_n_key=request['org_n_key']))
  if spec_filter:
    spec_filter_del = spec_filter.delete()
  if len(workingdetails['special_hours']) > 0:
    for j in workingdetails['special_hours']:  
      special_hours = models.BloodBankSpecialHours.objects.create(bloodbank_n_key=request['bloodbank_n_key'],org_n_key=request['org_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],
        end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
  return HttpResponse(json.dumps({"status":"success","bloodbank_n_key":request['bloodbank_n_key']}),content_type="application/json")

# bloodbank limit check
@csrf_exempt
def BloodBank_Limit_Check(request):
  data1 = json.loads(request.body.decode('utf-8'))
  planing = models.MdPaymentPricing.objects.filter(Q(org_n_key = data1['org_n_key'])&Q(product_name='DigiBlood')).values('current_plan','product_name')
  bloodbank = models.BloodBank_Master.objects.filter(Q(org_n_key=data1['org_n_key']))
  if planing:
    bbank = bloodbank.count()
    product = planing[0]['product_name']
    plan = planing[0]['current_plan']
    plandetail = models.PlanDetails.objects.filter(Q(product_name = product))
    plans = plandetail[0].plan_name.split(',')
    limit = plandetail[0].employees.split(',')
    plan_name = plans.index(plan)
    limitz = int(limit[plan_name])
    if bbank <= limitz:
      return HttpResponse(json.dumps({'status':'success','maximun_count':limitz,'total_bloodbank':bbank}),content_type='application/json')
    return HttpResponse(json.dumps({'status':'failed','maximun_count':limitz,'total_bloodbank':bbank}),content_type='application/json')


# bloodbank logo and banner image uploaded
@csrf_exempt
@api_view(["POST"])
def BloodBank_Logo_Update(request):
  find = models.BloodBank_Master.objects.filter(bloodbank_n_key=request.POST['bloodbank_n_key'])
  https_address = 'https://synapstics.com'
  http_address = 'http://'
  if find:
    if request.method == 'POST' and 'bloodbank_logo' in request.FILES and request.FILES['bloodbank_logo']:
      myfile = request.FILES['bloodbank_logo']
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
      http_address = ''
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001':        
        find.update(bloodbank_logo=http_address + request.get_host()+ uploaded_file_url)
      else:
        find.update(bloodbank_logo=https_address +"/api"+ uploaded_file_url)
    if request.method == 'POST' and 'banner_image' in request.FILES and request.FILES['banner_image']:
      myfile = request.FILES['banner_image']
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
      if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001':
        find.update(banner_image=http_address + request.get_host()+ uploaded_file_url)
      else:
        find.update(banner_image=https_address +"/api"+ uploaded_file_url)
    return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
  return HttpResponse(json.dumps({"status":"Failed"}),content_type="application/json")


# bloodbank logo and banner image get
@csrf_exempt
@api_view(["POST"])
def BloodBank_Logo_get(request):
  request = json.loads(request.body.decode('utf-8'))
  img = models.BloodBank_Master.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']))
  return HttpResponse(json.dumps({"logo":str(img[0].bloodbank_logo),"banner":str(img[0].banner_image)}),content_type="application/json")


#bloodbank get data organisation wise
@csrf_exempt
def OrganisationWise_GetData(request):
  data1 = json.loads(request.body.decode('utf-8'))
  organz = models.BloodBank_Master.objects.filter(Q(org_n_key=data1['org_n_key'])).values('bloodbank_n_key','bloodbank_address_line_one','bloodbank_name','bloodbank_phoneno','city','created_on','gst_no','licence_no','pincode','state','time_zone')
  for i in organz:
    i['bloodbank_phoneno'] = str(i['bloodbank_phoneno'])
    i['created_on'] = str(i['created_on'])
  return HttpResponse(json.dumps({"status":"success","data":list(organz)}),content_type="application/json")







@csrf_exempt
@api_view(["POST"])
def Hospital_Master_Post(request):
  request = json.loads(request.body.decode('utf-8'))
  data = []
  clinic = request['hospital_name']
  split_clinic = clinic.split(' ')
  short = ''
  if len(split_clinic) >= 3:
    for i in range(0,len(split_clinic)):
      if i <= 2:
        data.append(split_clinic[i][0])
    s = [str(i) for i in data]
    short = str("".join(s)).upper()
  if len(split_clinic) > 1 and len(split_clinic) <= 2:
    for i in range(0,len(split_clinic)):
      if i == 1:
        data.append(split_clinic[i][0])
      else:
        data.append(split_clinic[i][:2])
    s = [str(i) for i in data]
    short = str("".join(s)).upper()
  if len(split_clinic) == 1:
    s = [str(i) for i in split_clinic]
    short = str("".join(s)).upper()
    short = short[:3]
  time_zone = request.get('time_zone')
  now_time = datetime.datetime.now(timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')
  hos_create = models.HospitalMaster.objects.create(org_n_key=request.get('org_n_key'),hospital_name=request.get('hospital_name'),hospital_short=short,hospital_phoneno=request.get('hospital_phoneno'),
    employee_n_key=request.get('employee_n_key'),licence_no=request.get('licence_no'),hospital_logo=request.get('hospital_logo'),gst_no=request.get('gst_no'),hospital_address_line_one=request.get('hospital_address_line_one'),
    state=request.get('state'),city=request.get('city'),pincode=request.get('pincode'),hospital_address_line_two=request.get('hospital_address_line_two'),
    bloodbank=request.get('bloodbank'),g_ehr=request.get('g_ehr'),suburb=request.get('suburb'),country=request.get('country'),
    created_by_id=request.get('created_by_id'),created_by_name=request.get('created_by_name'),created_on=now_time,accreditation=request.get('accreditation'),provider_type=request.get('provider_type'),
    telephone_no=request.get('telephone_no'),emergency_no=request.get('emergency_no'),ambulance_no=request.get('ambulance_no'),foreign_patientcare=request.get('foreign_patientcare'),
    tollfree_no=request.get('tollfree_no'),helpline=request.get('helpline'),hospital_fax_no=request.get('hospital_fax_no'),pri_email_id=request.get('pri_email_id'),sec_email_id=request.get('sec_email_id'),
    website=request.get('website'),total_doctors=request.get('total_doctors'),total_experts=request.get('total_experts'),total_beds=request.get('total_beds'),total_wards=request.get('total_wards'),facilities_others=request.get('facilities_others'),
    establised_year=request.get('establised_year'),medical_specialty=request.get('medical_specialty'),facilities=request.get('facilities'),aayush=request.get('aayush'),medical_insurance=request.get('medical_insurance'),
    twenty_four_hours=request.get('twenty_four_hours'),provider_type_others=request.get('provider_type_others'),specialties_others=request.get('specialties_others'),medical_insurance_others=request.get('medical_insurance_others'),dial_code=request.get('dial_code'),time_zone=request.get('time_zone'),
    facebook_link=request.get('facebook_link'),instagram_link=request.get('instagram_link'),linkedin_link=request.get('linkedin_link'),googlemap_link=request.get('googlemap_link'))
  workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
  if request['twenty_four_hours'] != "Yes":
    if len(workingdetails['working_days']) > 0:
      for i in workingdetails['working_days']:
        if (i['start_time'] !='') and (i['start_time'] != None):
          hospital_working = models.HospitalWorkingDetails.objects.create(hospital_n_key=hos_create.hospital_n_key,org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],end_time=i['end_time'],
            created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
  if len(workingdetails['special_hours']) > 0:
    for j in workingdetails['special_hours']:
      special_hours = models.HospitalSpecialHours.objects.create(hospital_n_key=hos_create.hospital_n_key,org_n_key=request['org_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],
        end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
  hos_check = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
  if len(hos_check)==1:
    models.EmployeesMaster.objects.filter(employee_n_key=hos_create.employee_n_key).update(hospital_n_key=hos_create.hospital_n_key)
  hos_data = serializer1.HospitalMasterSerializer(hos_check[0]).data
  hos_last = serializer1.HospitalMasterSerializer(hos_check[len(hos_check)-1]).data
  return HttpResponse(json.dumps({"status":"success","last_details":hos_last,"details":hos_data,"time_zone":request.get('time_zone')}),content_type='application/json')


# def workingSpecialHourse(workingdays, specialhours):
#   splhours = []
#   working_days = []
#   def timeChange(time):
#     return datetime.datetime.strptime(time, '%I:%M %p').strftime("%H:%M:%S") if time != None and time != '' else None
#   working_days = [dict(x, **{'start_time':'00:00:00', 'end_time': '23:59:00'}) if x['start_time']=='24Hours' else dict(x, **{'start_time':timeChange(x['start_time']), 'end_time': timeChange(x['end_time'])}) for x in [y for x in [v for k,v in workingdays.items() if len(v)>0] for y in x ]]
#   splhours = [dict(x, **{'start_time':'00:00:00', 'end_time': '23:59:00'}) if x['start_time']=='24Hours' else dict(x, **{'start_time':timeChange(x['start_time']), 'end_time': timeChange(x['end_time'])}) for x in specialhours]
#   return {"working_days":working_days, "special_hours":splhours}

@csrf_exempt
def Hospital_Working_Details_Edit(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital = models.HospitalMaster.objects.filter(hospital_n_key=request['hospital_n_key'])
  today = datetime.datetime.now(timezone(hospital[0].time_zone)).date()
  hos_work_data = []
  hos_spec_data = []
  hospital_work = models.HospitalWorkingDetails.objects.filter(Q(hospital_n_key=request['hospital_n_key'])).values('working_days','start_time','end_time')
  hospital_spec = models.HospitalSpecialHours.objects.filter(Q(hospital_n_key=request['hospital_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
  hospital_data = serializer1.HospitalMasterSerializer(hospital, many=True).data
  hospital_data[0]['working_days'] = {}
  hospital_data[0]['special_hours'] = []
  if hospital[0].twenty_four_hours == 'Yes':
    return HttpResponse(json.dumps({"hospital":hospital_data,"working_details":{},"special_hours":[],"check_days":[],"special_hours_closed":[]}),content_type="application/json")
  convert = ReArrangeWorking(hospital_work,hospital_spec)
  return HttpResponse(json.dumps({"hospital":hospital_data,"working_details":convert['working_days'],"special_hours":convert['special_hours'],"special_hours_closed":convert['special_hours_closed'],"check_days":convert['avail_date']}),content_type="application/json")


def ReArrangeWorking(working, specialhours):
  form = ["12:00 AM","12:30 AM","01:00 AM","01:30 AM","02:00 AM","02:30 AM","03:00 AM","03:30 AM","04:00 AM","04:30 AM","05:00 AM","05:30 AM","06:00 AM","06:30 AM","07:00 AM","07:30 AM","08:00 AM","08:30 AM","09:00 AM","09:30 AM","10:00 AM","10:30 AM","11:00 AM","11:30 AM",
          "12:00 PM","12:30 PM","01:00 PM","01:30 PM","02:00 PM","02:30 PM","03:00 PM","03:30 PM","04:00 PM","04:30 PM","05:00 PM","05:30 PM","06:00 PM","06:30 PM","07:00 PM","07:30 PM","08:00 PM","08:30 PM","09:00 PM","09:30 PM","10:00 PM","10:30 PM","11:00 PM","11:30 PM","11:59 PM"]
  splhours = []
  specialhoursclosed = []
  working_days = {}
  spl_date = []
  avail_date = []
  count = []
  date = datetime.datetime.now().date()
  non_working = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
  def timeChange(time):
    return time.strftime('%I:%M %p') if time != None and time != '' else None
  def dateChange(date):
    return date.strftime('%d/%m/%Y')
  count = [(((datetime.datetime.combine(date, i['end_time']) if i['end_time'] != datetime.time(23, 59) else (datetime.datetime.combine(date, datetime.time(0, 0))+datetime.timedelta(days=1))) - datetime.datetime.combine(date, i['start_time'])).total_seconds()) for i in working]
  for i in non_working:
    temp = ({i:[j for j in working if j['working_days'].lower() == i]})
    work = []
    if len(temp[i])>0:
      work = [dict(item, **{'day':item['working_days'],'start_time':'24Hours','end_time':None,'startTime':form,'endTime':form}) if item['start_time'] == datetime.time(0, 0) and item['end_time'] == datetime.time(23, 59) else dict(item, **{'day':item['working_days'],'start_time':timeChange(item['start_time']),'end_time':timeChange(item['end_time']),'startTime':form,'endTime':form}) for item in temp[i]]
      temp[i] = work
      avail_date.append(work[0]['day'])
    working_days.update(temp)
  [spl_date.append(k['special_date']) for k in specialhours if k['special_date'] not in spl_date]
  for m in spl_date:
    temp_spec = ({'date':str(m),'times':[n for n in specialhours if n['special_date'] == m]})
    spec_work = []
    if len(temp_spec['times'])>0 :
      spec_work = [dict(item, **{'start_time':'24Hours','end_time':None,'date':dateChange(item['special_date']),'special_date':str(item['special_date']),'startTime':form,'endTime':form}) if item['start_time'] == datetime.time(0, 0) and item['end_time'] == datetime.time(23, 59) else dict(item, **{'start_time':timeChange(item['start_time']),'end_time':timeChange(item['end_time']),'date':dateChange(item['special_date']),'special_date':str(item['special_date']),'startTime':form,'endTime':form}) for item in temp_spec['times']]
      temp_spec['times'] = spec_work if spec_work[0]['available'] != 'Closed' else []
      temp_spec['check'] = "Open" if spec_work[0]['available'] != 'Closed' else None
    [splhours.append(temp_spec) if len(temp_spec['times']) !=0 else specialhoursclosed.append(temp_spec)]
  # totalHours = int(sum(count))//3600
  doc_minutes = int(sum(count))
  hour = doc_minutes // 3600
  doc_minutes %= 3600
  minute = doc_minutes // 60
  totalHours = str(hour)+':'+str(minute)
  return {"working_days":working_days, "total_hours":totalHours, "special_hours":splhours, "special_hours_closed":specialhoursclosed, "avail_date":list(set(avail_date))}

@csrf_exempt
def CouponCodePost(request):
  request = json.loads(request.body.decode('utf-8'))
  hospital = models.HospitalMaster.objects.filter(hospital_n_key=request['hospital_n_key'])
  request['created_on']=dt.now(timezone(hospital[0].time_zone)).strftime('%Y-%m-%d %H:%M:%S')
  request['expire_date'] = datetime.datetime.strptime(request['expire_date'] , "%Y-%m-%d").replace(hour=23,minute=59,second=59)
  if request['payment_type']=='Single Pay':
    request['promo_code'] = request['promo_details'][0]['promo_code']
    request['percentage'] = request['promo_details'][0]['percentage']
  if request['payment_type']== 'Subscription Pay':
    request['promo_code'] = request['promo_details'][0]['promo_code']
    request['percentage'] = request['promo_details'][0]['percentage']
    request['promo_code_two'] = request['promo_details'][1]['promo_code']
    request['percentage_two'] = request['promo_details'][1]['percentage']
    request['promo_code_three'] = request['promo_details'][2]['promo_code']
    request['percentage_three'] = request['promo_details'][2]['percentage']

  promo = serializer1.PromoCodeDetailsSerializer(data = request)
  if promo.is_valid():
    promo.save()
    return HttpResponse(json.dumps({'status':'success','data':promo.data}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({'status':'failed','data':promo.errors}), content_type="application/json")

@csrf_exempt
def ListPromocode(request):
  request = json.loads(request.body.decode('utf-8'))
  promo = models.PromoCodeDetails.objects.filter(Q(org_n_key=request['org_n_key'])&Q(status='valid'))
  if promo:
    promo_data = serializer1.PromoCodeDetailsSerializer(promo, many=True).data
    return HttpResponse(json.dumps({'status':'success','data':promo_data}), content_type="application/json")
  return HttpResponse(json.dumps({'status':'failed','data':[]}), content_type="application/json")

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def PromoCodeUpdate(request, pk):
  try:
    snippet = models.PromoCodeDetails.objects.get(pk=pk)
  except models.PromoCodeDetails.DoesNotExist:
    return HttpResponse(json.dumps({"data":"no data found"}),content_type="application/json")

  if request.method == 'GET':
    query_data = models.PromoCodeDetails.objects.filter(pk=pk).values('promo_id','expire_date','user','status','promo_type','patient_name','hospital_n_key','org_n_key','promo_details','payment_type','product','product_type')
    return_data = query_data[0]
    # serializer =serializer1.PromoCodeDetailsSerializer(snippet)
    # return_data = serializer.data
    # return_data[0]['percentage'] = int(float(return_data['percentage']))
    return_data['expire_date'] = str(return_data['expire_date'])
    return HttpResponse(json.dumps({'status':'success','data':return_data}), content_type="application/json")

  elif request.method == 'PUT':
    request = json.loads(request.body.decode('utf-8'))
    request['modified_on']=TimeZoneConvert(snippet.hospital_n_key)
    if 'expire_date' in request:
      request['expire_date'] = datetime.datetime.strptime(request['expire_date'] , "%Y-%m-%d").replace(hour=23,minute=59,second=59)
    if request['payment_type']=='Single Pay':
      request['promo_code'] = request['promo_details'][0]['promo_code']
      request['percentage'] = request['promo_details'][0]['percentage']
    if request['payment_type']== 'Subscription Pay':
      request['promo_code'] = request['promo_details'][0]['promo_code']
      request['percentage'] = request['promo_details'][0]['percentage']
      request['promo_code_two'] = request['promo_details'][1]['promo_code']
      request['percentage_two'] = request['promo_details'][1]['percentage']
      request['promo_code_three'] = request['promo_details'][2]['promo_code']
      request['percentage_three'] = request['promo_details'][2]['percentage']

    serializer =serializer1.PromoCodeDetailsSerializer(snippet, data=request, partial=True)
    if serializer.is_valid():
      serializer.save()
      return HttpResponse(json.dumps({'status':'success','data':serializer.data}), content_type="application/json")
    return HttpResponse(json.dumps({'status':'failed','data':serializer.errors}), content_type="application/json")

  elif request.method == 'DELETE':
    snippet.delete()
    return HttpResponse(json.dumps({"status":"success","data":"data deleted successfully"}),content_type="application/json")

  else:
    return HttpResponse(json.dumps({"status":"failed","data":"Method Not Allowed"}),content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def PatientCalendarSearch(request):
  payload = json.loads(request.body.decode('utf-8'))
  info = payload['patientinfo'].isdigit()
  if info:
    patient = models.PatientMaster.objects.filter(Q(phone_number=int(payload['patientinfo'])) & Q(org_n_key=payload['org_n_key']))
    if patient:
      patientdetails=serializer1.PatientMasterSerializer(patient, many=True).data
      return HttpResponse(json.dumps(patientdetails),content_type='application/json')
    else:
      return HttpResponse(json.dumps([]),content_type='application/json')
  else:
    queryset = []
    patient_name = models.PatientMaster.objects.filter(Q(first_name__istartswith=payload['patientinfo']) & Q(org_n_key=payload['org_n_key']))
    for i in patient_name:
      queryset.append(i)
    patient = models.PatientMaster.objects.filter((Q(first_name__startswith=payload['patientinfo']) | Q(first_name__contains=payload['patientinfo']) | Q (first_name__icontains=payload['patientinfo']) | Q (unique_health_n_key=payload['patientinfo']) | Q(patient_n_key=payload['patientinfo'])) & Q(org_n_key=payload['org_n_key']))
    for j in patient:
      if j not in queryset:
        queryset.append(j)
    patientdetails=serializer1.PatientMasterSerializer(queryset, many=True).data
    return HttpResponse(json.dumps(patientdetails),content_type='application/json')

@csrf_exempt
@api_view(["POST"])
def getClinicWorkingHours(request):
  request = json.loads(request.body.decode('utf-8'))
  hos_work_data = []
  hos_spec_data = []
  hospital = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']))
  clinical = models.ClinicalMaster.objects.filter(Q(clinical_n_key=request['clinical_n_key']))
  if clinical:
    today = datetime.datetime.now(timezone(hospital[0].time_zone)).date()
    twen_four = clinical[0].twenty_four_hours
    clinical_work = models.ClinicalWorkingDetails.objects.filter(Q(clinical_n_key=request['clinical_n_key'])).values('working_days','start_time','end_time')
    clinical_spec = models.ClinicalSpecialHours.objects.filter(Q(clinical_n_key=request['clinical_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
    clinical_data = serializer1.ClinicalMasterSerializer(clinical, many=True).data
    clinical_data[0]['working_days'] = {}
    clinical_data[0]['special_hours'] = []
    if clinical[0].twenty_four_hours == 'Yes':
      work_details = {"sunday":[],"monday":[],"tuesday":[],"wednesday":[],"thursday":[],"friday":[],"saturday":[]}
      return HttpResponse(json.dumps({'status':twen_four,'working_details':work_details,'special_hours':[],"check_days":[],"special_hours_closed":[]}),content_type="application/json")
    convert = ReArrangeWorking(clinical_work,clinical_spec)
    return HttpResponse(json.dumps({'status':twen_four,'working_details':convert['working_days'],'special_hours':convert['special_hours'],'special_hours_closed':convert['special_hours_closed'],"check_days":convert['avail_date']}),content_type="application/json")
  return HttpResponse(json.dumps({'status':'No Hospital Details Found'}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def EditEmployeeDetails(request):
  request = json.loads(request.body.decode('utf-8'))
  working_enable = 'No'
  working_format = []
  special_hours_closed=[]
  emp = models.EmployeesMaster.objects.filter(Q(employee_n_key=request['employee_n_key']))
  if not emp:
    return HttpResponse(json.dumps({'status':'failed','data':'No Hospital Details Found'}),content_type="application/json")
  working_days = {}
  special_hours = []
  check_days = []
  emp_data = serializer1.EmployeesMasterSerializer(emp[0]).data
  doc_role = DoctorRoleQuery(emp[0].org_n_key)
  emp_data['role_check'] = 'No'
  if (emp[0].role in doc_role) or (emp[0].role == 'Physician'):
    mdroles = models.GERoles.objects.filter(Q(org_n_key=emp[0].org_n_key)&Q(roles_name=emp[0].role))
    working_enable=mdroles[0].working_enable if mdroles else 'No'
    emp_data['role_check'] = 'Yes'
    emp_data['cal_n_key'] = None
    emp_data['interval'] = None
    emp_data['doctor_n_key'] = None
    emp_data['product_name'] = None
    calendar = models.CalendarSettings.objects.filter(Q(employee_n_key=request['employee_n_key']))
    if calendar:
      emp_data['cal_n_key'] = calendar[0].cal_n_key
      emp_data['interval'] = calendar[0].interval
      emp_data['allow_overlap'] = calendar[0].allow_overlap
    doctor = models.GeDoctorDetails.objects.filter(Q(employee_n_key=request['employee_n_key']))
    if doctor:
      emp_data['doctor_n_key'] = doctor[0].doctor_n_key
    access = models.MdAccess.objects.filter(Q(emp_n_key=request['employee_n_key']))
    if access:
      emp_data['product_name'] = access[0].product_name
    hospital = models.HospitalMaster.objects.filter(Q(hospital_n_key=emp[0].hospital_n_key))
    today = datetime.datetime.now(timezone(hospital[0].time_zone)).date()
    emp_work = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=request['employee_n_key'])).values('working_days','start_time','end_time')
    emp_spec = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=request['employee_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
    # print(emp_spec)
    emp_work_data = []
    emp_spec_data = []
    convert = ReArrangeWorking(emp_work,emp_spec)
    special_hours_closed=convert['special_hours_closed']
    working_days = convert['working_days']
    special_hours = convert['special_hours']
    check_days = convert['avail_date']
    non_working = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    for z in non_working:
      slots = {}
      daycheck = emp_work.filter(working_days=z)
      if daycheck:
        slots['day'] = z
        slots['count'] = len(daycheck)
        slots['work_hours'] = []
        for l in daycheck:
          slots['work_hours'].append({'start_time':l['start_time'].strftime('%I:%M %p'),'end_time':l['end_time'].strftime('%I:%M %p')})
        working_format.append(slots)  
  return HttpResponse(json.dumps({'status':'success','data':emp_data,'working_details':working_days,'special_hours':special_hours, 'special_hours_closed':special_hours_closed,'check_days':check_days,'format':working_format,'working_enable':working_enable}),content_type="application/json")


@csrf_exempt
# @api_view(["POST"])
def GetOrgPlan(request):
  request = json.loads(request.body.decode('utf-8'))
  return_data = {}
  org = models.OrganizationMaster.objects.filter(Q(org_n_key=request['org_n_key']))
  if not org:
    return HttpResponse(json.dumps({'status':'failed','data':{}}),content_type="application/json")
  return_data['organization_name'] = org[0].org_name
  return_data['day'] = datetime.datetime.now().strftime('%A')
  today = datetime.datetime.now().date()
  plan = models.PlanDetails.objects.filter(Q(product_name=request['product_name']))
  current = models.MdPaymentPricing.objects.filter(Q(org_n_key=request['org_n_key'])&Q(product_name=request['product_name'])).order_by('-payment_pricing_id')
  ex_day = (current[0].expire_date - today).days if current else 0
  return_data['expired_day'] = ex_day if ex_day > 0 else 0
  return_data['trial_or_plan'] = 'trial' if not current or current[0].subscrib_type == 'free' else 'plan'
  plan_name = plan[0].plan_name.split(',')
  # plan_value = plan[0].plan_name.split(',')
  # return_data['plan_name'] = plan_name[plan_value.index(current[0].current_plan)]
  return_data['plan_name'] = current[0].current_plan if current else plan_name[0]
  price = plan[0].price.split(',')
  sms = plan[0].sms.split(',')
  employees = plan[0].employees.split(',')
  hospitals = plan[0].hospitals.split(',')
  return_data['annually_plan_details']={
    "basic_plan":{
        "name":plan_name[0],
        "details":json.loads(json.dumps(plan[0].specification).format(hospitals[0],employees[0],sms[0])),
        "amount":int(price[0])*10
    },
    "advanced_plan":{
        "name":plan_name[1],
        "details":json.loads(json.dumps(plan[0].specification).format(hospitals[1],employees[1],sms[1])),
        "amount":int(price[1])*10
    },
    "premium_plan":{
        "name":plan_name[2],
        "details":json.loads(json.dumps(plan[0].specification).format(hospitals[2],employees[2],sms[2])),
        "amount":int(price[2])*10
    }
  }
  return_data['monthly_plan_details']={
    "basic_plan":{
        "name":plan_name[0],
        "details":json.loads(json.dumps(plan[0].specification).format(hospitals[0],employees[0],sms[0])),
        "amount":int(price[0])
    },
    "advanced_plan":{
        "name":plan_name[1],
        "details":json.loads(json.dumps(plan[0].specification).format(hospitals[1],employees[1],sms[1])),
        "amount":int(price[1])
    },
    "premium_plan":{
        "name":plan_name[2],
        "details":json.loads(json.dumps(plan[0].specification).format(hospitals[2],employees[2],sms[2])),
        "amount":int(price[2])
    }
  }
  org_data = serializer1.OrganizationMasterSerializer(org, many=True).data[0]
  return_data['user_details']={
    "address": None,
    "city": None,
    "state": None,
    "postal_code": None,
    "country": None
  }
  return_data['user_details'].update(org_data)
  return_data['user_details']['email_id'] = return_data['user_details'].pop('email')
  return_data['user_details']['phone_number'] = return_data['user_details'].pop('phone_num')
  return_data['current_plan'] = ORGcurrentPlan(request['org_n_key'],request['product_name'])
  return HttpResponse(json.dumps({'status':'success','data':return_data}),content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Cancel_plan(request):
  request = json.loads(request.body.decode('utf-8'))
  current = models.MdPaymentPricing.objects.filter(Q(org_n_key=request['org_n_key'])).order_by('-payment_pricing_id')
  today = datetime.datetime.now().date() + datetime.timedelta(days=-1)
  for i in current:
    i.expire_date = today
    i.save()
    break
  return HttpResponse(json.dumps({'status':'success'}),content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def EmpOtherDocPost(request):
  data = json.loads(request.POST['data'])
  document_image = None
  data['created_on']=TimeZoneConvert(data['hospital_n_key'])
  if request.method == 'POST':
    fs = FileSystemStorage()
    try:
      if request.FILES.get('document_image') != None:
        myfile = request.FILES['document_image']
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000':
          http_address =  'http://'
          document_image = http_address + request.get_host() + uploaded_file_url
        else:
          http_address = 'https://'
          document_image = http_address + request.get_host() + "/api" + uploaded_file_url
    except Exception as e:
      return HttpResponse(json.dumps({"status":"failed","data":e}), content_type="application/json")

    data['document_image'] = document_image
    serializer =serializer1.EmployeeOtherDocumentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        ret = serializer.data
        hospital = models.HospitalMaster.objects.filter(hospital_n_key=data['hospital_n_key'])
        ret['date'] = datetime.datetime.now(timezone(hospital[0].time_zone)).strftime("%d/%m/%Y")
        return HttpResponse(json.dumps({"status":"success","data":ret['date']}), content_type="application/json")
    return HttpResponse(json.dumps({"status":"failed","data":serializer.errors}), content_type="application/json")
  return HttpResponse(json.dumps({"status":"failed","data":"Method Not Allowed"}), content_type="application/json")


@csrf_exempt
def GetPortalDetails(request):
  request = json.loads(request.body.decode('utf-8'))
  alldata = {}
  hos_images = ["https://synapstics.com/api/media/hospital1.png","https://synapstics.com/api/media/hospital2.png","https://synapstics.com/api/media/hospital3.svg"]
  org = models.OrganizationMaster.objects.filter(Q(org_n_key=request['org_n_key']))
  if not org:
    return HttpResponse(json.dumps({"status":"failed","data":"No Organization Found"}), content_type="application/json")
  hospitals = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']))
  alldata['hospital_details']={}
  hospital_data = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key'])).values('hospital_name','hospital_logo','banner_image','dial_code','hospital_phoneno','ambulance_no','pri_email_id','hospital_address_line_one','city','suburb','pincode','facebook_link','instagram_link','twitter_link','linkedin_link','googlemap_link','about_us','whatsapp_number','whatsapp_dialcode')
  for x in hospital_data:
    x['phone_number']=str(x['hospital_phoneno'])
    x['email_id']=x['pri_email_id']
    x['whatsapp_number']=str(x['whatsapp_number']) if x['whatsapp_number'] != None else None 
    x['whatsapp_link']='https://wa.me/'+x['whatsapp_dialcode']+str(x['whatsapp_number']) if x['whatsapp_number'] != None else None 
    x['ambulance_number']=str(x['ambulance_no']) if x['ambulance_no'] != None else None
    x['address'] = x['hospital_address_line_one']
    del x['hospital_phoneno'],x['ambulance_no'],x['pri_email_id'],x['hospital_address_line_one']
    if x['banner_image'] == None or x['banner_image'] == '':
      x['banner_image'] = hos_images
    if x['hospital_logo'] == None or x['hospital_logo'] == '':
      x['hospital_logo'] = x['hospital_name'][0]
    alldata['hospital_details'] = x
  
  doc_role = ["Physician"]
  mdroles = models.GERoles.objects.filter(Q(role_check='Yes') & Q(org_n_key=request['org_n_key']))
  if mdroles:
    for k in mdroles:
      if k.roles_name not in doc_role:
        doc_role.append(k.roles_name)
  doctor = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(hospital_n_key=request['hospital_n_key']) & Q(role__in=doc_role) & Q(is_active=1))
  doctor_data = models.EmployeesMaster.objects.filter(Q(org_n_key=request['org_n_key']) & Q(hospital_n_key=request['hospital_n_key']) & Q(role__in=doc_role) & Q(is_active=1)).values('first_name','last_name','dial_code','designation','speciality','facebook_link','instagram_link','twitter_link','linkedin_link','employee_n_key')
  alldata['doctor_details'] = []
  for z in doctor_data:
    z['doctor_logo'] = None
    z['doctor_name'] = z['first_name'] + ' '+z['last_name']
    z['speciality'] = ",".join(z['speciality']) if z['speciality'] != None else ''
    doc = models.Employeedocuments.objects.filter(Q(doctor_n_key=z['employee_n_key']))
    edu = []
    education = models.Empeducationaldetails.objects.filter(Q(employee_n_key=z['employee_n_key']))
    [edu.append(e.qualification_title) for e in education]
    z['qualification'] = ",".join(edu)
    z['doctor_logo'] = str(doc[0].emp_attachment) if doc else z['doctor_logo']
    del z['employee_n_key']
    alldata['doctor_details'].append(z)
  alldata['doctor_details'] = alldata['doctor_details'][:8]

  specialities = []
  facilities = []
  alldata['aayush'] = []
  alldata['medical_insurance'] = []

  alldata['specialities'] = (hospitals[0].medical_specialty).split(',') if hospitals[0].medical_specialty != None else []
  facilities = (hospitals[0].facilities).split(',') if hospitals[0].facilities != None else []
  aayush= (hospitals[0].aayush).split(',') if hospitals[0].aayush != None else []
  medical_insurance= (hospitals[0].medical_insurance).split(',') if hospitals[0].medical_insurance != None else []
  alldata['facilities'] = facilities + aayush + medical_insurance
  doc_speciality = []
  for k in doctor:
    temp_spec = k.speciality if k.speciality != None else []
    for l in temp_spec:
      if l not in doc_speciality:
        doc_speciality.append(l)
  alldata['services'] = doc_speciality

  alldata['doctor_timing'] = []
  for i in doc_speciality:
    temp_time = {}
    spec_doctor = doctor.filter(Q(speciality__icontains=i))
    temp_time['speciality'] = i
    temp_time['count'] = len(spec_doctor)
    temp_time['details'] = []
    for j in spec_doctor:
      temp_details = {}
      temp_details['doctor_name'] = j.first_name + " " + j.last_name if j.last_name != None else j.first_name
      emp_work_data = []
      emp_spec_data = []
      consultation_days=[]
      today = datetime.datetime.now(timezone(hospitals[0].time_zone)).date()
      emp_work = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=j.employee_n_key)&Q(hospital_n_key=request['hospital_n_key'])).values('working_days','start_time','end_time')
      emp_spec = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=j.employee_n_key) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
      
      for k in emp_work:
        if k['working_days'] not in consultation_days:
          consultation_days.append(k['working_days'])
      temp_details['consultation_days']=','.join(consultation_days)
      
      working_details = []
      non_working = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
      for z in non_working:
        slots = {}
        daycheck = emp_work.filter(working_days=z)
        if daycheck:
          slots['day'] = z
          slots['count'] = len(daycheck)
          slots['work_hours'] = []
          for l in daycheck:
            slots['work_hours'].append({'start_time':l['start_time'].strftime('%I:%M %p'),'end_time':l['end_time'].strftime('%I:%M %p')})
          working_details.append(slots)          
      temp_details['working_details'] = working_details
      temp_time['details'].append(temp_details)
    alldata['doctor_timing'].append(temp_time)
  return HttpResponse(json.dumps({"status":"success","data":alldata}), content_type="application/json")

# @csrf_exempt
# @api_view(["POST"])
# def Enable_Disable_Online_Practice(request):
#   request = json.loads(request.body.decode('utf-8'))
#   https_address = 'https://synapstics.com'
#   if request['online_practice_status'] == None:
#     if request['product_name'] == 'Mrecs':
#       orgnazation = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key']).update(online_practice=request['online_practice'])
#       hospitals = models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key']))
#       data = []
#       for hospital in hospitals:
#         if request['online_practice'] == 'Yes':
#           models.HospitalMaster.objects.filter(hospital_n_key=hospital.hospital_n_key).update(online_practice_status='Enable',url=https_address +"/hospital/"+ hospital.org_n_key+"/"+hospital.hospital_n_key)
#           hospital_data = models.HospitalMaster.objects.filter(Q(hospital_n_key=hospital.hospital_n_key)).values('online_practice_status','url','hospital_name','hospital_n_key','hospital_address_line_one','city','suburb','pincode')
#           data.append([hospital_data[0]])
#         else:
#           models.HospitalMaster.objects.filter(hospital_n_key=hospital.hospital_n_key).update(online_practice_status=None,url=None)
#       orgnazation1 = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key'])
#       return HttpResponse(json.dumps({"status":"success","data":data, "online_practice":orgnazation1[0].online_practice}), content_type="application/json")
#     if request['product_name'] == 'DigiBlood':
#       orgnazation = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key']).update(online_bloodbank=request['online_practice'])
#       bloods = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
#       data = []
#       for blood in bloods:
#         if request['online_practice'] == 'Yes':
#           models.BloodBank_Master.objects.filter(bloodbank_n_key=blood.bloodbank_n_key).update(online_practice_status='Enable',url=https_address +"/bloodbank/"+ blood.org_n_key+"/"+blood.bloodbank_n_key)
#           blooddata = models.BloodBank_Master.objects.filter(Q(bloodbank_n_key=hospital.bloodbank_n_key)).values('online_practice_status','url','bloodbank_name','bloodbank_n_key','bloodbank_address_line_one','city','suburb','pincode')
#           data.append([blooddata[0]])
#         else:
#           models.BloodBank_Master.objects.filter(bloodbank_n_key=blood.bloodbank_n_key).update(online_practice_status=None,url=None)
#       orgnazation1 = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key'])
#       return HttpResponse(json.dumps({"status":"success","data":data, "online_practice":orgnazation1[0].online_bloodbank}), content_type="application/json")
#   else:
#     hospitals = models.HospitalMaster.objects.filter(hospital_n_key=request['hospital_n_key']).update(online_practice_status=request['online_practice_status'])
#     return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")

@csrf_exempt
@api_view(["POST"])
def Get_Online_Practice(request):
  request = json.loads(request.body.decode('utf-8'))
  data = []
  blood_data = []
  https_address = 'https://synapstics.com'
  orgnazation1 = models.OrganizationMaster.objects.filter(org_n_key=request['org_n_key'])
  if orgnazation1[0].online_practice == 'Yes':
    data = list(models.HospitalMaster.objects.filter(Q(org_n_key=request['org_n_key'])).values('online_practice_status','url','hospital_name','hospital_n_key','hospital_address_line_one','city','suburb','pincode','state','hospital_phoneno','online_practice_status'))
    for i in data:
      i['product_name'] = 'Mrecs'
      i['online_practice_status'] = 'Enable' if i['online_practice_status'] == 'Enable' else 'Disable'
      i['hospital_phoneno'] = str(i['hospital_phoneno'])
      i['url'] =https_address +"/hospital/"+ request['org_n_key'] +"/"+ i['hospital_n_key']
  if orgnazation1[0].online_bloodbank == 'Yes':  
    blood_data = list(models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key'])).values('online_practice_status','url','bloodbank_name','bloodbank_n_key','bloodbank_address_line_one','city','suburb','pincode','state','bloodbank_phoneno','online_practice_status'))
    for j in blood_data:
      j['product_name'] = 'DigiBlood'
      j['online_practice_status'] = 'Enable' if j['online_practice_status'] == 'Enable' else 'Disable'
      j['bloodbank_phoneno'] = str(j['bloodbank_phoneno'])
      j['url'] =https_address +"/bloodbank/"+ request['org_n_key'] +"/"+ j['bloodbank_n_key']
  mrecs =  models.MdPaymentPricing.objects.filter(Q(product_name='Mrecs') & Q(org_n_key=request['org_n_key'])).exists()
  DigiBlood =  models.MdPaymentPricing.objects.filter(Q(product_name='DigiBlood') & Q(org_n_key=request['org_n_key'])).exists()
  return HttpResponse(json.dumps({"status":"success","data":data, "blood_data":blood_data, "online_practice":orgnazation1[0].online_practice,"online_bloodbank":orgnazation1[0].online_bloodbank,"subscriptionstatus":{'mrecs':mrecs,'DigiBlood':DigiBlood}}), content_type="application/json")

@csrf_exempt
def subscriptionstatus(request):
  request = json.loads(request.body.decode('utf-8'))
  mrecs =  models.MdPaymentPricing.objects.filter(Q(product_name='Mrecs') & Q(org_n_key=request['org_n_key'])).exists()
  DigiBlood =  models.MdPaymentPricing.objects.filter(Q(product_name='DigiBlood') & Q(org_n_key=request['org_n_key'])).exists()
  return HttpResponse(json.dumps({'mrecs':mrecs,'DigiBlood':DigiBlood}), content_type="application/json")


# blood bank apis

# @csrf_exempt
# @api_view(["POST"])
# def BloodBank_Details_Post(request):
#   request = json.loads(request.body.decode('utf-8'))
#   time_zone = request.get('time_zone')
#   now_time = datetime.datetime.now(timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S')
#   request['created_on'] = now_time
#   bloodbank_n_key = None
#   bb_create = serializer1.BloodBankMasterSerializer(data=request)
#   if bb_create.is_valid():
#     bb_create.save()
#     details = bb_create.data
#     bloodbank_n_key = details['bloodbank_n_key']
#   else:
#     return HttpResponse(json.dumps({"data":bb_create.errors}),content_type="application/json")
#   workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
#   if request['twenty_four_hours'] != "Yes":
#     if len(workingdetails['working_days']) > 0:
#       for i in workingdetails['working_days']:
#         if (i['start_time'] !='') and (i['start_time'] != None):
#           bloodbank_working = models.BloodBankWorkingDetails.objects.create(bloodbank_n_key=bloodbank_n_key,org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],end_time=i['end_time'],
#             created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
#   if len(workingdetails['special_hours']) > 0:
#     for j in workingdetails['special_hours']:
#       special_hours = models.BloodBankSpecialHours.objects.create(bloodbank_n_key=bloodbank_n_key,org_n_key=request['org_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],
#         end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=now_time)
#   bb_check = models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key']))
#   if len(bb_check)==1:
#     models.EmployeesMaster.objects.filter(employee_n_key=bb_create.employee_n_key).update(bloodbank_n_key=bloodbank_n_key)
#   return HttpResponse(json.dumps({"status":"success"}),content_type='application/json')


def workingSpecialHourse(workingdays, specialhours,specialhoursclosed):
  splhours = []
  working_days = []
  specialhours += specialhoursclosed
  def timeChange(time):
    return datetime.datetime.strptime(time, '%I:%M %p').strftime("%H:%M:%S") if time != None and time != '' else None
  if len(workingdays)>0:
    working_days = [dict(x, **{'start_time':'00:00:00', 'end_time': '23:59:00'}) if x['start_time']=='24Hours' else dict(x, **{'start_time':timeChange(x['start_time']), 'end_time': timeChange(x['end_time'])}) for x in [y for x in [v for k,v in workingdays.items() if len(v)>0] for y in x ]]
  if len(specialhours)>0:
    splhours = [dict(x, **{'start_time':'00:00:00', 'end_time': '23:59:00'}) if x['start_time']=='24Hours' else dict(x, **{'start_time':timeChange(x['start_time']), 'end_time': timeChange(x['end_time'])}) for x in specialhours]
  return {"working_days":working_days, "special_hours":splhours}


# @csrf_exempt
# def BloodBank_Detaile_Edit(request):
#   request = json.loads(request.body.decode('utf-8'))
#   bbank = models.BloodBankMaster.objects.filter(bloodbank_n_key=request['bloodbank_n_key'])
#   today = datetime.datetime.now(timezone(bbank[0].time_zone)).date()
#   bb_work_data = []
#   bb_spec_data = []
#   bb_work = models.BloodBankWorkingDetails.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key'])).values('working_days','start_time','end_time')
#   bb_spec = models.BloodBankSpecialHours.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']) & Q(special_date__gte=today)).values('special_date','available','start_time','end_time')
#   bb_data = serializer1.BloodBankMasterSerializer(bbank, many=True).data
#   bb_data[0]['working_days'] = {}
#   bb_data[0]['special_hours'] = []
#   if bbank[0].twenty_four_hours == 'Yes':
#     return HttpResponse(json.dumps({"bloodbank":bb_data,"working_details":{},"special_hours":[],"check_days":[],"special_hours_closed":[]}),content_type="application/json")
#   convert = ReArrangeWorking(bb_work,bb_spec)
#   return HttpResponse(json.dumps({"bloodbank":bb_data,"working_details":convert['working_days'],"special_hours":convert['special_hours'],'special_hours_closed':convert['special_hours_closed'],"check_days":convert['avail_date']}),content_type="application/json")

# @csrf_exempt
# @api_view(["POST"])
# def BloodBank_Details_Update(request):
#   request = json.loads(request.body.decode('utf-8'))
#   bloodbank = models.BloodBankMaster.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']))
#   if bloodbank:
#     request['modified_on'] = DefaultTimeZone()
#     # request['modified_on'] = TimeZoneConvert(request['bloodbank_n_key'])
#     bb_create = serializer1.BloodBankMasterSerializer(instance=bloodbank[0], data=request, partial=True)
#     if bb_create.is_valid():
#       bb_create.save()
#     else:
#       return HttpResponse(json.dumps({"data":bb_create.errors}),content_type="application/json")
#   work_filter = models.BloodBankWorkingDetails.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']) & Q(org_n_key=request['org_n_key']))
#   if work_filter:
#     work_filter_del = work_filter.delete()
#   workingdetails = workingSpecialHourse(request['working_days'],request['special_hours'],request['special_hours_closed'])
#   if request['twenty_four_hours'] != "Yes":
#     if len(workingdetails['working_days']) > 0:      
#       for i in workingdetails['working_days']:
#         if (i['start_time'] !='') and (i['start_time'] != None):
#           bloodbank_working = models.BloodBankWorkingDetails.objects.create(bloodbank_n_key=request['bloodbank_n_key'],org_n_key=request['org_n_key'],working_days=i['day'],start_time=i['start_time'],end_time=i['end_time'],
#             created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
#   spec_filter = models.BloodBankSpecialHours.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']) & Q(org_n_key=request['org_n_key']))
#   if spec_filter:
#     spec_filter_del = spec_filter.delete()
#   if len(workingdetails['special_hours']) > 0:
#     for j in workingdetails['special_hours']:  
#       special_hours = models.BloodBankSpecialHours.objects.create(bloodbank_n_key=request['bloodbank_n_key'],org_n_key=request['org_n_key'],special_date=j['date'],available=j['available'],start_time=j['start_time'],
#         end_time=j['end_time'],created_by_id=request['created_by_id'],created_by_name=request['created_by_name'],created_on=DefaultTimeZone())
#   return HttpResponse(json.dumps({"status":'success'}),content_type="application/json")
@csrf_exempt
@api_view(["POST"])
def BoodBank_Wise_GetData(request):
  request = json.loads(request.body.decode('utf-8'))
  data=models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key'])).values('bloodbank_name','bloodbank_n_key','bloodbank_address_line_one','state','city','pincode','bloodbank_phoneno','gst_no','licence_no','time_zone','created_on')
  for i in data:
    i['bloodbank_phoneno'] = str(i['bloodbank_phoneno'])
    i['created_on'] = str(i['created_on'])
  return HttpResponse(json.dumps({"status":'success',"data":list(data)}),content_type="application/json")

# @csrf_exempt
# @api_view(["POST"])
# def BloodBank_Logo_Update(request):
#   find = models.BloodBankMaster.objects.filter(bloodbank_n_key=request.POST['bloodbank_n_key'])
#   https_address = 'https://synapstics.com'
#   http_address = 'http://'
#   if find:
#     if request.method == 'POST' and 'bloodbank_logo' in request.FILES and request.FILES['bloodbank_logo']:
#       myfile = request.FILES['bloodbank_logo']
#       fs = FileSystemStorage()
#       filename = fs.save(myfile.name, myfile)
#       uploaded_file_url = fs.url(filename)
#       http_address = ''
#       if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001':        
#         find.update(bloodbank_logo=http_address + request.get_host()+ uploaded_file_url)
#       else:
#         find.update(hospital_logo=https_address +"/api"+ uploaded_file_url)
#     if request.method == 'POST' and 'banner_image' in request.FILES and request.FILES['banner_image']:
#       myfile = request.FILES['banner_image']
#       fs = FileSystemStorage()
#       filename = fs.save(myfile.name, myfile)
#       uploaded_file_url = fs.url(filename)
#       if request.get_host() == '127.0.0.1:8000' or request.get_host() == 'localhost:8000' or request.get_host() == '127.0.0.1:8001':
#         find.update(banner_image=http_address + request.get_host()+ uploaded_file_url)
#       else:
#         find.update(banner_image=https_address +"/api"+ uploaded_file_url)
#     return HttpResponse(json.dumps({"status":"uploaded successfully"}),content_type="application/json")
#   return HttpResponse(json.dumps({"status":"Failed"}),content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def Appointment_search(request):
  request = json.loads(request.body.decode('utf-8'))
  session = models.AppSessionDetails.objects.filter(Q(appointment_n_key=request['appointment_n_key']))
  if not session:
    return HttpResponse(json.dumps({"status":'failed',"data":"No Session Details"}),content_type="application/json")
  appoint = list(models.AppointmentMaster.objects.filter(Q(appointment_n_key=request['appointment_n_key'])).values('appointment_n_key','doc_app_id','patient_n_key','appointment_date','appointment_time'))
  if appoint:
    patient = models.PatientMaster.objects.filter(Q(patient_n_key=appoint[0]['patient_n_key']))
    credid = models.AppointmentCredits.objects.filter(Q(patient_n_key=appoint[0]['patient_n_key']))
    emp = models.EmployeesMaster.objects.filter(Q(employee_n_key=appoint[0]['doc_app_id']))
    appoint[0]['patient_name'] = patient[0].full_name
    appoint[0]['cancel_count'] = credid.count()
    appoint[0]['appointment_time'] = str(appoint[0]['appointment_time'])
    appoint[0]['appointment_date'] = str(appoint[0]['appointment_date'])+' '+str(appoint[0]['appointment_time'])
    appoint[0]['therapist_name'] = emp[0].first_name

  return HttpResponse(json.dumps({"status":'success',"data":appoint[0]}),content_type="application/json")
  
@csrf_exempt
@api_view(["POST"])
def AddCreditsSessionAppoint(request):
  request = json.loads(request.body.decode('utf-8'))
  session = models.AppSessionDetails.objects.filter(Q(appointment_n_key=request['appointment_n_key']))
  if not session:
    return HttpResponse(json.dumps({"status":'failed',"data":"No Session Details"}),content_type="application/json")
  hospital_n_key = session[0].hospital_n_key
  org_n_key = session[0].org_n_key
  app_payment_n_key = session[0].app_payment_n_key
  try:
    payment = models.InvoiceBillDetails.objects.filter(Q(appointment_n_key=request['appointment_n_key']))
    invoice = models.InvoiceBillPayment.objects.filter(Q(appointment_n_key=request['appointment_n_key']))
    payment.delete() if payment else None
    invoice.delete() if invoice else None
    session.delete() if session else None
  except Exception as e:
    pass
  request['hospital_n_key'] = hospital_n_key
  request['org_n_key'] = org_n_key
  request['app_payment_n_key'] = app_payment_n_key
  request['created_on'] = TimeZoneConvert(hospital_n_key)
  credit = serializer1.AppointmentCreditsSerializer(data=request)
  if credit.is_valid():
    credit.save()
    return HttpResponse(json.dumps({"status":"success","data":credit.data}),content_type="application/json")
  else:
    return HttpResponse(json.dumps({"status":"failed","data":credit.errors}),content_type="application/json")


def NewPayment(request):
  session = int(request['total_session'])
  request['product_amount']= 1499*session
  request['payment_status'] = 'Payment Success'
  request['split_session']=[session]
  request['discount'] = round((100*(1499*session - int(request['amount'])) / (1499*session)),2)
  request['discount_amount'] = 1499*session - int(request['amount'])
  if request['app_prod_n_key'] == 'APP_PROD-0':
    product = models.AppProductDetails.objects.filter(Q(app_prod_n_key=request['app_prod_n_key']))
    plan_a,plan_b,plan_c = json.loads(product[0].plan_a),json.loads(product[0].plan_b),json.loads(product[0].plan_c)
    plan = [int(plan_a['amount']),int(plan_b['amount']),int(plan_c['amount'])]
    request['product_amount'] = min(plan, key=lambda x:abs(x-session))
    request['payment_status'] = 'Completed'
    request['discount'] = round((100*(request['product_amount'] - int(request['amount'])) / request['product_amount']),2)
    request['discount_amount'] = request['product_amount'] - int(request['amount'])
    if 'doctors' in request:
      del request['doctors']
  app_pay = serializer1.AppPaymentDetailsSerializer(data=request)
  if app_pay.is_valid():
    app_pay.save()
    return {"status":"success","data":app_pay.data['app_payment_n_key']}
  else:
    return {"status":"failed","data":app_pay.errors}

def UpdatePayment(request):
  bought_session = int(request['total_session'])
  single_pay = round(float(request['amount'])/bought_session,2)
  single_discount = 1499 - single_pay
  payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
  
  invoice = payment[0].invoice.split(',') if payment[0].invoice != None else []
  invoice_discount = payment[0].invoice_discount.split(',') if payment[0].invoice_discount != None else []
  doctors = payment[0].doctors.split(',') if payment[0].doctors != None else []
  product_amount = payment[0].product_amount.split(',') if payment[0].product_amount != None else []
  discount = payment[0].discount.split(',') if payment[0].discount != None else []
  discount_amount = payment[0].discount_amount.split(',') if payment[0].discount_amount != None else []
  split_session = payment[0].split_session if payment[0].split_session != None else [int(payment[0].total_session)]
  amount = payment[0].amount.split(',') if payment[0].amount != None else []
  payment_details = payment[0].payment_details.split(',') if payment[0].payment_details != None else []
  created_on = payment[0].created_on.split(',') if payment[0].created_on != None else []
  
  amount.append(request['amount'])
  product_amount.append(str(1499 * bought_session))
  discount_amount.append(str((1499 * bought_session)-int(request['amount'])))
  discount.append(str(round(100 * ((1499*bought_session) - int(request['amount'])) / (1499*bought_session) , 2)))
  split_session.append(bought_session)
  created_on.append(request['created_on'])
  payment_details.append(request['payment_details'])
  for k in range(bought_session):
    invoice.append(str(single_pay))
    invoice_discount.append(str(single_discount))
    doctors.append(request['doctors'])
  total = int(payment[0].total_session) + bought_session
  payment.update(invoice=",".join(invoice),invoice_discount=",".join(invoice_discount),doctors=",".join(doctors),
        product_amount=",".join(product_amount),discount=",".join(discount),discount_amount=",".join(discount_amount),split_session=split_session,
        amount = ','.join(amount),total_session = total,payment_details = ','.join(payment_details),created_on=','.join(created_on))
  return {"status":"success","data":{}}

@csrf_exempt
def NewCreditsSessionAppoint(request):
  request = json.loads(request.body.decode('utf-8'))
  request['hospital_n_key'] = 'CAR-HOS-1'
  request['org_n_key'] = 'ORGID-1'
  request['clinical_n_key'] = 'CAR-CLI-1'
  request['clinical_name'] = 'Careme-mind'
  request['created_on'] = TimeZoneConvert(request['hospital_n_key'])
  pay_data = []
  payment_check = list(models.AppPaymentDetails.objects.filter(Q(payment_status='Completed') | Q(payment_status='Payment Success')).values_list('payment_details',flat=True))
  for x in payment_check:
    pay_data+=x.split(',')
  if request['payment_details'] in pay_data:
    return HttpResponse(json.dumps({'status':'This payment id is already available'}), content_type="application/json")
  if request['app_payment_n_key'] != None and request['app_payment_n_key'] != '':
    payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
    if payment:
      request['app_prod_n_key'] = payment[0].app_prod_n_key
  if 'app_prod_n_key' in request and request['app_prod_n_key'] == 'APP_PROD-0':
    if request['app_payment_n_key'] != None and request['app_payment_n_key'] != '':
      chat_therapy = RenewChatTherapy(request)
    else:
      app_pay = NewPayment(request)
      request['app_payment_n_key'] = app_pay['data']
      chat_therapy = NewChatTherapy(request)
    return HttpResponse(json.dumps(chat_therapy), content_type="application/json")
  else:
    if request['app_payment_n_key'] != None and request['app_payment_n_key'] != '':
      app_pay = UpdatePayment(request)
    else:
      app_pay = NewPayment(request)
    return HttpResponse(json.dumps(app_pay), content_type="application/json")


def NewChatTherapy(request):
  current = datetime.datetime.strptime(request['created_on'],'%Y-%m-%d %H:%M:%S')
  request['patient_type']='New Patient'
  request['service_name'] = request['product']
  request['overall_status'] = 'Completed'
  request['colour'] = '#eb519eff'
  request['appointment_name'] = 'ChatTherapy'
  request['payment_type'] = 'with payment'
  request['appointment_date'] = current.date()
  request['appointment_time'] = current.time()
  request['appointment_end_time'] = current.time()
  product = models.AppProductDetails.objects.filter(Q(app_prod_n_key=request['app_prod_n_key']))
  doc_key = product[0].doctor_details if product else ''
  doc_list = doc_key.split(',')
  doctor = models.EmployeesMaster.objects.filter(Q(employee_n_key__in=doc_list) & Q(is_active=1)) if len(doc_list)>0 else []
  if not doctor:
    return {'status':'failed','data':'No Therpist Available'}
  def BookDoctor(doctor_query):
    doc_count = []
    for k in doc_list:
      chat = models.ChatHistory.objects.filter(Q(employee_n_key=[k])&Q(end_date__gte=request['created_on']))
      doc_count.append(chat.count())
    index = doc_count.index(min(doc_count))
    request['doc_app_id']=doc_list[index]
    appoint = serializer1.AppointmentMasterSerializer(data = request)
    if appoint.is_valid():
      appoint.save()
      request['appointment_n_key']=appoint.data['appointment_n_key']
      payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
      if payment:
        payment.update(payment_status='Completed',appointment_n_key=appoint.data['appointment_n_key'])
      try:
        invoice = session_service_pay(appoint.data['appointment_n_key'],request,request['total_session'],payment)
      except Exception as e:
        pass   
      chat_post = ChatTherapyPost(request,current)
      return {'status':'success','data':{}}
    else:
      return {'status':'error','data':appoint.errors}
  book = BookDoctor(doctor)
  if book['status'] == None:
    return {'status':'failed','data':'No Therpist Available'}
  else:
    return book

def ChatTherapyPost(request,current):
  request['modified_on'] = current
  request['channelid'] = request['appointment_n_key']
  request['type_of_chat'] = 'ChatTherapy'
  request['employee_n_key'] = [request['doc_app_id']]
  request['end_date'] = current + relativedelta(days = int(request['total_session']))
  chat = serializer1.ChatHistorySerializer(data=request)
  if chat.is_valid():
    chat.save()
  else:
    return chat.errors

@csrf_exempt
def creditsPaymentCheck(request):
  request = json.loads(request.body.decode('utf-8'))
  payment_key = []
  patient = models.PatientMaster.objects.filter(Q(unique_health_n_key=request['patient_n_key']))
  if not patient:
    return HttpResponse(json.dumps({'status':"Patient Details Not Found"}),content_type='application/json')
  payment = models.AppPaymentDetails.objects.filter(Q(patient_n_key=patient[0].patient_n_key) & Q(payment_status__in=['Completed','Payment Success'])).values('total_session','app_payment_n_key','payment_status','payment_details','product')
  for i in payment:
    payment_key.append(i['app_payment_n_key'])
  if len(payment_key) > 0 :
    return HttpResponse(json.dumps({'status':'success','data':payment_key}),content_type='application/json')
  return HttpResponse(json.dumps({'status':'No credits available to continue add credits'}),content_type='application/json')


def CashFreeHeaders():
  headers = {
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
    }
  return headers

class CreatePaymentLink(APIView):
  def post(self, request):
    request = json.loads(request.body.decode('utf-8'))
    headers = CashFreeHeaders()
    orderId='Cure'+str(uuid.uuid1().int)[-8:]
    returnUrl = 'https://caremehealth.synapstics.com/paymentstatus'
    if 'returnUrl' in request:
      returnUrl = request['returnUrl']
    data = {
      'appId': settings.CASHFREE_APPID,
      'secretKey': settings.CASHFREE_SECRET,
      'orderId': orderId,
      'orderAmount': request['orderAmount'],
      'orderNote': 'Mrecs Product',
      'customerName': request['customerName'],
      'customerPhone': request['customerPhone'],
      'customerEmail': request['customerEmail'],
      'returnUrl': settings.CASHFREE_RETURN_URL,
      'notifyUrl':'',
      'paymentModes': '',
      'pc':''
    }
    response = requests.post('https://test.cashfree.com/api/v1/order/create', headers=headers, data=data)
    response = json.loads(response.text)
    if response['status'] == 'OK':
      link = response['paymentLink']
      # PaymentHistoryPost(orderId,request)
      return HttpResponse(json.dumps({'status':'success','data':link,'order_id':orderId}), content_type="application/json")
    return HttpResponse(json.dumps({'status':'failed','data':'Error','order_id':None}), content_type="application/json")

from rest_framework import serializers as serializers_rest
@csrf_exempt
def CashfreeStatus(request):
  request = json.loads(request.body.decode('utf-8'))
  headers = CashFreeHeaders()
  data = {
    'appId': settings.CASHFREE_APPID,
    'secretKey': settings.CASHFREE_SECRET,
    'orderId': request['order_id']
  }
  response = requests.post('https://test.cashfree.com/api/v1/order/info/status', headers=headers, data=data)
  response = json.loads(response.text)
  if response['txStatus'] == 'SUCCESS':
    history = PaymentHistoryPost(request)
    pricing = PaymentPricingPost(request)
  return HttpResponse(json.dumps({'status':'success','data':response}), content_type="application/json")

@csrf_exempt
def PaymentHistory(request):
  request = json.loads(request.body.decode('utf-8'))
  return_data = []
  pricing = models.MdPaymentHistory.objects.filter(Q(org_n_key=request['org_n_key'])).values('org_n_key','product_name','currentplan_amount','order_id','paid_amount','discount_amount','payment_date')
  for i in pricing:
    i['payment_date'] = i['payment_date'].strftime('%d/%m/%Y')
    i['paid_amount'],i['currentplan_amount'],i['discount_amount'] = str(i['paid_amount']),str(i['currentplan_amount']),str(i['discount_amount'])
    return_data.append(i)
  return HttpResponse(json.dumps({'status':'success','payment_history':return_data,'current_plan':ORGcurrentPlan(request['org_n_key'],'All')}), content_type="application/json")

def PaymentHistoryPost(request):
  request['created_on'] = DefaultTimeZone()
  request['status'] = 'Payment Success'
  request['payment_date'] = request['created_on']
  history = serializer1.MdPaymentHistorySerializer(data=request)
  if history.is_valid():
    history.save()
    return ({'status':'success','data':history.data})
  else:
    # return ({'status':'failed','data':history.errors})
    raise serializers_rest.ValidationError(history.errors)

def PaymentPricingPost(request):
  current = datetime.datetime.now()
  pricing = models.MdPaymentPricing.objects.filter(Q(org_n_key=request['org_n_key'])&Q(product_name=request['product_name']))
  add_days = 30 if request['subscrib_type'] == 'month' else 365 if request['subscrib_type'] == 'year' else 7
  if pricing:
    expire_date = pricing[0].expire_date + datetime.timedelta(days=add_days)
    request['modified_on'] = DefaultTimeZone()
    pricing.update(expire_date=expire_date,modified_on=request['modified_on'],current_plan=request['current_plan'],subscrib_type=request['subscrib_type'],modified_by_id=request['created_by_id'],modified_by_name=request['created_by_name'])
  else:
    request['created_on'] = DefaultTimeZone()
    request['status'] = 'Payment Success'
    request['expire_date'] = current.date() + datetime.timedelta(days=add_days)
    history = serializer1.MdPaymentPricingSerializer(data=request)
    if history.is_valid():
      history.save()
      return ({'status':'success','data':history.data})
    else:
      # return ({'status':'failed','data':history.errors})
      raise serializers_rest.ValidationError(history.errors)


def ORGcurrentPlan(org_n_key,product_name):
  alldata = []
  if product_name == 'All':
    pricing = models.MdPaymentPricing.objects.filter(Q(org_n_key=org_n_key)).values('current_plan','product_name','expire_date','subscrib_type')
  else:
    pricing = models.MdPaymentPricing.objects.filter(Q(org_n_key=org_n_key)&Q(product_name=product_name)).values('current_plan','product_name','expire_date','subscrib_type')
  if pricing:
    for i in pricing:
      current = datetime.datetime.now().date()
      i['expired_day'] = (i['expire_date'] - current).days if (i['expire_date'] - current).days >0 else 0
      i['expire_date'] = i['expire_date'].strftime('%d %b %Y')
      i['subscrib_type'] = i['subscrib_type'].capitalize() if i['subscrib_type'] == 'trial' else 'Plan'
      alldata.append(i)
  return alldata

def DateConversion(temp_date,types):
  if types == 'str_date':
    return datetime.datetime.strptime(temp_date,'%Y-%m-%d').date()
  if types == 'str_timestamp':
    return datetime.datetime.strptime(temp_date,'%Y-%m-%d %H:%M:%S').date()
  return 'failed'
  
@csrf_exempt
def Billing_Session_Report(request):
  # request = {}
  # request['fromdate']=data.GET.get('fromdate', None)
  # request['todate']=data.GET.get('todate', None)
  # request['hospital_n_key']=data.GET.get('hospital_n_key', 'CAR-HOS-1')
  # request['org_n_key']=data.GET.get('org_n_key', 'ORGID-1')
  # request['return_type']=data.GET.get('return_type', 'pdf')

  request = json.loads(request.body.decode('utf-8'))
  alldata = []
  session_filter = Q(hospital_n_key=request['hospital_n_key'])
  payment_filter = Q()
  if 'doc_app_id' in request and request['doc_app_id'] != None and request['doc_app_id'] != '':
    session_filter &= Q(doc_app_id=request['doc_app_id'])
  if 'patient_n_key' in request and request['patient_n_key'] != None:
    session_filter &= Q(patient_n_key=request['patient_n_key'])
  if 'uhid' in request and request['uhid'] != None:
    patient = models.PatientMaster.objects.filter(Q(unique_health_n_key=request['uhid']))
    session_filter &= Q(patient_n_key=patient[0].patient_n_key)
  if 'app_prod_n_key' in request and request['app_prod_n_key'] != None:
    session_filter &= Q(app_prod_n_key=request['app_prod_n_key'])
  if 'payment_id' in request and request['payment_id'] != None:
    session_filter &= Q(payment_details=request['payment_id'])
  payment = []
  query = models.AppSessionDetails.objects.filter(session_filter).distinct().values('app_payment_n_key')
  if query:
    payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key__in=query)&Q(payment_status='Completed')).values('app_payment_n_key','total_session','patient_n_key','appointment_n_key','app_prod_n_key','amount','payment_details','created_on','product_amount','discount','discount_amount','product','split_session')
  if 'fromdate' in request and request['fromdate'] != None:
    payment |= models.AppPaymentDetails.objects.filter(Q(product='Chat Therapy')&Q(payment_status='Completed')&Q(org_n_key=request['org_n_key'])&Q(created_on__range=(request['fromdate'],request['todate']))).values('app_payment_n_key','total_session','patient_n_key','appointment_n_key','app_prod_n_key','amount','payment_details','created_on','product_amount','discount','discount_amount','product','split_session')
    for k in list(payment):
      created = (k['created_on']).split(',')
      check_created_on = False
      # print(k['app_payment_n_key'])
      for l in created:
        if DateConversion(request['fromdate'],'str_date') <= DateConversion(l,'str_timestamp') <= DateConversion(request['todate'],'str_date'):
          check_created_on = True
      if not check_created_on:
        payment = payment.exclude(app_payment_n_key=k['app_payment_n_key'])
  alldata = BillingDataConversionCareMe(payment)
  for index,x in enumerate(list(alldata)):
    if 'fromdate' in request and request['fromdate'] != None:
      if DateConversion(request['fromdate'],'str_date') <= DateConversion(x['created_on'],'str_timestamp') <= DateConversion(request['todate'],'str_date'):
        pass
      else:
        alldata.remove(x)
  if request['return_type'] != 'pdf':
    alldata = json.dumps(alldata, default = decimal_default)
    return HttpResponse(json.dumps({'status':'success','data':json.loads(alldata)}), content_type="application/json")
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="CareMe_Billing.csv"'
  fieldnames = ['SNo','UHID','PatientName','Phone Number','Patient Type','Payment Id','Product Name','Payment Done Date','Amount Paid','TotalSession','PerSession','PerSession Cost']
  filewriter = csv.DictWriter(response,fieldnames=fieldnames)
  filewriter.writeheader()
  s_no = 0
  for j in alldata:
    j['last_name'] = '' if j['last_name'] == None else j['last_name']
    if j != {}:
      s_no += 1
      filewriter.writerow({'SNo':s_no,'UHID':j['unique_health_n_key'],'PatientName':j['first_name']+' '+j['last_name'],'Phone Number':j['phone_number'],'Patient Type':j['patient_type'],'Payment Id':j['payment_details'],'Product Name':j['product'],'Payment Done Date':j['created_on'],'Amount Paid':j['amount'],'TotalSession':j['total_session'],'PerSession':j['split_session'],'PerSession Cost':j['per_session_cost']})
    else:
      filewriter.writerow({})
  return response


def BillingDataConversionCareMe(payment):
  alldata = []
  cursor = connection.cursor()
  database = connection.settings_dict['NAME']
  for i in payment:
    try:
      cursor.execute('''SELECT a.first_name,a.last_name,a.unique_health_n_key,a.phone_number,a.gender,c.first_name as 'doctor_name' from '''+str(database)+'''.ge_patient_master as a INNER JOIN '''+str(database)+'''.ge_appointment_master as b INNER JOIN '''+str(database)+'''.md_employees_master as c where a.patient_n_key="'''+i['patient_n_key']+'''" AND b.appointment_n_key="'''+i['appointment_n_key']+'''" AND b.doc_app_id=c.employee_n_key''')
      check_in = dictfetchall(cursor)
      temp_data = {**i, **check_in[0]}
      session = models.AppSessionDetails.objects.filter(Q(app_payment_n_key=i['app_payment_n_key']))
      amount = (i['amount']).split(',')
      payment_details = (i['payment_details']).split(',')
      created_on = (i['created_on']).split(',')
      product_amount = (i['product_amount']).split(',')
      discount_amount = (i['discount_amount']).split(',')
      discount = (i['discount']).split(',')
      split_session = i['split_session'] if i['split_session'] != None and i['split_session'] != '' else []
      for index,k in enumerate(amount):
        temp_data['total_session'] = temp_data['total_session'] #if index == 0 else ''
        temp_data['completed'] = session.count() #if index == 0 else ''
        temp_data['pending'] = int(i['total_session']) - temp_data['completed'] #if index == 0 else ''
        temp_data['product'] = temp_data['product']
        temp_data['patient_type'] = 'New' if index == 0 else 'Followup'
        temp_data['amount'],temp_data['payment_details'],temp_data['created_on'],temp_data['product_amount'],temp_data['discount_amount'],temp_data['discount'] = k,payment_details[index],created_on[index],product_amount[index],discount_amount[index],discount[index]
        temp_data['split_session'] = split_session[index] if split_session != [] and len(split_session)>=index+1 else str(i['total_session'])+"/Old"
        temp_data['per_session_cost'] = int(temp_data['amount'])/int(temp_data['split_session']) if isinstance(temp_data['split_session'], int) else ''
        alldata.append(temp_data.copy())
    except Exception as e:
      pass
      print("passed",i['appointment_n_key'],e)
  return alldata

@csrf_exempt
def BillAppointmentWiseReport(request):
  request = json.loads(request.body.decode('utf-8'))
  session_filter = ~Q(overall_status='Register')
  if 'doc_app_id' in request and request['doc_app_id'] != None and request['doc_app_id'] != '':
    session_filter &= Q(doc_app_id=request['doc_app_id'])
  if 'fromdate' in request and request['fromdate'] != None:
    session_filter &= Q(appointment_date__range=(request['fromdate'],request['todate']))
  if 'patient_n_key' in request and request['patient_n_key'] != None:
    session_filter &= Q(patient_n_key=request['patient_n_key'])
  if 'uhid' in request and request['uhid'] != None:
    patient = models.PatientMaster.objects.filter(Q(unique_health_n_key=request['uhid']))
    session_filter &= Q(patient_n_key=patient[0].patient_n_key)

  payment = []
  appoint = list(models.AppointmentMaster.objects.filter(session_filter).distinct().values_list('appointment_n_key',flat=True))
  session = models.AppSessionDetails.objects.filter(appointment_n_key__in=appoint).values('app_payment_n_key','appointment_n_key','patient_n_key','doc_app_id','app_prod_n_key','payment_details')
  for i in session:
    if i['appointment_n_key'] in appoint:
      appoint.remove(i['appointment_n_key'])
  bill = BillingAppointmentsCareMe(session)
  alldata = bill['alldata']
  if request['return_type'] != 'pdf':
    alldata = json.loads(json.dumps(alldata, default = decimal_default))
    return_data = []
    for x in alldata:
      return_data+=x
    return HttpResponse(json.dumps({'status':'success','data':return_data}), content_type="application/json")
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="CareMe_Appointments.csv"'
  fieldnames = ['SNo','FullName','UHID','PhoneNumber','EncounterId','AppointmentType','AppointmentDate','AppointmentTime','TherapistName','PaymentID','PaymentDoneDate','TotalAmountPaid','PersessionCost','TotalSession','Completed','Pending','AppointmentStatus','AppointmentComment','ProductType','AppointmentCancellationDate','Recommended']
  filewriter = csv.DictWriter(response,fieldnames=fieldnames)
  filewriter.writeheader()
  s_no = 0
  for j in alldata:
    s_no += 1 
    filewriter.writerow({'SNo':s_no,'FullName':j['first_name']+' '+j['last_name'] if j['last_name'] != None else j['first_name'],'UHID':j['unique_health_n_key'],'PhoneNumber':j['phone_number'],'EncounterId':j['encounter_id'],'AppointmentType':j['appointment_type'],'AppointmentDate':j['appointment_date'],'AppointmentTime':j['appointment_time'],'TherapistName':j['therapist_name'],'PaymentID':j['payment_id'],'PaymentDoneDate':j['payment_date'],'TotalAmountPaid':j['amount_paid'],'PersessionCost':j['invoice'],'TotalSession':j['total_session'],'Completed':j['completed'],'Pending':j['pending'],'AppointmentStatus':j['overall_status'],'AppointmentComment':j['comments'],'ProductType':j['product'],'AppointmentCancellationDate':j['cancelled_date_time'],"Recommended":j['recommended']})
  appoint = set(appoint+bill['except_data'])
  for k in appoint:
    s_no += 1
    cursor = connection.cursor()
    database = connection.settings_dict['NAME'] 
    cursor.execute('''SELECT SUM(d.total_sessions_recommended) as recommended,a.encounter_id,a.patient_type,a.appointment_date,a.appointment_time,a.overall_status,a.chief_complaints,a.cancelled_reason,a.noshow_reason,a.left_without_seen_reason,a.reschedule_reason,a.cancelled_date_time,b.first_name,b.last_name,b.unique_health_n_key,b.phone_number,c.first_name as therapist_name from '''+str(database)+'''.ge_appointment_master as a inner join '''+str(database)+'''.ge_patient_master as b inner join '''+str(database)+'''.md_employees_master as c inner join '''+str(database)+'''.app_therapy_journey as d where a.appointment_n_key ="'''+k+'''" AND a.patient_n_key=b.patient_n_key AND a.doc_app_id=c.employee_n_key AND b.patient_n_key=d.patient_n_key''')
    details_query = dictfetchall(cursor)
    pat = details_query[0]
    chief_complaints = '\nchief - {}'.format(pat['chief_complaints']) if pat['chief_complaints'] != None and pat['chief_complaints'] != '' else ''
    cancelled_reason = '\ncancel - {}'.format(pat['cancelled_reason']) if pat['cancelled_reason'] != None and pat['cancelled_reason'] != '' else ''
    noshow_reason = '\nnoshow - {}'.format(pat['noshow_reason']) if pat['noshow_reason'] != None and pat['noshow_reason'] != '' else ''
    left_without_seen_reason = '\nleft - {}'.format(pat['left_without_seen_reason']) if pat['left_without_seen_reason'] != None and pat['left_without_seen_reason'] != '' else ''
    reschedule_reason = '\nreschedule - {}'.format(pat['reschedule_reason']) if pat['reschedule_reason'] != None and pat['reschedule_reason'] != '' else ''
    pat['comments'] = chief_complaints + cancelled_reason + noshow_reason + left_without_seen_reason + reschedule_reason
    filewriter.writerow({'SNo':s_no,'FullName':pat['first_name']+' '+pat['last_name'] if pat['last_name'] != None else pat['first_name'],'UHID':pat['unique_health_n_key'],'PhoneNumber':pat['phone_number'],'EncounterId':pat['encounter_id'],'AppointmentType':pat['patient_type'],'AppointmentDate':pat['appointment_date'],'AppointmentTime':pat['appointment_time'],'TherapistName':pat['therapist_name'],'AppointmentStatus':pat['overall_status'],'AppointmentComment':pat['comments'],'AppointmentCancellationDate':pat['cancelled_date_time'],"Recommended":pat['recommended']})
  return response

def BillingAppointmentsCareMe(session):
  alldata = []
  except_data = []
  cursor = connection.cursor()
  database = connection.settings_dict['NAME']
  for i in session:
    try:
      payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key=i['app_payment_n_key'])).values('app_payment_n_key','total_session','patient_n_key','amount','product','split_session','invoice','invoice_discount','discount_amount','payment_details','created_on')
      overall_session = models.AppSessionDetails.objects.filter(Q(app_payment_n_key=i['app_payment_n_key']))
      cursor.execute('''SELECT SUM(d.total_sessions_recommended) as recommended, a.appointment_n_key,a.patient_n_key,a.encounter_id,a.patient_type,a.reschedule_reason,a.appointment_date,a.appointment_time,a.doc_app_id,a.overall_status,a.cancelled_date_time,a.chief_complaints,a.cancelled_reason,a.noshow_reason,a.left_without_seen_reason,a.reschedule_reason,b.first_name,b.last_name,b.unique_health_n_key,b.phone_number,c.first_name as therapist_name from '''+str(database)+'''.ge_appointment_master as a inner join '''+str(database)+'''.ge_patient_master as b inner join '''+str(database)+'''.md_employees_master as c inner join '''+str(database)+'''.app_therapy_journey as d where a.appointment_n_key ="'''+i['appointment_n_key']+'''" AND a.patient_n_key=b.patient_n_key AND a.doc_app_id=c.employee_n_key AND b.patient_n_key=d.patient_n_key''')
      details_query = dictfetchall(cursor)
      temp_data = {**payment[0],**details_query[0],**i}
      list_pay = payment[0]['payment_details'].split(',')
      invoice = payment[0]['invoice'].split(',')
      temp_data['payment_date'], temp_data['amount_paid'] = '',''
      if i['payment_details'] != None and i['payment_details'] != '':
        index = list_pay.index(i['payment_details'])
        temp_data['payment_date'] = payment[0]['created_on'].split(',')[index]
        temp_data['amount_paid'] = payment[0]['amount'].split(',')[index]
      temp_data['completed'] = overall_session.count()
      temp_data['pending'] = int(temp_data['total_session']) - temp_data['completed']
      temp_data['payment_id'] = i['payment_details']
      session = list(overall_session.values_list('appointment_n_key',flat=True))
      session_index = session.index(i['appointment_n_key'])
      temp_data['appointment_type'] = 'New Patient' if i['appointment_n_key'] == session[0] else 'FollowUp'
      temp_data['invoice'] = invoice[session_index]
      chief_complaints = '\nchief - {}'.format(temp_data['chief_complaints']) if temp_data['chief_complaints'] != None and temp_data['chief_complaints'] != '' else ''
      cancelled_reason = '\ncancel - {}'.format(temp_data['cancelled_reason']) if temp_data['cancelled_reason'] != None and temp_data['cancelled_reason'] != '' else ''
      noshow_reason = '\nnoshow - {}'.format(temp_data['noshow_reason']) if temp_data['noshow_reason'] != None and temp_data['noshow_reason'] != '' else ''
      left_without_seen_reason = '\nleft - {}'.format(temp_data['left_without_seen_reason']) if temp_data['left_without_seen_reason'] != None and temp_data['left_without_seen_reason'] != '' else ''
      reschedule_reason = '\nreschedule - {}'.format(temp_data['reschedule_reason']) if temp_data['reschedule_reason'] != None and temp_data['reschedule_reason'] != '' else ''
      temp_data['comments'] = chief_complaints + cancelled_reason + noshow_reason + left_without_seen_reason + reschedule_reason
      alldata.append(temp_data)
    except Exception as e:
      # print("passed",i['appointment_n_key'],e)
      except_data.append(i['appointment_n_key'])
      pass
  return {'alldata':alldata,'except_data':except_data}


def render_to_pdf(template_src, context_dict):
  template = get_template(template_src)
  html  = template.render(context_dict)
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
  if not pdf.err:
    return HttpResponse(result.getvalue(), content_type='application/pdf')
  return None


@csrf_exempt
def OrganisationInvoice(request):
  data1 = json.loads(request.body.decode('utf-8'))
  alldata = []
  pricing = models.MdPaymentHistory.objects.filter(Q(org_n_key= data1['org_n_key'])).values('product_name','currentplan_amount','paid_amount','payment_date','gst','order_id')
  org_details = models.OrganizationMaster.objects.filter(Q(org_n_key=data1['org_n_key'])).values('organization_id','org_name','email','phone_num')
  for i in pricing:
    i['payment_date'] = i['payment_date'].strftime('%d/%m/%Y')
    i['paid_amount'],i['currentplan_amount'],i['order_id'] = str(i['paid_amount']),str(i['currentplan_amount']),str(i['order_id'])
    if i['gst'] == None:
      i['gst'] = 0
    alldata.append(i)
  for j in org_details:
    j['organization_id'],j['phone_num'],j['organization_id'] = str(j['organization_id']),str(j['phone_num']),str(j['organization_id'])
  template = get_template('organisationinvoice.html')
  context = {'Order_number':i['order_id'],'org_name':j['org_name'],'email':j['email'],'phone_num':j['phone_num'],'organization_number':j['organization_id'],'invoice_date': i['payment_date'],'data':alldata}
  html = template.render(context)
  pdf = render_to_pdf('organisationinvoice.html', context)
  if pdf:
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "OrganisationInvoice.pdf"
    content = "inline; filename='%s'" %(filename)
    download = request.GET.get("download")
    if download:
      content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response
  return HttpResponse("Not found")

@csrf_exempt
def UserLimitCheck(request):
  data1 = json.loads(request.body.decode('utf-8'))
  values = []
  planing = models.MdPaymentPricing.objects.filter(Q(org_n_key = data1['org_n_key'])).values('product_name','current_plan')
  for i in planing:
    user = models.EmployeesMaster.objects.filter(Q(org_n_key = data1['org_n_key'])&Q(product_name__icontains=i['product_name']))
    plan = models.PlanDetails.objects.filter(Q(product_name = i['product_name']))
    total = user.count()
    planz = plan[0].product_name
    if len(planz)>1:
      plans = plan[0].plan_name.split(',')
      limit = plan[0].employees.split(',')
      plan_name1 = plans.index(i['current_plan'])
      limitz = int(limit[plan_name1])
      limitz +=  limitz
      total += total
      values.append({'maximum_count':limitz,'total_user':total})
      if total <= limitz:
        return HttpResponse(json.dumps({'status':'success','maximum_count':limitz,'total_user':total}),content_type='application/json')  
      return HttpResponse(json.dumps({"status":"Failed",'maximum_count':limitz,'total_user':total}),content_type='application/json')
    elif len(planz) == 1:  
      plans = plan[0].plan_name.split(',')
      limit = plan[0].employees.split(',')
      plan_name1 = plans.index(i['current_plan'])
      limitz = int(limit[plan_name1])
      values.append({'maximum_count':limitz,'total_user':total})
      if total <= limitz:
        return HttpResponse(json.dumps({'status':'success','maximum_count':limitz,'total_user':total}),content_type='application/json')  
      return HttpResponse(json.dumps({"status":"Failed",'maximum_count':limitz,'total_user':total}),content_type='application/json')
@csrf_exempt
def SubscribedPlan(request):
  request = json.loads(request.body.decode('utf-8'))
  alldata = []
  plan = list(models.MdPaymentPricing.objects.filter(Q(org_n_key=request['org_n_key'])).values('product_name'))
  for i in plan:
    i['select']=True
  return HttpResponse(json.dumps({'status':'success','data':plan}),content_type='application/json')

@csrf_exempt
def GetBloodBankName(request):
  request = json.loads(request.body.decode('utf-8'))
  blood = list(models.BloodBank_Master.objects.filter(Q(org_n_key=request['org_n_key'])).values('bloodbank_n_key','bloodbank_name'))
  return HttpResponse(json.dumps({'status':'success','data':blood}),content_type='application/json')

@csrf_exempt
def Enable_Disable_Online_Practice(request):
  request = json.loads(request.body.decode('utf-8'))
  if request['hospital_n_key'] != None and request['hospital_n_key'] != '':
    hospital = models.HospitalMaster.objects.filter(Q(hospital_n_key=request['hospital_n_key']))
    if hospital:
      hospital.update(online_practice_status=request['online_practice_status'])
      return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
  if request['bloodbank_n_key'] != None and request['bloodbank_n_key'] != '':
    blood = models.BloodBank_Master.objects.filter(Q(bloodbank_n_key=request['bloodbank_n_key']))
    if blood:
      blood.update(online_practice_status=request['online_practice_status'])
      return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
  return HttpResponse(json.dumps({'status':'failed'}),content_type='application/json')



# Credit Availability Check 
@csrf_exempt
def FollowupCountCheck(request):
  request = json.loads(request.body.decode('utf-8'))
  payment_key = []
  patient = models.PatientMaster.objects.filter(Q(unique_health_n_key=request['unique_health_n_key']))
  if not patient:
    return HttpResponse(json.dumps({'status':"Patient Details Not Found"}),content_type='application/json')
  patient_data = list(patient.values('patient_n_key','unique_health_n_key','phone_number'))
  patient_data[0]['phone_number'] = str(patient_data[0]['phone_number'])
  patient_data[0]['patient_name'] = patient[0].full_name
  payment = models.AppPaymentDetails.objects.filter(Q(patient_n_key=patient[0].patient_n_key) & Q(payment_status__in=['Completed','Payment Success'])&~Q(app_prod_n_key='APP_PROD-0')).values('total_session','app_payment_n_key','payment_status','payment_details','product')
  for i in payment:
    session = models.AppSessionDetails.objects.filter(Q(app_payment_n_key=i['app_payment_n_key']))
    if int(i['total_session']) > session.count():
      paymentdetails = i['payment_details'].split(',')
      payment_key.append({"app_payment_n_key":i['app_payment_n_key'],"payment_details":paymentdetails[-1],"product":i['product']})
  if len(payment_key) > 0 :
    return HttpResponse(json.dumps({'status':'success',"payment_details":payment_key,"patient_details":patient_data}),content_type='application/json')
  return HttpResponse(json.dumps({'status':'No credits available to continue add credits'}),content_type='application/json')


# Book Appointment 
@csrf_exempt
def CareTeam_Book_Appointment(request):
  request = json.loads(request.body.decode('utf-8'))
  payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
  if not payment:
    return HttpResponse(json.dumps({'status':'failed','data':'No Payment Details Found'}), content_type="application/json")
  overall_session = models.AppSessionDetails.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
  if len(overall_session) >= int(payment[0].total_session):
    return HttpResponse(json.dumps({'status':'failed','data':'All Sessions are Completed'}), content_type="application/json")
  current_time = TimeZoneConvert(request['hospital_n_key'])
  # request['app_prod_n_key'] = payment[0].app_prod_n_key
  request['service_name'] = payment[0].product
  request['patient_type']='Followup' if payment[0].appointment_n_key != None and payment[0].appointment_n_key != '' else 'New Patient'
  request['overall_status'] = 'Scheduled'
  request['colour'] = '#eb519eff'
  request['appointment_name'] = 'TeleHealth'
  request['payment_type'] = 'with payment'
  request['created_on'] = current_time
  request['choose_by_mode'] = 'Therapist'
  appoint = serializer1.AppointmentMasterSerializer(data = request)
  if appoint.is_valid():
    appoint.save()
    request['appointment_n_key'] = appoint.data['appointment_n_key']
    if payment[0].appointment_n_key == None or payment[0].appointment_n_key == '' or len(overall_session)==0:
      paymet_update = UpdatePaymentDetails(request,payment)
    session = SessionDetailsPost(request,len(overall_session),payment)
    create_meeting = video.generate_meetingid(request,appoint.data['appointment_n_key'])
    try:
      bill = session_service_pay(appoint.data['appointment_n_key'],request,overall_session,payment)
    except Exception as e:
      pass
    tele_chat = TeleHealthChat(appoint.data['appointment_n_key'],request)
    return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({'status':'failed','data':appoint.errors}), content_type="application/json")


# Tele Health Chat
def TeleHealthChat(app_n_key,data):
  data['type_of_chat'] = 'TeleHealth'
  data['employee_n_key'] = [data['doc_app_id']]
  data['modified_on'] = data['created_on']
  data['channelid'] = app_n_key
  data['end_date'] = data['appointment_date']+' '+data['appointment_end_time']
  chat_data = serializer1.ChatHistorySerializer(data=data)
  if chat_data.is_valid():
    chat_data.save()
    return 'success'
  else:
    return chat_data.errors

# Method Payment Table Update for Initial
def UpdatePaymentDetails(request,payment):
  single_paid = round(float(payment[0].amount)/int(payment[0].total_session),2)
  single_discount = round(float(payment[0].discount)/int(payment[0].total_session),2)
  invoice,invoice_discount,doctors = [],[],[]
  for j in range(int(payment[0].total_session)):
    invoice.append(str(single_paid))
    invoice_discount.append(str(single_discount))
    doctors.append(request['doc_app_id'])
  payment.update(appointment_n_key=request['appointment_n_key'],payment_status='Completed',invoice=",".join(invoice),doctors=",".join(doctors),invoice_discount=",".join(invoice_discount))
  return 'success'

# Method Session Table Post
def SessionDetailsPost(request,count,payment):
  request['status'] = 'Scheduled'
  request['app_prod_n_key'] = payment[0].app_prod_n_key
  payment_id = payment[0].payment_details.split(',')
  request['payment_details'] = payment_id[-1]
  try:
    if 'app_payment_n_key' in request:
      payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
      payment_details = (payment[0].payment_details).split(',') if payment[0].payment_details != None and payment[0].payment_details != '' else []
      split_session = []
      if payment[0].split_session != None and payment[0].split_session != '':
        session = payment[0].split_session
        for index,i in enumerate(payment_details):  
          split_session.extend(repeat(i,session[index]))
      else:
        session = [payment[0].total_session]
        split_session.extend(repeat(payment_details[-1],int(session[0])))
      request['payment_details'] = split_session[count]
  except Exception as e:
    pass
  serializer = serializer1.AppSessionDetailsSerializer(data = request)
  if serializer.is_valid():
    serializer.save()
    return serializer.data
  else:
    return serializer.errors

# Calendar Billing For Appointments
def session_service_pay(appointment_n_key,request,overall_session,payment):
  appoint = models.AppointmentMaster.objects.filter(Q(appointment_n_key = appointment_n_key))
  doct = models.EmployeesMaster.objects.filter(Q(employee_n_key=appoint[0].doc_app_id))
  patient = models.PatientMaster.objects.filter(Q(patient_n_key=request['patient_n_key']))
  if request['app_prod_n_key'] == 'APP_PROD-0':
    chat_product = (payment[0].product_amount).split(',')
    chat_amount = (payment[0].amount).split(',')
    chat_discount = (payment[0].discount_amount).split(',')
    single_product = chat_product[-1]
    single_paid = chat_amount[-1]
    single_discount = chat_discount[-1]
    # single_product = round(float(request['product_amount']) ,2)
    # single_paid = round(float(request['amount']) ,2)
    # single_discount = round(float(request['discount_amount']) ,2)
  else:
    current = len(overall_session)
    pay_invoice = (payment[0].invoice).split(',')
    pay_invoice_dis = (payment[0].invoice_discount).split(',')
    single_product = 1499
    single_paid = float(pay_invoice[current])
    single_discount = float(pay_invoice_dis[current])
  discount = 100 * (single_product - single_paid) / single_product
  inv_payments = {
    "appointment_n_key":appoint[0].appointment_n_key,
    "encounter_id":appoint[0].encounter_id,
    "billing_date":datetime.datetime.today().date(),
    "due_date":appoint[0].appointment_date,
    "org_n_key":appoint[0].org_n_key,
    "product_name":payment[0].product,
    "quantity":1,
    "rate":None,
    "amount":single_product,
    "tax":0,
    "central_tax":0,
    "state_tax":0,
    "sub_total":single_paid,
    "tax_amount":0,
    "taxperone":0,
    "doctor_name":doct[0].first_name + " " + doct[0].last_name,
    "doctor_share":0,
    "s_discount":discount,
    "s_dis_amt":single_discount,
    "d_amt":0,
    "d_discount":0,
    "d_dis_amt":0,
    "h_amt":single_paid,
    "h_discount":0,
    "h_dis_amt":0,
    "created_by_id":appoint[0].doc_app_id,
    "created_by_name":doct[0].first_name,
    "created_on":request['created_on'],
    "patient_name":patient[0].full_name,
    "patient_n_key":patient[0].patient_n_key,
    "hospital_n_key":appoint[0].hospital_n_key,
    "inclusive_of_tax":"Yes",
    "finalized":"Yes",
    "product_amount":single_product,
    "app_payment_n_key":request['app_payment_n_key']
  }
  serializer = serializer1.InvoiceBillPaymentSerializer(data=inv_payments)   
  if serializer.is_valid():
    serializer.save()
  else:
    # print(serializer.errors)
    return(serializer.errors)

  invoice_no = serializer.data['invoice_no']
  inv_details={
    "invoice_no":invoice_no,
    "patient_n_key":patient[0].patient_n_key,
    "hospital_n_key":appoint[0].hospital_n_key,
    "encounter_id":appoint[0].encounter_id,
    "org_n_key":appoint[0].org_n_key,
    "appointment_n_key":appoint[0].appointment_n_key,
    "patient_name":patient[0].first_name,
    "status":'Paid',
    "debit_amt":0,
    "cash_amt":0,
    "credit_amt":single_paid,
    "cheque_amt":0,
    "write_off_amount":0,
    "advance_used":0,
    "balance_amount":0,
    "created_by_id":appoint[0].doc_app_id,
    "created_by_name":doct[0].first_name,
    "created_on":request['created_on']
  }
  summary = serializer1.InvoiceBillDetailsSerializer(data=inv_details)
  if summary.is_valid():
    summary.save()
    # print("payment_saved")
    return summary.data
  else:
    return summary.errors


def RenewChatTherapy(request):
  payment = models.AppPaymentDetails.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
  if payment:
    amount = payment[0].amount.split(',')
    app_prod = payment[0].product_amount.split(',')
    app_dis = payment[0].discount.split(',')
    app_dis_amt = payment[0].discount_amount.split(',')
    payment_details = payment[0].payment_details.split(',')
    split_session = payment[0].split_session if payment[0].split_session != None else [int(payment[0].total_session)]
    product = models.AppProductDetails.objects.filter(Q(app_prod_n_key=request['app_prod_n_key']))
    plan_a,plan_b,plan_c = json.loads(product[0].plan_a),json.loads(product[0].plan_b),json.loads(product[0].plan_c)
    plan = [int(plan_a['amount']),int(plan_b['amount']),int(plan_c['amount'])]
    request['product_amount'] = min(plan, key=lambda x:abs(x-int(request['total_session'])))
    request['discount'] = round((100*(request['product_amount'] - int(request['amount'])) / request['product_amount']),2)
    request['discount_amount'] = request['product_amount'] - int(request['amount'])
    
    amount.append(request['amount'])
    app_prod.append(str(request['product_amount']))
    app_dis_amt.append(str(request['discount_amount']))
    app_dis.append(str(request['discount']))
    payment_details.append(request['payment_details'])
    split_session.append(int(request['total_session']))
    created_on = payment[0].created_on+","+request['created_on']
    bought_session = int(payment[0].total_session) + int(request['total_session'])
    payment.update(payment_details=",".join(payment_details),total_session=bought_session,created_on=created_on,amount=",".join(amount),product_amount=",".join(app_prod),discount=",".join(app_dis),discount_amount=",".join(app_dis_amt),split_session=split_session)
    renew = RenewChatAppoint(request,payment)
    return renew
  return {'status':'failed'}

def RenewChatAppoint(request,payment):
  current = datetime.datetime.strptime(request['created_on'],'%Y-%m-%d %H:%M:%S')
  chat = models.ChatHistory.objects.filter(Q(app_payment_n_key=request['app_payment_n_key']))
  current = chat[0].end_date if current < chat[0].end_date else current
  last_appoint = list(models.AppointmentMaster.objects.filter(Q(appointment_n_key=chat[0].channelid)).values('patient_n_key','service_name','overall_status','colour','appointment_name','payment_type','doc_app_id','created_by_id','created_by_name'))
  data = dict(request)
  data.update(last_appoint[0])
  data['patient_type'] = 'FollowUp'
  data['appointment_date'] = current.date()
  data['appointment_time'] = current.time()
  data['appointment_end_time'] = current.time()
  chat_end = current + relativedelta(days=int(request['total_session']))
  chat.update(end_date=chat_end)
  appoint = serializer1.AppointmentMasterSerializer(data = data)
  if appoint.is_valid():
    appoint.save()
    ret_appoint = models.AppointmentMaster.objects.filter(Q(appointment_n_key=appoint.data['appointment_n_key']))
    ret_data = serializer1.AppointmentSortSerializer(ret_appoint,many=True).data
    ret_data = ret_data[0]
    request['appointment_n_key']=appoint.data['appointment_n_key']
    try:
      invoice = session_service_pay(appoint.data['appointment_n_key'],request,request['total_session'],payment)
    except Exception as e:
      pass
    return {'status':'success','data':{}} 
  else:
    return {'status':'failed','data':appoint.errors}  

@csrf_exempt
def PatientUhid(request):
  data = json.loads(request.body.decode('utf-8'))
  pat_data = []
  patient = models.PatientMaster.objects.filter(Q(unique_health_n_key=data['uhid']))
  if patient:
    pat_data = list(patient.values('patient_n_key','phone_number','unique_health_n_key'))
    pat_data[0]['full_name'] = patient[0].full_name
    pat_data[0]['phone_number'] = str(patient[0].phone_number)
  return HttpResponse(json.dumps({'status':'success','data':pat_data}), content_type="application/json")

@csrf_exempt
def PatientDateReport(request):
  data = json.loads(request.body.decode('utf-8'))
  alldata = []
  app_filter = Q(hospital_n_key=data['hospital_n_key'])
  if 'uhid' in data and data['uhid'] != None and data['doc_app_id'] != '':
    app_filter &= Q(patient_n_key__unique_health_n_key=data['uhid'])
  if 'registration_fromdate' in data and data['registration_fromdate'] != None:
    app_filter &= Q(patient_n_key__registration_date__range=(data['registration_fromdate'],data['registration_todate']))
  if 'doc_app_id' in data and data['doc_app_id'] != None:
    app_filter &= Q(doc_app_id=data['doc_app_id'])
  patient_key = set(models.AppointmentMaster.objects.filter(app_filter).values_list('patient_n_key',flat=True))
  cursor = connection.cursor()
  database = connection.settings_dict['NAME']
  for k in patient_key:
    try:
      cursor.execute('''SELECT (SELECT COALESCE(SUM(total_session), 0) FROM '''+database+'''.app_payment_details where patient_n_key="'''+k+'''" AND app_prod_N_key !="APP_PROD-0" AND payment_status in ("Completed","Payment Success")) as total,
        (SELECT COALESCE(SUM(total_sessions_recommended), 0) FROM '''+database+'''.app_therapy_journey where patient_n_key="'''+k+'''") as recommended,
        (SELECT COUNT(patient_n_key) FROM '''+database+'''.ge_appointment_master where patient_n_key="'''+k+'''" and overall_status not in ('Register','Cancelled by patient','Cancelled by practitioner','No Show') AND appointment_name !="ChatTherapy") as completed,
        (SELECT appointment_date FROM '''+database+'''.ge_appointment_master where patient_n_key="'''+k+'''" and overall_status!='Register' ORDER BY appointment_id ASC LIMIT 1) as first_date,
        (SELECT appointment_date FROM '''+database+'''.ge_appointment_master where patient_n_key="'''+k+'''" and overall_status!='Register' ORDER BY appointment_id DESC LIMIT 1) as last_date,
        (SELECT doc_app_id FROM '''+database+'''.ge_appointment_master where patient_n_key="'''+k+'''" and overall_status!='Register' ORDER BY appointment_id DESC LIMIT 1) as doc_app_id,
        (SELECT b.product_title FROM '''+database+'''.app_payment_details AS a INNER JOIN '''+database+'''.app_product_details AS b WHERE patient_n_key ="'''+k+'''" AND a.app_prod_n_key=b.app_prod_n_key AND a.payment_status in ("Completed","Payment Success") ORDER BY a.app_payment_n_key DESC LIMIT 1) AS product,
        patient_n_key,unique_health_n_key,first_name,last_name,phone_number,email,registration_date from '''+database+'''.ge_patient_master where patient_n_key="'''+k+'''"''')
      details_query = dictfetchall(cursor)
      emp = models.EmployeesMaster.objects.filter(Q(employee_n_key=details_query[0]['doc_app_id']))
      today = datetime.datetime.now().date() - details_query[0]['last_date']
      details_query[0]['therapist_name']=emp[0].first_name
      details_query[0]['last_from_today']=today.days
      alldata.append(details_query[0])
    except Exception as e:
      pass
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="Patient Datewise Report.csv"'
  fieldnames = ['SNO','UHID','Patinet Name','Phone','Email','Registration Date','Therapist Name','Product','First Appoint Date','Last Appoint Date','Recommended','Purchased','Completed','Last From Today']
  filewriter = csv.DictWriter(response,fieldnames=fieldnames)
  filewriter.writeheader()
  s_no = 0
  for i in alldata:
    s_no += 1 
    filewriter.writerow({'SNO':s_no,'UHID':i['unique_health_n_key'],'Patinet Name':i['first_name']+' '+i['last_name'] if i['last_name'] != None else i['first_name'],'Phone':i['phone_number'],'Email':i['email'],'Registration Date':i['registration_date'],'Product':i['product'],'Therapist Name':i['therapist_name'],'First Appoint Date':i['first_date'],'Last Appoint Date':i['last_date'],'Recommended':i['recommended'],'Purchased':i['total'],'Completed':i['completed'],'Last From Today':i['last_from_today']})
  return response

@csrf_exempt
def AttendanceReport(request):
  data = json.loads(request.body.decode('utf-8'))
  alldata = []
  dates = []
  end_date = datetime.datetime.strptime(data['end_date'],"%Y-%m-%d").date()
  start_date = datetime.datetime.strptime(data['start_date'],"%Y-%m-%d").date()
  temp_start = start_date
  while (temp_start<=end_date):
    dates.append(str(temp_start))
    temp_start = temp_start + datetime.timedelta(days=1)
  doc_role = DoctorRoleQuery(data['org_n_key'])+['Physician']
  if 'employee_n_key' in data and data['employee_n_key'] != None:
    emp = models.EmployeesMaster.objects.filter(Q(org_n_key=data['org_n_key'])&Q(is_active=1)&Q(role__in=doc_role)&Q(employee_n_key=data['employee_n_key']))
  else:
    emp = models.EmployeesMaster.objects.filter(Q(role__in=doc_role))
  for i in emp:
    temp_dates = [{'name':i.first_name,'date':'','total':'','booked':'','total_hours':0,'utilized_hours':0}]
    temp_dates += [{'name':i.first_name,'date' : d,'total':'','booked':''} for d in dates]
    emp_working={'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0,'Sunday':0}
    working = models.DoctorWorkingDetails.objects.filter(Q(doctor_n_key=i.employee_n_key)).order_by('working_days')
    # special = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=i.employee_n_key)&Q(special_date__in=dates))
    for j in working:
      diff = (datetime.datetime.strptime(str(j.end_time), '%H:%M:%S') - datetime.datetime.strptime(str(j.start_time), '%H:%M:%S')).total_seconds()
      emp_working[j.working_days] += diff
    for k in dates:
      appoint = models.AppointmentMaster.objects.filter(Q(doc_app_id=i.employee_n_key)&Q(appointment_date=k)&~Q(overall_status__in=['Register','No Show','Cancelled by patient','Cancelled by practitioner'])&~Q(appointment_name=['ChatTherapy']))
      appoint_seconds = sum([(datetime.datetime.strptime(str(l.appointment_end_time), '%H:%M:%S') - datetime.datetime.strptime(str(l.appointment_time), '%H:%M:%S')).total_seconds() for l in appoint])
      appoint_hours=SecondsToHour(appoint_seconds)
      # print(appoint_hours)
      d = next(item for item in temp_dates if item['date'] == k)
      d['booked']=appoint_hours
      temp_dates[0]['utilized_hours']+=appoint_seconds
      special = models.DoctorSpecialHours.objects.filter(Q(doctor_n_key=i.employee_n_key)&Q(special_date=k))
      if special:
        if special[0].available == 'Closed':
          d['total'] = 'Vacation'
        else:
          spec_seconds=0
          for l in special:
            speci_diff = (datetime.datetime.strptime(str(l.end_time), '%H:%M:%S') - datetime.datetime.strptime(str(l.start_time), '%H:%M:%S')).total_seconds()
            spec_seconds += speci_diff
          spec_hours = SecondsToHour(spec_seconds)
          d['total'] = spec_hours
          temp_dates[0]['total_hours'] += spec_seconds
      else:
        req_date = datetime.datetime.strptime(k, '%Y-%m-%d').weekday()
        day = calendar.day_name[req_date]
        d['total']=SecondsToHour(emp_working[day])
        temp_dates[0]['total_hours'] += emp_working[day]
    alldata.append(temp_dates)
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="Therapist Attendance Report.csv"'
  fieldnames = ['SNo','Therapist']+dates+['total_hours','utilized_hours']
  filewriter = csv.DictWriter(response,fieldnames=fieldnames)
  filewriter.writeheader()
  s_no = 0
  for z in alldata:
    s_no += 1
    temp = {}
    temp['SNo'] = s_no
    temp['Therapist'] = z[0]['name']
    temp['total_hours'] = SecondsToHour(z[0]['total_hours'])
    temp['utilized_hours'] = SecondsToHour(z[0]['utilized_hours'])
    for x in z:
      if x['date'] != '':
        temp[x['date']] = (x['booked']+'/'+x['total']) if x['total'] != '0:0' and x['total'] != '' and x['total'] != 'Vacation' else 'Vacation' if x['total'] == 'Vacation' else'N/W'
    filewriter.writerow(temp)
  return response
  return HttpResponse(json.dumps(alldata), content_type="application/json")

def SecondsToHour(sec):
  seconds = int(sec)
  hour = seconds // 3600
  seconds %= 3600
  minute = seconds // 60
  totalHours = str(hour)+':'+str(minute)
  return totalHours

# @csrf_exempt
# def temp(request):
#   data = json.loads(request.body.decode('utf-8'))
#   doc_role = DoctorRoleQuery('ORGID-1')+['Physician']
#   emp = list(models.EmployeesMaster.objects.filter(Q(role__in=doc_role)&Q(org_n_key='ORGID-1')&Q(is_active=1)).values('first_name','last_name','phone_number','email','designation','languages_known','type_of_employement')) 
#   response = HttpResponse(content_type='text/csv')
#   response['Content-Disposition'] = 'attachment; filename="Careme_Employees.csv"'
#   fieldnames = ['SNo','FullName','PhoneNumber','Email','Designation','languages_known','type_of_employement']
#   filewriter = csv.DictWriter(response,fieldnames=fieldnames)
#   filewriter.writeheader()
#   s_no = 0
#   for i in emp:
#     s_no += 1 
#     filewriter.writerow({'SNo':s_no,'FullName':i['first_name']+' '+i['last_name'],'PhoneNumber':i['phone_number'],'Email':i['email'],'Designation':i['designation'],'languages_known':i['languages_known'],'type_of_employement':i['type_of_employement']})
#   return response

@csrf_exempt
def ProductGroup(request):
  data = json.loads(request.body.decode('utf-8'))
  grp = list(models.ProductGroupDetails.objects.filter(Q(org_n_key=data['org_n_key'])).values('app_prod_cat_id','app_prod_grp_key','title'))
  return HttpResponse(json.dumps({'status':'success','data':grp}), content_type="application/json")
