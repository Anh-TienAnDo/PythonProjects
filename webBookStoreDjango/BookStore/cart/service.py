from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import *
from .serializers import CartSerializer
from .cart import _generate_cart_id

# create api cart: get cart by user_id+product_slug+status=False|update cart, get carts and create cart: user_id=user_id, status=False, 
# create cart: cart_id=_generate_cart_id(), user_id=user_id, product_slug=slug, quantity=quantity
# delete cart: user_id=user_id, product_slug=slug

# API để lấy giỏ hàng theo user_id và product_slug và status=False
@csrf_exempt
def get_and_update_cart(request, user_id, product_slug):
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(user_id=user_id, product_slug=product_slug, status=False)
            resp = {
                'status'     : 'Success',
                'status_code': '200',
                'data'       : CartSerializer(cart).data,
            }
            
            return JsonResponse(resp)
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'Failed', 'status_code': '404', 'message': 'Cart does not exist.'}, status=404)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity')
        quantity = int(quantity)
        status = data.get('status')
        if quantity is None:
            return JsonResponse({'status': 'Failed', 'status_code': '400', 'message': 'Quantity is not None.'}, status=400)
        try:
            cart = Cart.objects.get(user_id=user_id, product_slug=product_slug, status=False)
            cart.quantity = cart.quantity + quantity
            if status is not None and int(status) == 1:
                cart.status = True
            if cart.quantity <= 0:
                cart.delete()
            else:
                cart.save()
            return JsonResponse({'status': 'Success', 'status_code': '201', 'message': 'Cart updated successfully.'})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'Failed', 'status_code': '404', 'message': 'Cart does not exist.'}, status=404)


# API để xóa giỏ hàng
@csrf_exempt
def delete_cart(request, user_id, product_slug):
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(user_id=user_id, product_slug=product_slug, status=False)
            cart.delete()
            return JsonResponse({'status': 'Success', 'status_code': '200', 'message': 'Cart deleted successfully.'})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'Failed', 'status_code': '404', 'message': 'Cart does not exist.'}, status=404)

# API để tạo giỏ hàng mới
@csrf_exempt
def get_carts_and_create_cart(request, user_id):
    if request.method == 'GET':
        carts = Cart.objects.filter(user_id=user_id, status=False)
        resp = {'status': 'Success', 'status_code': '200', 'data': CartSerializer(carts, many=True).data}
        return JsonResponse(resp)
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        product_slug = data.get('product_slug')
        quantity = data.get('quantity')
        if user_id is None or product_slug is None or quantity is None:
            return JsonResponse({'status': 'Failed', 'status_code': '400', 'message': 'Data cart eroor.'})
        try:
            cart = Cart.objects.filter(user_id=user_id, product_slug=product_slug, status=False)
            if len(cart)==0:
                Cart.objects.create(cart_id=_generate_cart_id(), user_id=user_id, product_slug=product_slug, quantity=quantity)
            elif len(cart)>0:
                cart = cart[0]
                cart.quantity = cart.quantity + quantity
                cart.save()
            return JsonResponse({'status': 'Success', 'status_code': '201', 'message': 'Cart created successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'Failed', 'status_code': '404', 'message': str(e)}, status=400)



