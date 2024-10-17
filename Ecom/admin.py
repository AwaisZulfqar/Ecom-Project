from django.contrib import admin
from .models import Customer,Product,Brand,Cart,Shipping,Payment,Contact,Review,OrderProduct
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','user','name','email','location','state')
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','brand','category','title','image','price','discounted_price','description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','quantity',)

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','first_name','last_name','company_name','area_code',
                    'primary_phone','street_address','zip_code','buisness_address')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','holder_name','card_number','expiry_month','expiry_year','CSC')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','subject','message')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','name','title','review','created_at')


@admin.register(OrderProduct)
class OrderProductDetails(admin.ModelAdmin):
    list_diaplay = ['user', 'image', 'product', 'discounted_price', 'quantity','title']