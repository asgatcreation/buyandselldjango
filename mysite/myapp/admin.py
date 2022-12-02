from django.contrib import admin
from .models import Product

# Register your models here.

admin.site.site_header = "BuyitSellit ecommerce"
admin.site.site_title = "Buyit stores"
admin.site.index_title= "Manage BuyitSellit ecommerce site"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','desc','seller_name',)
    search_fields = ('name',)
    #search_fields = ('price',)
    
    def set_price_to_zero(self,request,queryset): 
        queryset.update(price=0)
        
    actions = ('set_price_to_zero',)
    
    list_editable = ('price','desc')  
    # def thirty_percent_discount(self,request,queryset): 
    #     queryset.update(price=30/100*price)
        
    # actions = ('thirty_percent_discount',)
        
    



admin.site.register(Product,ProductAdmin)