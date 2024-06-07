from django.shortcuts import render, HttpResponse
import json
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .serializers import *

# Create your views here.
@csrf_exempt
def get_users(request):
    method = request.method
    if method == 'GET':
        users = User.objects.all()
        resp = {'status': 'Success', 'status_code': '200', 'data': UserSerializer(users, many=True).data}
        return JsonResponse(resp)

