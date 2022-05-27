from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .import models
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.db.models import Avg, Count, Sum, IntegerField
from django.db.models.functions import Coalesce
import json
import datetime
import requests



#generate meeting ID

def generate_meetingid(request_data,appointment_n_key):
    try:
        available_credit =models.AudioCallBalance.objects.filter(Q(org_n_key=request_data['org_n_key'])).aggregate(recharge_amount_total=Coalesce(Sum('Amount'), 0, output_field=IntegerField()))
        used_balance = models.AudioCallLogs.objects.filter(Q(org_n_key=request_data['org_n_key'])).aggregate(used_credits=Coalesce(Sum('credits'),0, output_field=IntegerField()))
        available_balance = available_credit['recharge_amount_total'] - used_balance['used_credits']
        if available_balance >=1:
            url = "https://api.cluster.dyte.in/v1/organizations/90e0b776-6ab1-4249-8481-06ee1a6789b8/meeting"
            payload = {
                "title": "Online Consultation",
                "presetName": "therapist",
                "authorization": {
                    "waitingRoom": True,
                    "closed": True
                }
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "d2ef0104ecc50fdd8a6b"
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            response = json.loads(response.text)
            appoint = models.AppointmentMaster.objects.filter(Q(appointment_n_key=appointment_n_key))
            appoint.update(meeting_id=response['data']['meeting']['id'],room_name=response['data']['meeting']['roomName'])
            return {'status':'success'}
        else:
            return {'status':'failed','data':'Low Balance'}
    except Exception as e:
        return {'status':'failed','data':e}
    
# a = generate_meetingid({"org_n_key":"ORGID-1"},'CAR-APT-11442')
# print(a)

#add Patient to the meeting
@csrf_exempt
def JoinRoomPatient(request):
    request_data = json.loads(request.body.decode('utf-8'))
    appointment_details =models.AppointmentMaster.objects.filter(Q(appointment_n_key=request_data['appointment_n_key']))
    patient_details =models.PatientMaster.objects.filter(Q(patient_n_key=appointment_details[0].patient_n_key.patient_n_key)).values('first_name','last_name','patient_n_key')
    meeting_id=appointment_details[0].meeting_id
    url = "https://api.cluster.dyte.in/v1/organizations/90e0b776-6ab1-4249-8481-06ee1a6789b8/meetings/{}/participant".format(meeting_id)
    payload = {
        "clientSpecificId": patient_details[0]['patient_n_key'],
        "userDetails": {
            "name": patient_details[0]['first_name'] + patient_details[0]['last_name']
        },
        "presetName": "patient"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "d2ef0104ecc50fdd8a6b"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    response=json.loads(response.text)
    return HttpResponse(json.dumps({"status":"success","room_name":appointment_details[0].room_name,"auth_token":response['data']['authResponse']['authToken']}),content_type="application/json")


#add Therapist to the meeting
@csrf_exempt
def JoinRoomtherapist(request):
    request_data = json.loads(request.body.decode('utf-8'))
    appointment_details =models.AppointmentMaster.objects.filter(Q(appointment_n_key=request_data['appointment_n_key']))
    doctor_details =models.EmployeesMaster.objects.filter(Q(employee_n_key=appointment_details[0].doc_app_id)).values('first_name','last_name','employee_n_key')
    meeting_id=appointment_details[0].meeting_id
    url = "https://api.cluster.dyte.in/v1/organizations/90e0b776-6ab1-4249-8481-06ee1a6789b8/meetings/{}/participant".format(meeting_id)
    payload = {
        "clientSpecificId": doctor_details[0]['employee_n_key'],
        "userDetails": {
            "name": doctor_details[0]['first_name'] + doctor_details[0]['last_name']
        },
        "presetName": "therapist"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "d2ef0104ecc50fdd8a6b"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    response=json.loads(response.text)
    return HttpResponse(json.dumps({"status":"success","room_name":appointment_details[0].room_name,"auth_token":response['data']['authResponse']['authToken']}),content_type="application/json")         
