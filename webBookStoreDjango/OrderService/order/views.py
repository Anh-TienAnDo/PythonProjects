from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import *
from .serializers import *
import re
import jwt, datetime
from OrderService.settings import SIMPLE_JWT

# create api Checkout and OrderItems:
# get all Checkout by user_id | cancel Checkout by user_id,
# get all OrderItems by checkout__id, checkout__user_id

def _generate_code():
    code = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    code_length = 10
    for y in range(code_length):
        code += characters[random.randint(0, len(characters) - 1)]
    return code

def validate_data(data):
    errors = {}

    # Kiểm tra name
    name = data.get('name')
    if not name:
        errors['name'] = "Name không được để trống."
    elif not name.replace(" ", "").isalpha():
        errors['name'] = "Name chỉ bao gồm chữ cái và dấu cách."

    # Kiểm tra email
    email = data.get('email')
    if not email:
        errors['email'] = "Email không được để trống."
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors['email'] = "Email không hợp lệ."

    # Kiểm tra độ dài phone
    phone = data.get('phone')
    if not phone:
        errors['phone'] = "Phone không được để trống."
    elif len(phone) != 10:
        errors['phone'] = "Phone phải có 10 ký tự."

    # Kiểm tra định dạng của address và city
    address = data.get('address')
    if not address:
        errors['address'] = "Address không được để trống."

    city = data.get('city')
    if not city:
        errors['city'] = "City không được để trống."

    return errors

# API để tạo đơn hàng mới
@csrf_exempt
def create_order(request):
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        resp = {'status'     : 'Failed',
                'status_code': '400',
                'message'    : "Not Token"}
        return JsonResponse(resp, status=400)

    try:
        payload = jwt.decode(jwt=token, key=SIMPLE_JWT.get("SIGNING_KEY"), algorithms=[SIMPLE_JWT.get("ALGORITHM")])
    except jwt.ExpiredSignatureError:
        resp = {'status'     : 'Failed',
                'status_code': '400',
                'message'    : "Error Token!"}
        return JsonResponse(resp, status=400)
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        address = data.get('address')
        city = data.get('city')
        code = data.get('code')

        validation_errors = validate_data(data)
        if validation_errors:
            return JsonResponse(
                {'status'     : 'Failed',
                'status_code': '400',
                'message'    : validation_errors
                }, status=400)
        else:
            list_order = Checkout.objects.using('order').filter(user_id=user_id, code=code)
            if len(list_order) > 0:
                checkout = list_order[0]
                checkout.user_id=user_id
                checkout.name=name
                checkout.code=code
                checkout.phone=phone
                checkout.email=email
                checkout.address=address
                checkout.city=city
                checkout.save()
            else:
                # Tạo một đối tượng Checkout mới
                total = 0
                checkout = Checkout.objects.using('order').create(
                    user_id=user_id,
                    name=name,
                    code=code,
                    phone=phone,
                    email=email,
                    address=address,
                    city=city,
                    total=total,
                    note="",
                )
                checkout.save()
                # Cập nhật trạng thái của các mặt hàng trong đơn hàng
                result = get_all_cart_service(user_id=user_id)
                if result.get('status') == "Failed":
                    return HttpResponse(result)
                items = result.get('data')
                for item in items:
                    product = getDetailsBookServiceUrl(slug=item.get('product_slug'))
                    if product is None:
                        product = getDetailsMobileServiceUrl(slug=item.get('product_slug'))
                    if product is None:
                        product = getDetailsClothesServiceUrl(slug=item.get('product_slug'))
                    total += product.get('price') * item.get('quantity')
                    OrderItems.objects.using('order').create(
                        product_slug=item.get('product_slug'),
                        price=product.get('price'),
                        quantity=item.get('quantity'),
                        checkout=checkout
                    )
                    delete_cart = delete_cart_service(user_id=user_id, product_slug=item.get('product_slug'))
                    if delete_cart.get('status') == "Failed":
                        return HttpResponse(delete_cart)
                    # update_cart = update_cart_service(user_id=user_id, product_slug=item.get('product_slug'), data={'quantity': 0,
                    #                                                                                                 'status': 1,})
                checkout.total = total
                checkout.save()
            data = CheckoutSerializer(checkout).data

            return JsonResponse({'status': 'Success', 'status_code': '201', 'message': 'Order created successfully.','data': data}, status=201)

    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only POST method is allowed.'}, status=405)

# API để lấy tất cả đơn hàng của một người dùng bằng user_id
@csrf_exempt
def get_checkouts_by_user(request, user_id):
    if request.method == 'GET':
        checkouts = Checkout.objects.using('order').filter(user_id=user_id)
        orders = CheckoutSerializer(checkouts, many=True).data
        return JsonResponse({'status': 'Success', 'status_code': '200', 'data': orders})
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)

# API để lấy tất cả đơn hàng
@csrf_exempt
def get_checkouts(request):
    if request.method == 'GET':
        checkouts = Checkout.objects.using('order').all()
        orders = CheckoutSerializer(checkouts, many=True).data
        return JsonResponse({'status': 'Success', 'status_code': '200', 'data': orders})
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)


# API để hủy đơn hàng của một người dùng bằng user_id
@csrf_exempt
def cancel_checkout(request, id):
    if request.method == 'GET':
        checkout = Checkout.objects.using('order').get(id=id)
        checkout.status = 5
        checkout.save()
        return JsonResponse({'status': 'Success', 'status_code': '200', 'message': 'Order cancelled successfully.'}, status=200)
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)

@csrf_exempt
def re_order_checkout(request, id):
    if request.method == 'GET':
        checkout = Checkout.objects.using('order').get(id=id)
        checkout.status = 1
        checkout.save()
        return JsonResponse({'status': 'Success', 'status_code': '200', 'message': 'Order cancelled successfully.'}, status=200)
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)

# API để lấy tất cả các mặt hàng trong một đơn hàng bằng checkout_id
@csrf_exempt
def get_order_items(request, checkout_id):
    if request.method == 'GET':
        order_items = OrderItems.objects.using('order').filter(checkout__id=checkout_id)
        items = OrderItemsSerializer(order_items, many=True).data
        return JsonResponse({'status': 'Success', 'status_code': '200', 'data': items})
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)

# API để lấy tất cả các mặt hàng đã được order
@csrf_exempt
def get_all_order_items(request):
    if request.method == 'GET':
        order_items = OrderItems.objects.using('order').all()
        items = OrderItemsSerializer(order_items, many=True).data
        return JsonResponse({'status': 'Success', 'status_code': '200', 'data': items})
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)


# API để lấy thông tin của 1 checkout
@csrf_exempt
def get_checkout(request, checkout_id):
    if request.method == 'GET':
        checkout = Checkout.objects.using('order').get(id=checkout_id)
        data = CheckoutSerializer(checkout).data
        return JsonResponse({'status': 'Success', 'status_code': '200', 'data': data})
    else:
        return JsonResponse({'status': 'Failed', 'status_code': '405', 'message': 'Only GET method is allowed.'}, status=405)

