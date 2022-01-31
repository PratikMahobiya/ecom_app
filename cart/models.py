from django.db import models
from users.models import User
from store.models import Product

class UserCart(models.Model):
    user_id 				= models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='User Id')
    product_id              = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Product Id')
    quantity                = models.PositiveBigIntegerField(verbose_name='Quantity',default=1)
    created_on              = models.DateTimeField(auto_now_add=True)
    modefied_on             = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class Order(models.Model):
    user_id 				= models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='User Id')
    bill_no                 = models.AutoField(primary_key=True,verbose_name='Bill No.')
    first_name              = models.CharField(max_length=100,verbose_name='First Name')
    last_name               = models.CharField(max_length=100,verbose_name='Last Name')
    mobile   				= models.BigIntegerField(verbose_name='Contact Number')
    address     			= models.TextField(verbose_name='Address')
    amount            		= models.FloatField(verbose_name='Order_amount')
    no_of_items        		= models.PositiveBigIntegerField(verbose_name='Number Of Items')
    order_date              = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.bill_no)

class OrderDetail(models.Model):
    bill_no                 = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='Bill No')
    item_name               = models.CharField(max_length=100,verbose_name='Item Name')
    quantity     			= models.PositiveBigIntegerField(verbose_name='Quantity')
    mrp                		= models.FloatField(verbose_name='MRP/Quantity')
    total                 	= models.FloatField(verbose_name='Total')
    order_date              = models.DateTimeField(auto_now_add=True)