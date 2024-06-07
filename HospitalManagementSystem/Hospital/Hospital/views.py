from django.shortcuts import render

def index(request):
    context = {
        'page_title': 'home',
    }
    return render(request, 'home.html', context=context)