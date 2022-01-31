from store.models import Product
from django.shortcuts import render

# Create your views here.
def Index(request):
	return render(request, "index.html")

def Checkout(request):
	return render(request, "checkout.html")

def Order(request):
	return render(request, "order.html")

def single_page(request):
	return render(request, "single.html")