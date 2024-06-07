from django.shortcuts import render, redirect
from .service import Person

# Create your views here.
def informations(request):
    context = {
        'page_title': 'Informations',
    }
    return render(request, 'user/informations.html', context=context)
def login(request):
    context = {
        'page_title': 'Login',
    }
    if request.method == 'POST':
        data = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        person = Person()
        user = person.login(data=data)
        if user['status'] == 'Success':
            request.session['user'] = user.get('data').get('user')
            return redirect('index')
        else:
            context['message'] = user.get('message')
            return render(request, 'user/login.html', context=context)
    return render(request, 'user/login.html', context=context)

def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('user:login')
