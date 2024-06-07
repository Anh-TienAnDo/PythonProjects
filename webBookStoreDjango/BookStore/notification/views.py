from django.shortcuts import render
from django.http import HttpResponse
import json
import requests

# Create your views here.
# send_email when ordered
def send_email_service(url = 'http://127.0.0.1:9995/notification/email', data={}):
    print('Notification Service: ' + url)
    response = requests.post(url, json=data).json()
    print('Data:')
    print(response)
    return response