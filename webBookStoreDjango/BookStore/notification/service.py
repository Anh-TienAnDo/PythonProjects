from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

@csrf_exempt
def send_email(request):
    content = {

    }
    if request.method == 'POST':
        data = json.loads(request.body)
        content['user_id'] = data.get('user_id')
        content['name'] = data.get('name')
        content['phone'] = data.get('phone')
        content['email'] = data.get('email')
        content['address'] = data.get('address')
        content['city'] = data.get('city')
        content['code'] = data.get('code')

        subject = 'Xác Nhận Đơn Hàng'
        html_message = render_to_string('notification/email_ordered.html', {'content': content})
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [content['email']]
        try:
            # send_mail(subject, message, email_from, recipient_list)
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype ='html'
            message.send()
            return JsonResponse({'status': 'Success', 'message': 'send email successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'Failed', 'message': str(e)})
