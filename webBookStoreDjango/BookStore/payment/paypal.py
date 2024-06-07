# payment/paypal.py

import paypalrestsdk
from django.shortcuts import render, redirect
from django.http import HttpResponse
from BookStore.settings import PAYPAL

def configure_paypal():
    print(PAYPAL.get('CLIENT_ID'))
    print(PAYPAL.get('CLIENT_SECRET'))
    paypalrestsdk.configure({
      "mode": "sandbox", # sandbox or live
      "client_id": PAYPAL.get('CLIENT_ID'),
      "client_secret": PAYPAL.get('CLIENT_SECRET') })

def create_payment(request, amount, description):
    configure_paypal()

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:9995/payment/execute-paypal",
            "cancel_url": "http://localhost:9995/payment/cancel-paypal"},
        "transactions": [{
            "item_list": {
                "items": []},
            "amount": {
                "total": str(int(amount)/25000),
                "currency": "USD"},
            "description": description}]})

    if payment.create():
        return redirect(payment.links[1].href)
    else:
        return HttpResponse('Error occurred while creating payment: {}'.format(payment.error))

def execute_payment(request):
    configure_paypal()

    payment = paypalrestsdk.Payment.find(request.GET['paymentId'])
    if payment.execute({"payer_id": request.GET['PayerID']}):
        return redirect(to='success-paypal')
    else:
        return HttpResponse('Error occurred while executing payment: {}'.format(payment.error))

def cancel_payment(request):
    return HttpResponse('Payment cancelled')

def success_payment(request):
    return HttpResponse('Payment successful')