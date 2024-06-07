from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from json import *
from app.views import getCookies
from .paypal import create_payment, execute_payment, cancel_payment, success_payment
from notification.views import send_email_service

# Create your views here.
def create_order_service(url = 'http://127.0.0.1:9995/orders/api/order/create', data={}):
    response = requests.post(url, json=data).json()
    return response

def create_or_update_payment_service(url = 'http://127.0.0.1:9995/payment/api/create_or_update', data={}):
    response = requests.post(url, json=data).json()
    return response

def get_payment_by_checkoutid_service(url = 'http://127.0.0.1:9995/payment/api/get/', checkout_id=0):
    url = url + str(checkout_id)
    response = requests.get(url).json()
    return response

def paymentBank(request):
    context = {
        'page_title': 'payment bank',
        'mybank': 'LE HONG ANH - 0961148064',
        'name_bank': 'VPBank',
    }
    if request.method == 'GET':
        return render(request, 'payment/payment_bank.html', context=context)
    elif request.method == 'POST':
        bank = request.POST.get('number_bank')
        data_order = request.session['checkout']
        result = create_order_service(data = data_order, token=getCookies(request))
        if result.get('status') == "Failed":
            context['notifications'] = result.get('message')
            context['content'] = data_order
            return render(request, 'order/shipment.html', context=context)
        else:
            payment_data = {
                'checkout_id': result.get('data').get('id'),
                'code': data_order.get('code'),
                'bank': bank,
                'total': result.get('data').get('total'),
            }
            result_payment = create_or_update_payment_service(data=payment_data)
            if result_payment.get('status') == "Failed":
                return HttpResponse(result_payment)
            del request.session['checkout']
            return render(request, 'order/ordered.html', context={'email': data_order.get('email')})
        

def payment_paypal(request):
    # Get the total amount and description from the cart
    amount = request.session['total']
    description = "payment by paypal"

    return create_payment(request, amount, description)

def execute_paypal(request):
    return execute_payment(request)

def cancel_paypal(request):
    return cancel_payment(request)
    # data_order = request.session['checkout']
    # context = {
    #     'page_title': 'Cancel payment',
    #     'notifications': 'Payment cancelled',
    #     'content': data_order,
    # }
    # return render(request, 'order/shipment.html', context=context)

def success_paypal(request):
    return success_payment(request)
