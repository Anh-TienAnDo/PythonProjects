from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import CartService, _generate_cart_id
from book.book import *
from mobile.mobile import *
from clothes.clothes import *
from cart.models import *
from .forms import *
import requests
from json import *
from cart import views
from datetime import datetime, timedelta

def getCookies(request):
    try:
        token = str(request.COOKIES.get('token'))
    except KeyError:
        token = None
    return token

def user_register_service(url = 'http://127.0.0.1:9997/user/register', data={}):
    response = requests.post(url, json=data).json()
    return response

def user_login_service(url = 'http://127.0.0.1:9997/user/login', data={}):
    response = requests.post(url, json=data).json()
    return response

def user_update_service(url = 'http://127.0.0.1:9997/user/informations/', id="", data={}, token=""):
    url = url + str(id)
    headers = {
        'Content-Type': 'application/json',  # Example header
        'Authorization': token, # Example header for authorization
    }
    response = requests.post(url, headers=headers, json=data).json()
    return response

def get_user_service(url = 'http://127.0.0.1:9997/user/informations/', id="", token=""):
    url = url + str(id)
    headers = {
        'Content-Type': 'application/json',  # Example header
        'Authorization': token, # Example header for authorization
    }
    response = requests.get(url, headers=headers).json()
    return response

def user_change_password_service(url = 'http://127.0.0.1:9997/user/change-password/', id="", data={}, token=""):
    url = url + str(id)
    headers = {
        'Content-Type': 'application/json',  # Example header
        'Authorization': token, # Example header for authorization
    }
    response = requests.post(url, headers=headers, json=data).json()
    return response

def add_user_to_session(request, data):
    try:
        if 'user' not in request.session:
            request.session['user'] = data.get('user')
        if 'account' not in request.session:
            request.session['account'] = data.get('account')
        if 'address' not in request.session:
            request.session['address'] = data.get('address')
        if 'name_user' not in request.session:
            request.session['name_user'] = data.get('name_user')
        return 'Success'
    except Exception as e:
        print(e)
        return 'Failed'
    
def update_user_in_session(request, data):
    try:
        if 'user' in request.session:
            request.session['user'] = data.get('user')
        if 'account' in request.session:
            request.session['account'] = data.get('account')
        if 'address' in request.session:
            request.session['address'] = data.get('address')
        if 'name_user' in request.session:
            request.session['name_user'] = data.get('name_user')
        return 'Success'
    except Exception as e:
        print(e)
        return 'Failed'

def delete_user_in_session(request):
    try:
        if 'user' in request.session:
            del request.session['user']
        if 'name_user' in request.session:
            del request.session['name_user']
        if 'account' in request.session:
            del request.session['account']
        if 'address' in request.session:
            del request.session['address']
        return 'Success'
    except Exception as e:
        print(e)
        return 'Failed'
    
def delete_product_in_session(request):
    try:
        if 'books' in request.session:
            del request.session['books']
        if 'mobiles' in request.session:
            del request.session['mobiles']
        if 'clothes' in request.session:
            del request.session['clothes']
        return 'Success'
    except Exception as e:
        print(e)
        return 'Failed'

def clear_cookies(request):
    response = HttpResponse()
    # Xóa cookie 'token'
    response.delete_cookie('token')
    return 'Success'

def get_page_header_user(request):
    if request.session['account'].get('is_staff') is False:
        page = 'page/header.html'
    else:
        page = 'page/manage_header.html'
    return page

# Create your views here.
def home(req):
    if 'user' not in req.session or req.session['account'].get('is_staff') is False:
        try:
            if 'books' not in req.session:
                req.session['books'] = getBooksServiceUrl()
            if 'mobiles' not in req.session:
                req.session['mobiles'] = getMobilesServiceUrl()
            if 'clothes' not in req.session:
                req.session['clothes'] = getClothesServiceUrl()
        except Exception as e:
            print('error connection service product')
            req.session['books'] = None
            req.session['mobiles'] = None
            req.session['clothes'] = None

        context = {
            'page_title': 'home',
            'products': req.session['books'],
            'mobiles': req.session['mobiles'],
            'clothes': req.session['clothes'],
        }
        return render(req, 'home.html', context)
    elif req.session['account'].get('is_superuser'):
        template = loader.get_template('manage/home.html')
        context = {
            
        }
        # return render(req, 'home.html', context)
        return HttpResponse(template.render(context, req))

