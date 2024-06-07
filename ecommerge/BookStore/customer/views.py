from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer

# Create your views here.
def detailsCustomer(req, id):
    customer = Customer.objects.get(id=id)
    content = {'customer': customer}
    return render(req, 'customer/details_customer.html', content)

def allCustomer(req):
    customers = Customer.objects.all()
    content = {'customers': customers}
    return render(req, 'customer/customers.html', content)
