from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from cart.models import *
from clothes.clothes import *
from mobile.mobile import *
from book.book import *
from notification.views import send_email_service
from .service import _generate_code
from payment import views
from app.service import format_string_to_date
from app.views import getCookies
import json
import requests

# Create your views here.
# get checkouts by user
def get_checkouts_by_user_service(url = 'http://127.0.0.1:9995/orders/api/checkouts/', user_id=0):
    url = url + str(user_id)
    response = requests.get(url).json()
    return response

# get all checkout for report by customer
def get_checkouts_service(url = 'http://127.0.0.1:9995/orders/api/checkouts'):
    response = requests.get(url).json()
    return response

# get items in an order by checkout_id
def get_order_items_service(url = 'http://127.0.0.1:9995/orders/api/order-items/', checkout_id=0):
    url = url + str(checkout_id)
    response = requests.get(url).json()
    return response

# get all items exists for report product
def get_all_order_items_service(url = 'http://127.0.0.1:9995/orders/api/all-order-items'):
    response = requests.get(url).json()
    return response

# create or update an order
def create_order_service(url = 'http://127.0.0.1:9995/orders/api/order/create', data={}, token=''):
    
    headers = {
        'Content-Type': 'application/json',  # Example header
        'Authorization': token, # Example header for authorization
    }
    print("token: ")
    print(str(token))
    try:
        response = requests.post(url, headers=headers, json=data, timeout=(5, 10))
        response = response.json()
    except requests.exceptions.Timeout:
        print("Timed out")
        try:
            response = requests.post(url, headers=headers, json=data, timeout=(5, 10))
            response = response.json()
        except requests.exceptions.Timeout:
            print("Timed out")
            try:
                response = requests.post(url, headers=headers, json=data, timeout=(5, 10))
                response = response.json()
            except requests.exceptions.Timeout:
                print("Timed out")
                response = {'status': 'Failed', 'message': 'Timed out'}
    print("-----------------------------")
    print("Token: " + str(token))
    print("Order Service: create_order_service - " + 'http://127.0.0.1:9995/orders/api/order/create')
    print("Order Service Data:")
    print(response)
    return response

# user cancel order by id
def cancel_checkout_service(url = 'http://127.0.0.1:9995/orders/api/checkouts/', id=0):
    url = url + str(id) + '/cancel'
    response = requests.get(url).json()
    return response

# user re-order by id
def re_order_checkout_service(url = 'http://127.0.0.1:9995/orders/api/checkouts/', id=0):
    url = url + str(id) + '/re_order'
    response = requests.get(url).json()
    return response

# get information user of an order, when user view details
def get_checkout_service(url = 'http://127.0.0.1:9995/orders/api/checkout/', checkout_id=0):
    url = url + str(checkout_id)
    response = requests.get(url).json()
    return response

# -----------------------------------------
def getOrders(request):
    user_id = request.session['user'].get('id')
    result = []
    result_order = get_checkouts_by_user_service(user_id=user_id)
    if result_order.get('status') == "Failed":
        return HttpResponse(result_order)
    else:
        orders = result_order.get('data')
        for order in orders:
            payment = views.get_payment_by_checkoutid_service(checkout_id=order.get('id'))
            if payment.get('status') == "Failed":
                return HttpResponse(result_order)
            else:
                date_order = order.get('date_order')
                order['date_order'] = format_string_to_date(date_order)
                result.append({'order': order,
                               'payment': payment.get('data'),})
    # orders = Checkout.objects.filter(user_id=user_id)
    context = {
        'page_title': 'orders',
        'result': result,
    }
    return render(request=request, template_name='order/orders.html', context=context)

