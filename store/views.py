from django.http import JsonResponse
from rest_framework import filters, generics, pagination
from . import serializers
from . import models

from rest_framework.decorators import api_view

# Create your views here.
class ProductView(generics.ListAPIView):
	paginator = pagination.PageNumberPagination()
	paginator.page_size = 100
	queryset = models.Product.objects.all().order_by('-created_on')
	serializer_class = serializers.ProductSerializer
	pagination_class = pagination.PageNumberPagination

class ProductSearchView(generics.ListAPIView):
	paginator = pagination.PageNumberPagination()
	paginator.page_size = 1100
	queryset = models.Product.objects.all().order_by('-created_on')
	serializer_class = serializers.ProductSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['product_title','category__category','description']
	pagination_class = pagination.PageNumberPagination

@api_view(['GET',])
def ProductCategoryView(request):
	if request.method == 'GET':
		queryset = models.ProductCategory.objects.all()
		serializer = serializers.ProductCategorySerializer(queryset, many=True)
		return JsonResponse({'status':200, 'data': serializer.data})
	return JsonResponse({'status':401, 'message':'Wrong Method Used.'})

@api_view(['GET',])
def ProductCategoryFilterView(request):
	if request.method == 'GET':
		category = request.GET.get('category', None)
		paginator = pagination.PageNumberPagination()
		paginator.page_size = 1100
		queryset = models.Product.objects.filter(category=category).order_by('-created_on')
		result_page = paginator.paginate_queryset(queryset, request)
		serializer = serializers.ProductSerializer(result_page, many=True)
		return paginator.get_paginated_response(serializer.data)
	return JsonResponse({'status': 401, 'message':'Wrong Method Used.'})

@api_view(['GET',])
def SingleProductView(request):
	if request.method == 'GET':
		product_id = request.GET.get('product_id', None)
		queryset = models.Product.objects.get(id=product_id)
		serializer = serializers.ProductSerializer(queryset)
		return JsonResponse({'status':200, 'data': serializer.data})
	return JsonResponse({'status': 401, 'message':'Wrong Method Used.'})

