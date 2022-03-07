import razorpay
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import filters, generics, pagination
from . import serializers
from . import models
from store.models import Product
from users.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from ecom_app import settings

razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))
# Create your views here.
class UserCartView(APIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [IsAuthenticated]
	def get(self, request):
		user_id 			= User.objects.get(email = request.user)
		queryset = models.UserCart.objects.filter(user_id = user_id)
		serializer = serializers.UserCartSerializer(queryset, many=True)
		return JsonResponse({'status':200, 'count':len(queryset), 'data': serializer.data})

	def post(self, request):
		user_id 			= User.objects.get(email = request.user)
		product_id 	  = request.data['product_id']
		if len(models.UserCart.objects.filter(user_id=user_id, product_id=product_id)) != 0:
			quantity = models.UserCart.objects.get(user_id=user_id, product_id=product_id).quantity
			models.UserCart.objects.filter(user_id=user_id, product_id=product_id).update(quantity = quantity+1)
			queryset = models.UserCart.objects.filter(user_id = user_id)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':200, 'count':len(queryset), 'data': serializer.data})
		else:
			data = {'user_id': user_id.id,'product_id': product_id}
			serializer = serializers.UserCartSerializer(data=data)
			if not serializer.is_valid():
				return JsonResponse({'status':403, 'errors': serializer.errors})
			serializer.save()
			queryset = models.UserCart.objects.filter(user_id = user_id)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':200, 'count':len(queryset), 'data': serializer.data})
	
	def delete(self, request):
		user_id 			= User.objects.get(email = request.user)
		product_id 	  = request.data['product_id']
		models.UserCart.objects.get(user_id = user_id, product_id=product_id).delete()
		queryset = models.UserCart.objects.filter(user_id = user_id)
		serializer = serializers.UserCartSerializer(queryset, many=True)
		return JsonResponse({'status':200, 'count':len(queryset), 'data': serializer.data})

	def put(self, request):
		user_id 			= User.objects.get(email = request.user)
		product_id 	  = request.data['product_id']
		quantity = models.UserCart.objects.get(user_id=user_id, product_id=product_id).quantity
		if quantity == 1:
			models.UserCart.objects.get(user_id = user_id, product_id=product_id).delete()
			queryset = models.UserCart.objects.filter(user_id = user_id)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':200, 'count':len(queryset), 'data': serializer.data})
		else:
			models.UserCart.objects.filter(user_id=user_id, product_id=product_id).update(quantity = quantity-1)
			queryset = models.UserCart.objects.filter(user_id = user_id)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':200, 'count':len(queryset), 'data': serializer.data})

class OrderView(APIView):
	authentication_classes = [TokenAuthentication,]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		user_id 			= User.objects.get(email = request.user)
		queryset = models.Order.objects.filter(user_id = user_id).order_by('-order_date')
		serializer = serializers.OrderSerializer(queryset, many=True)
		return JsonResponse({'status':200, 'count':len(queryset), 'data': serializer.data})

	def post(self, request):
		user_id 			= User.objects.get(email = request.user)
		product_list_str  = request.data['product_list'][:-1]
		product_list_str_split = product_list_str.split('/')
		product_list = []
		for item in product_list_str_split:
			product_list.append(item.split(','))
		ord_data = {'user_id':user_id.id,
								'first_name':request.POST.get('first_name',''),
								'last_name':request.POST.get('last_name',''),
								'mobile':request.POST.get('mobile',''),
								'address':request.POST.get('address',''),'amount':request.POST.get('amount',''),
								'no_of_items':request.POST.get('no_of_items','')
							}
		Ord_Serializer = serializers.OrderSerializer(data=ord_data)
		if not Ord_Serializer.is_valid():
			return JsonResponse({'status':403, 'errors': Ord_Serializer.errors})
		Ord_Serializer.save()
		res_product = []
		for product in product_list:
			res_product.append([Product.objects.get(id = int(product[0])).product_title,int(product[1]),int(product[2]),int(product[3])])
			ord_det_data = {'bill_no':Ord_Serializer.data['bill_no'],
											'item_name':Product.objects.get(id = int(product[0])).product_title,
											'quantity':int(product[1]),
											'mrp':int(product[2]),
											'total':int(product[3])
										}
			Ord_Det_serializer = serializers.OrderDetailSerializer(data=ord_det_data)
			if not Ord_Det_serializer.is_valid():
				return JsonResponse({'status':403, 'errors': Ord_Det_serializer.errors})
			Ord_Det_serializer.save()
		res_data = {'bill_no':Ord_Serializer.data['bill_no'],
								'first_name':request.POST.get('first_name',''),
								'last_name':request.POST.get('last_name',''),
								'mobile':request.POST.get('mobile',''),
								'address':request.POST.get('address',''),
								'amount':request.POST.get('amount',''),
								'no_of_items':request.POST.get('no_of_items',''),
								'product_list':res_product,
								'order_date': Ord_Serializer.data['order_date']
							}
		order_currency = 'INR'
		callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
		notes = {'order-type': "basic order from the website", 'key':'value'}
		razorpay_order = razorpay_client.order.create(dict(amount=int(request.POST.get('amount',0))*100, currency=order_currency, notes = notes, receipt=Ord_Serializer.data['bill_no'], payment_capture='0'))
		print(razorpay_order['id'])
		order = models.Order.objects.get(bill_no = Ord_Serializer.data['bill_no'])
		order.razorpay_order_id = razorpay_order['id']
		order.save()

		models.UserCart.objects.filter(user_id = user_id).delete()
		return JsonResponse({'status':200, 'data': res_data,'message':'Order is Placed.','order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':request.POST.get('amount',0), 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})

@csrf_exempt
def handlerequest(request):
	if request.method == "POST":
		try:
				payment_id = request.POST.get('razorpay_payment_id', '')
				order_id = request.POST.get('razorpay_order_id','')
				signature = request.POST.get('razorpay_signature','')
				params_dict = { 
				'razorpay_order_id': order_id, 
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
				}
				try:
						order_db = models.Order.objects.get(razorpay_order_id=order_id)
				except:
						return JsonResponse({'status':505})
				order_db.razorpay_payment_id = payment_id
				order_db.razorpay_signature = signature
				order_db.save()
				result = razorpay_client.utility.verify_payment_signature(params_dict)
				if result==None:
					amount = order_db.total_amount * 100   #we have to pass in paisa
					try:
						razorpay_client.payment.capture(payment_id, amount)
						order_db.payment_status = 1
						order_ = order_db.save()
						order_serializer = serializers.OrderSerializer(order_)
						return JsonResponse({'status':200, 'data': order_serializer.data,'message':'Order is Placed.'})
					except:
						order_db.payment_status = 2
						order_db.save()
						return JsonResponse({'status':505, 'data': order_serializer.data,'message':'Order is Placed.'})
				else:
					order_db.payment_status = 2
					order_db.save()
					return JsonResponse({'status':505, 'data': order_serializer.data,'message':'Order is Placed.'})
		except:
				return JsonResponse({'status':505})