def informations(req):
    page = get_page_header_user(req)
    context = {
        'page': page 
    }
    return render(req, "user/informations.html", context)

def update_password(request):
    page = get_page_header_user(request)
    content = {
        'page': page 
    }
    notifications = ""
    if request.method == "POST":
        user = request.session['user']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        result = user_change_password_service(id=user.get("id"), data={"password": password,
                                                                       'confirm_password': confirm_password,}
                                                                       , token=getCookies(request))
        if result['status'] == 'Success':
            return redirect('informations-user')
        else:
            notifications=result['message']
            return render(request, "user/change-password.html", content)
    return render(request, "user/change-password.html", content)


def update_user(request):
    page = get_page_header_user(request)
    content = {
        'page': page,
    }
    notifications = {}
    user = request.session['user']
    account = request.session['account']
    name_user = request.session['name_user']
    content['username'] = account.get('username')
    content['email'] = account.get('email')
    content['fname'] = name_user.get('fname')
    content['lname'] = name_user.get('lname')
    content['phone'] = user.get('phone')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        content['username'] = username
        content['email'] = email
        content['fname'] = first_name
        content['lname'] = last_name
        content['phone'] = phone
        result = user_update_service(id=user.get("id"), data=content, token=getCookies(request))
        if result['status'] == 'Success':
            update_user = update_user_in_session(request=request, data=result['data'])
            return redirect('informations-user')
        else:
            notifications=result['message']
            return render(request, "user/update-user.html", {'content': content, 'notifications': notifications})
    return render(request, "user/update-user.html", {'content': content, 'notifications': notifications})

# dang ky -> dang nhap save session 
#  logout: delete session
def register(request):
    content = {}
    notifications = {}
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        content['username'] = username
        content['email'] = email
        content['fname'] = first_name
        content['lname'] = last_name
        content['phone'] = phone
        content['password'] = password
        content['confirm_password'] = confirm_password
        result = user_register_service(data=content)
        if result['status']=='Success':
            return redirect(login_user)
        else:
            notifications=result['message']
            return render(request, 'user/register.html', {'content': content, 'notifications': notifications})

    return render(request, 'user/register.html', {'content': content, 'notifications': notifications})

def login_user(request):
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        result = user_login_service(data={'username': username,
                                          'password': password,})
        # Logged in successfully
        if result['status'] == 'Success':
            user_id = result['data']['user'].get('id')
            add_session = add_user_to_session(request=request, data=result['data'])
            cartService = CartService(request=request)
            for product_slug, item in cartService.cart.items():
                result_cart = views.create_cart_service(user_id=user_id, data={'user_id': user_id,
                                                            'product_slug': product_slug,
                                                            'quantity': item['quantity'],})
                if result_cart.get('status') == "Failed":
                    return HttpResponse(result_cart)

            cartService.clear()
            print("token: " + str(result['data']['token']))
            response = HttpResponse("Token user: " + str(result['data']['token']))
            response.set_cookie('token', result['data']['token'])
            return response
            # return redirect(home)
        # Invalid username and password
        else:
            notifications = result['message']
            render(request, 'user/login.html', {'notifications': notifications})
    if method == 'GET':
        content = {}
        if 'user' in request.session:
            return redirect(home)
        return render(request, 'user/login.html', content)

    
def logout_user(request):
    delete_user = delete_user_in_session(request=request)
    delete_product = delete_product_in_session(request=request)
    delete_cookie = clear_cookies(request)
    return redirect(login_user)



