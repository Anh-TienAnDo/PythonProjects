from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from order.views import get_all_order_items_service, get_checkouts_service
from clothes.clothes import *
from mobile.mobile import *
from book.book import *
import json
from app.views import get_page_header_user, get_user_service, getCookies
from app.service import format_string_to_date

# get all orderiem
# dict['product']=total
# sort
# get product
# show
def report_product(request):
    if request.method == "GET":
        result_report_product = []
        page = get_page_header_user(request)
        context = {
            'page_title': 'report product',
            'page': page,
        }
        product = {}
        get_items = get_all_order_items_service() 
        if get_items.get('status') == "Failed":
            return HttpResponse(get_items)
        else:
            items = get_items.get('data')
            for i in items:
                product_slug = i.get('product_slug')
                if product_slug in product:
                    product[product_slug] += int(i.get('price')) *  int(i.get('quantity'))
                else:
                    product[product_slug] = int(i.get('price')) *  int(i.get('quantity'))
            # Sắp xếp từ điển product theo giá trị giảm dần
            sorted_product = dict(sorted(product.items(), key=lambda item: item[1], reverse=True))
            for k,v in sorted_product.items():
                tmp = {}
                product = getDetailsBookServiceUrl(slug=k)
                if product is None:
                    product = getDetailsMobileServiceUrl(slug=k)
                if product is None:
                    product = getDetailsClothesServiceUrl(slug=k)
                tmp['product'] = product
                tmp['total'] = v
                tmp['quantity'] = str(int(v)/int(product.get('price')))[0:-2]
                result_report_product.append(tmp)
            context['result'] = result_report_product

            return render(request, 'manage/report-product.html', context=context)
            # return HttpResponse(result_report_product)


# get all checkout
# dict['user_id']=total
# sort
# get user by id
# show
def report_customer(request):
    if request.method == "GET":
        result_report_customer = []
        page = get_page_header_user(request)
        context = {
            'page_title': 'report customer',
            'page': page,
        }
        customer = {}
        get_orders = get_checkouts_service()
        if get_orders.get('status') == "Failed":
            return HttpResponse(get_orders)
        else:
            orders = get_orders.get('data')
            for o in orders:
                user_id = o.get('user_id')
                if user_id in customer:
                    customer[user_id] += int(o.get('total'))
                else:
                    customer[user_id] = int(o.get('total'))
            # Sắp xếp từ điển customer theo giá trị giảm dần
            sorted_customer = dict(sorted(customer.items(), key=lambda item: item[1], reverse=True))
            for k,v in sorted_customer.items():
                tmp = {}
                get_user = get_user_service(id=k, token=getCookies(request))
                user_data = get_user.get('data')
                user_dict = dict(user_data.get('account'))
                user_dict.update(dict(user_data.get('user'))) 
                tmp['user'] = user_dict
                tmp['total'] = v
                tmp['user']['created_at'] = format_string_to_date(tmp['user']['created_at'])
                result_report_customer.append(tmp)
            context['result'] = result_report_customer

            return render(request, 'manage/report-customer.html', context=context)
            # return HttpResponse(result_report_customer)


