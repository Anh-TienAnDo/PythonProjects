import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Checkout, OrderItems
from cart.models import CartItems
from cart.service import CartServiceLogged
from django.http import JsonResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create your views here.

def checkout(request):
    if 'account' not in request.session:
        logger.info("User not logged in, redirecting to login page")
        return redirect('user:log-in-ordered')
    else:
        user_id = request.session['account']['id']
        if request.method == "GET":
            logger.info("GET request received for checkout")
            page_title = 'Checkout'
            cart_items = CartItems.objects.filter(user_id=user_id, status=False)
            total_quantity = len(cart_items)
            total_price = 0
            for item in cart_items:
                total_price += item.price * item.quantity
            content = {'page_title': page_title, 'cart_items': cart_items, 'total_quantity': total_quantity, 'total_price': total_price}
            logger.info("Rendering checkout page with %d items", total_quantity)
            return render(request, 'order/checkout.html', content)
        elif request.method == "POST":
            logger.info("POST request received for checkout")
            person_name = request.POST['person_name']
            number_house = request.POST['number_house']
            street = request.POST['street']
            district = request.POST['district']
            city = request.POST['city']
            phone = request.POST['phone']
            email = request.POST['email']
            total = request.POST['total']
            order = Checkout(user_id=user_id, person_name=person_name, number_house=number_house, street=street, district=district, city=city, phone=phone, email=email, total=total)
            order.save()
            logger.info("Order saved with ID %d", order.id)
            cart_items = CartItems.objects.filter(user_id=user_id)
            for item in cart_items:
                order_item = OrderItems(id=item.id, product_slug=item.product_slug, price=item.price, quantity=item.quantity, checkout=order)
                order_item.save()
            cart_items.delete()
            logger.info("Cart items deleted for user ID %d", user_id)
            return HttpResponse('Order success')

def order_list(request):
    if 'account' not in request.session:
        logger.info("User not logged in, redirecting to login page")
        return redirect('user:log-in')
    else:
        user_id = request.session['account']['id']
        orders = Checkout.objects.filter(user_id=user_id)
        page_title = 'Orders'
        content = {'page_title': page_title, 'orders': orders}
        logger.info("Rendering order list page for user ID %d", user_id)
        return render(request, 'order/history.html', content)

def orderitems(request, order_id):
    logger.info("Request received for order items with order ID %d", order_id)
    order_items = OrderItems.objects.filter(checkout=order_id)
    return HttpResponse(order_items)

def cancel_order(request, order_id):
    logger.info("Request received to cancel order with ID %d", order_id)
    order = Checkout.objects.get(id=order_id)
    if order.status == '4':
        logger.info("Order with ID %d already cancelled", order_id)
        return HttpResponse('Order already cancelled')
    elif order.status == '1':
        order.status = '4'
        order.save()
        logger.info("Order with ID %d cancelled", order_id)
    else:
        logger.info("Order with ID %d cannot be cancelled", order_id)
        return HttpResponse('Order cannot be cancelled')
    return HttpResponse('Order cancelled')

def re_cancel_order(request, order_id):
    logger.info("Request received to re-cancel order with ID %d", order_id)
    order = Checkout.objects.get(id=order_id)
    if order.status == '1':
        logger.info("Order with ID %d already pending", order_id)
        return HttpResponse('Order already pending')
    elif order.status == '4':
        order.status = '1'
        order.save()
        logger.info("Order with ID %d re-cancelled", order_id)
    else:
        logger.info("Order with ID %d cannot be re-cancelled", order_id)
        return HttpResponse('Order cannot be re-cancelled')
    return HttpResponse('Order re-cancelled')

