from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import Payment
from .serializers import *
import re

def validate_bank(bank):
    error = None
    if not bank:
        error = "bank không được để trống."
    elif not re.match(r'^[0-9]*$', bank):
        error = "Bank chỉ chứa số."
    return error


# API để tạo payment mới
@csrf_exempt
def create_or_update_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        checkout_id = data.get('checkout_id')
        code = str(data.get('code'))
        bank = data.get('bank')
        total = data.get('total')
        paymented = data.get('paymented')
        if paymented is None:
            paymented = 0
        missing = total - paymented

        validation_error = validate_bank(bank)
        if validation_error is not None:
            return JsonResponse(
                {'status'     : 'Failed',
                'status_code': '400',
                'message'    : validation_error
                }, status=400)
        else:
            list_payment = Payment.objects.using('payment').filter(checkout=checkout_id)
            if len(list_payment) > 0:
                payment = list_payment[0]
                payment.code=code
                payment.bank=bank
                payment.checkout=checkout_id
                payment.total=total
                payment.paymented=paymented
                payment.missing=missing
                payment.save()

            else:
                # Tạo một đối tượng Payment
                payment = Payment.objects.using('payment').create(
                    code=code,
                    bank=bank,
                    checkout=checkout_id,
                    total=total,
                    paymented=paymented,
                    missing=missing,
                    note="",
                )
            data = PaymentSerializer(payment).data

            return JsonResponse({'status': 'Success', 'status_code': '201', 'message': 'Payment created successfully.', 'data': data}, status=201)

    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only POST method is allowed.'}, status=405)


# API để lấy thông tin của 1 payment by checkout_id
@csrf_exempt
def get_payment_by_checkoutid(request, checkout_id):
    if request.method == 'GET':
        payment = Payment.objects.using('payment').get(checkout=checkout_id)
        data = PaymentSerializer(payment).data
        return JsonResponse({'status': 'Success', 'status_code': '200', 'data': data})
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)




