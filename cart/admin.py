from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('user_id','product_id','quantity','created_on','modefied_on')
    list_per_page = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bill_no','status','payment_status','user_id','first_name','last_name','mobile','address','amount','no_of_items','order_date','razorpay_order_id','razorpay_payment_id','razorpay_signature')
    readonly_fields = ('bill_no','user_id','first_name','last_name','mobile','address','amount','no_of_items','order_date','razorpay_order_id','razorpay_payment_id','razorpay_signature')
    list_per_page = 10
    search_fields = ['bill_no','user_id']

@admin.register(models.OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('bill_no_id','item_name','quantity','mrp','total','order_date')
    readonly_fields = ('bill_no','item_name','quantity','mrp','total','order_date')
    list_per_page = 10
    search_fields = ['item_name']