def checkout(request):
    context = {
        'page_title': 'checkout',
        'notifications': None,
        'content': None,
    }
    if request.method == "GET":
        if 'user' in request.session:
            return render(request, 'order/shipment.html', context=context)
        else:
            return redirect(to='login-user')
    elif request.method == "POST":
        user_id = request.session['user'].get('id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        payment_method = request.POST.get('payment')
        code = _generate_code()

        content = {}
        content['user_id'] = user_id
        content['name'] = name
        content['phone'] = phone
        content['email'] = email
        content['address'] = address
        content['city'] = city
        content['code'] = code

        if payment_method == 'offline':
            result = create_order_service(data = content, token=getCookies(request))
            if result.get('status') == "Failed":
                context['notifications'] = result.get('message')
                context['content'] = content
                return render(request, 'order/shipment.html', context=context)
            else:
                if 'checkout' in request.session:
                    del request.session['checkout']
                payment_data = {
                    'checkout_id': result.get('data').get('id'),
                    'code': result.get('data').get('code'),
                    'bank': '0',
                    'total': result.get('data').get('total'),
                }
                result_payment = views.create_or_update_payment_service(data=payment_data)
                if result_payment.get('status') == "Failed":
                    return HttpResponse(result_payment)
                result_email = send_email_service(data=content)
                if result_email.get('status') == "Failed":
                    return HttpResponse(result_email)
                return render(request, 'order/ordered.html', context={'email': email})
        elif payment_method == 'online':
            request.session['checkout'] = content
            return redirect(to='payment-bank')

        elif payment_method == 'paypal':
            result = create_order_service(data = content, token=getCookies(request))
            if result.get('status') == "Failed":
                context['notifications'] = result.get('message')
                context['content'] = content
                return render(request, 'order/shipment.html', context=context)
            else:
                if 'checkout' in request.session:
                    del request.session['checkout']
                payment_data = {
                    'checkout_id': result.get('data').get('id'),
                    'code': result.get('data').get('code'),
                    'bank': '0',
                    'total': result.get('data').get('total'),
                    'paymented': result.get('data').get('total'),
                }
                result_payment = views.create_or_update_payment_service(data=payment_data)
                if result_payment.get('status') == "Failed":
                    return HttpResponse(result_payment)
                result_email = send_email_service(data=content)
                if result_email.get('status') == "Failed":
                    return HttpResponse(result_email)
            return redirect(to='payment-paypal')
            # return redirect(to='home')
        # total = 0
        # # Tạo một đối tượng Checkout mới
        # checkout = Checkout.objects.create(
        #     user_id=user_id,
        #     name=name,
        #     phone=phone,
        #     email=email,
        #     address=address,
        #     city=city,
        #     total=total,  
        #     note="",
        # )
        # checkout.save()
        
        # items = Cart.objects.filter(user_id=user_id, status=False)
        # for item in items:
        #     total += item.getTotal
        #     product = getDetailsBookServiceUrl(slug=item.product_slug)
        #     if product is None:
        #         product = getDetailsMobileServiceUrl(slug=item.product_slug)
        #     if product is None:
        #         product = getDetailsClothesServiceUrl(slug=item.product_slug)
        #     orderitem = OrderItems.objects.create(
        #         product = item.product_slug,
        #         price = product['price'],
        #         quantity = item.quantity,
        #         checkout = checkout,
        #     )
        # checkout.total = total
        # checkout.save()
        # items.update(status=True)


def detailsOrder(request, id):
    context = {
        'page_title': f'details order {id}',
        'notifications': None,
        'content': None,
    }
    user_id = request.session['user'].get('id')
    result_api_orderitems = get_order_items_service(checkout_id=id)
    if result_api_orderitems.get('status') == "Failed":
        return HttpResponse(result_api_orderitems)
    else:
        items = result_api_orderitems.get('data')
    # items = OrderItems.objects.filter(checkout__id=id, checkout__user_id=user_id)
    result_api_checkout = get_checkout_service(checkout_id=id)
    if result_api_checkout.get('status') == "Failed":
        return HttpResponse(result_api_checkout)
    else:
        information_order = result_api_checkout.get('data')
    result = []
    for item in items:
        product = getDetailsBookServiceUrl(slug=item.get('product_slug'))
        if product is None:
            product = getDetailsMobileServiceUrl(slug=item.get('product_slug'))
        if product is None:
            product = getDetailsClothesServiceUrl(slug=item.get('product_slug'))
        tmp = {}
        tmp['item'] = item
        tmp['price'] = int(item.get('quantity')) * int(product.get('price'))
        tmp['product'] = product
        result.append(tmp)
    context = {
        'page_title': 'items of order ' + str(id),
        'result': result,
        'information_order': information_order,
        'quantity_item': len(items),
    }
    return render(request=request, template_name='order/details_order.html', context=context)

def cancelOrder(request, id):
    user_id = request.session['user'].get('id')
    if request.method == "GET":
        result = cancel_checkout_service(id=id)
        if result.get('status') == "Failed":
            return HttpResponse(result)
        else:
            return redirect(to='orders')

def re_Order(request, id):
    user_id = request.session['user'].get('id')
    if request.method == "GET":
        result = re_order_checkout_service(id=id)
        if result.get('status') == "Failed":
            return HttpResponse(result)
        else:
            return redirect(to='orders')


