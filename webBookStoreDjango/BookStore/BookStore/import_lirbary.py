
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.cart import *
from book.book import *
from mobile.mobile import *
from clothes.clothes import *
import requests
from json import *