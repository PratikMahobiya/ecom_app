from cart.models import OrderDetail, Order
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

def get_invoice(request):
	invoice_data = Order.objects.get(bill_no = request.GET.get('bill_no'))
	items = OrderDetail.objects.get(bill_no = request.GET.get('bill_no'))
	return render(request, "invoice_template.html", context={'invoice': invoice_data ,'items':items})