
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from os import name
from django.contrib import admin
#from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#from .views import list_products, payment_response, product_detail


app_name = 'myapp'
urlpatterns = [
    path('',views.index),
    
    # path('products/', views.ProductListView.as_view(), name='products'),
    path('products/', views.products, name='products'),
     path('products/<int:id>/', views.product_detail, name = 'product_detail'),
     #path('products/<int:id>/details', views.product_detail, name='details'),
    # path('products/<int:pk>/', views.ProductDetailView.as_view(), name = 'product_detail'),
    path('products/add/', views.add_product, name = 'add_product'),
    
    # path('products/add/', views.ProductCreateView.as_view(), name = 'add_product'),
    
    path('products/update/<int:id>/', views.update_product, name = 'update_product'),
    
    # path('products/update/<int:pk>/', views.ProductUpdateView.as_view(), name = 'update_product'),
    path('products/delete/<int:id>/', views.delete_product, name = 'delete_product'),
    
    path('products/mylistings/', views.my_listings, name = 'mylistings'),
    
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name = 'delete_product'),
    path('success/',views.PaymentSuccessView.as_view(), name = 'success'),
    path('failed/',views.PaymentFailedView.as_view(), name = 'failed'),
    path('api/checkout-session/<id>',views.create_checkout_session, name = 'api_checkout_session' ),
    
    # path('customer_info', views.customer_info(),
    #      name='customer_info')
    
]
 