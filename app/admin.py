from django.contrib import admin
from .models import Customer,Product,Cart,Orderplaced

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','categary','product_image'] 

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']       

@admin.register(Orderplaced)
class OrderplacedAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status']