from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .service import *
from .models import *
from cart.service import CartServiceLogged, CartServiceNotLogged

# Create your views here.
def register(request):
    content = {}
    notifications = {}
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        content = {
            'username': username,
            'password': password,
            'confirm_password': confirm_password,
            'email': email,
            'fname': fname,
            'lname': lname,
        }
        result = create_user(data = content)
        if result['status']=='Success':
            if 'message' in request.session:
                request.session['message'] = "Đăng ký thành công. Bạn có thể đăng nhập ngay bây giờ."
            return redirect("user:log-in")
        else:
            notifications=result['message']
            return render(request, 'user/register.html', {'content': content, 'notifications': notifications})

    return render(request, 'user/register.html', {'content': content, 'notifications': notifications})

def login_user(request):
    content = {}
    notifications = {}
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        content = {
            'username': username,
            'password': password,
        }
        result = check_user_login(data=content)
        if result['status']=='Success':
            request.session['account'] = result['account']
            request.session['message'] = "Đăng nhập thành công."
            cart_service = CartServiceLogged(request)
            cart_service.get_cart_in_session_on_db()
            
            jwt_user_service = JWTUserMiddleware()
            user_information = result['account']
            token = jwt_user_service.create_token(data=user_information)
            response = HttpResponse("Đăng nhập thành công. Token: " + token)
            response.set_cookie('token', token)
            return response
            # return redirect("core:index")
        else:
            notifications=result['message']
            return render(request, 'user/login.html', {'content': content, 'notifications': notifications})
        
    return render(request, 'user/login.html', {'content': content, 'notifications': notifications})

def logout(request):
    if 'account' in request.session:
        del request.session['account']
    request.session['message'] = "Đăng xuất thành công."
    return redirect("core:index")

def informations(request):
    context = {}
    account = request.session.get('account')
    if account is None:
        return redirect("user:log-in")
    user = User.objects.get(account=account)
    name = Name.objects.get(id=user.name.id)
    context = {
        'user': user,
        'account': account,
        'name': name,
    }
    return render(request, 'user/informations.html', context=context)

def update(request):
    content = {}
    notifications = {}
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        street = request.POST['street']
        district = request.POST['district']
        city = request.POST['city']

        content = {
            'username': username,
            'email': email,
            'fname': fname,
            'lname': lname,
            'phone': phone,
            'street': street,
            'district': district,
            'city': city,
        }
        result = update_user(data = content)
        if result['status']=='Success':
            request.session['message'] = "Cập nhật thông tin thành công."
            return redirect("user:informations")
        else:
            notifications=result['message']
            return render(request, 'user/update.html', {'content': content, 'notifications': notifications})

def change_password(request):
    content = {}
    notifications = {}
    method = request.method
    if method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        content = {
            'old_password': old_password,
            'password': new_password,
            'confirm_password': confirm_password,
        }
        result = change_password_user(data = content)
        if result['status']=='Success':
            request.session['message'] = "Đổi mật khẩu thành công."
            return redirect("user:informations")
        else:
            notifications=result['message']
            return render(request, 'user/change_password.html', {'content': content, 'notifications': notifications})

    return render(request, 'user/change_password.html', {'content': content, 'notifications': notifications}) 

def login_user_ordered(request):
    content = {}
    notifications = {}
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        content = {
            'username': username,
            'password': password,
        }
        result = check_user_login(data=content)
        if result['status']=='Success':
            request.session['account'] = result['account']
            request.session['message'] = "Đăng nhập thành công."
            cart_service = CartServiceLogged(request)
            cart_service.get_cart_in_session_on_db()
            return redirect("order:checkout")
        else:
            notifications=result['message']
            return render(request, 'user/login_ordered.html', {'content': content, 'notifications': notifications})
        
    return render(request, 'user/login_ordered.html', {'content': content, 'notifications': notifications})