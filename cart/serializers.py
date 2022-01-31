from rest_framework import serializers
from . import models

class UserCartSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.UserCart
		fields 	= '__all__'

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.Order
		fields 	= '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.OrderDetail
		fields 	= '__all__'