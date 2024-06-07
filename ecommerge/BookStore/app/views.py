from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from product.models import Product
from cart.cart import CartService

# Create your views here.
def home(req):
    cart = CartService(request=req)
    products = Product.objects.all()
    content = {'products': products}
    return render(req, 'home.html', content)

def informations(req):
    return render(req, "user/informations.html")

def register(request):
    content = {}
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        content['username'] = username
        content['email'] = email
        content['first_name'] = first_name
        content['last_name'] = last_name
        if password == confirm_password and username:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username is already exist')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                messages.info(request, 'You have successfully registered')
                return redirect(login_user)
        else:
            messages.info(request, 'Password and Confirm Password do not match')
            return render(request, 'user/register.html', content)
    else:
        return render(request, 'user/register.html', content)

def login_user(request):
    method = request.method
    if method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            messages.info(request, "Logged in successfully")
            return redirect(home)
        else:
            messages.info(request, "Invalid username and password")
            return redirect(login_user)
    else:
        content = {}
        return render(request, 'user/login.html', content)
    
def logout_user(request):
    logout(request)
    messages.info(request, "you are logged out")
    return redirect(login_user)

