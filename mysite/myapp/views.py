import math
import random
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import requests
import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

from django.shortcuts import render,  redirect
from django.http import HttpResponse
from requests import session

from .forms import PaymentForm
from . import views
from .models import Product, OrderDetail, CustomerInfo
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator 
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import paystack







# Create your views here.

def index(request):
    return HttpResponse("Hello World") 


def products(request):
    page_obj = products = Product.objects.all()
    
    product_name = request.GET.get('product_name')
    if product_name!='' and product_name is not None:
        page_obj = products.filter(name__icontains=product_name)
        
    paginator = Paginator(page_obj,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={
        'page_obj':page_obj
    }
    return render(request, 'myapp/index.html', context)
#        'page_obj':page_obj
#not needed again   'products': products
#  'page_obj': page_obj
######VIEW FOR LIST PRODUCTS INITIALLLY

# def products(request):
#     products = Product.objects.all()
#     context ={
#         'products': products
#     }
#     return render(request, 'myapp/index.html', context)
############# FUNCTION BASE

# now change products to page_obj on the for product in products in index
#not there
    #products = ["iphone","imac","ipads"]
    #return HttpResponse(products)
    #return HttpResponse("<h1>List of products</h1>")
    
  #class based view for above product [lstview]

# class ProductListView(ListView):
#     model = Product
#     product_name = request.GET.get('product_name')
#     products.filter(name__icontains = product_name)
#     template_name = 'myapp/index.html'
#     context_object_name =  'products'
#     paginate_by = 6
      


     
def product_detail(request,id):
    product = Product.objects.get(id=id)
    # if request.method=='POST':
    #     form = PaymentForm(request.POST)
    #     if form.is_valid():
    #         name=  form.cleaned_data['name']
    #         email = form.cleaned_data['email']
    #         price = form.cleaned_data['amount']
    #         phone = form.cleaned_data['phone']
    #         return redirect(str(process_payment(name,email,price,phone)))
    
    # else:
    #     form = PaymentForm()
    
    context={
        'product':product,
 #       'form':form
    }
    return render(request,'myapp/detail.html', context )
    
    #class based view for detail view
    
# class ProductDetailView(DetailView):
#     model = Product
#     template_name='myapp/detail.html'
#     context_object_name = 'product'
#     pk_url_kwarg = 'pk'
    
    
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView,self).get_context_data(**kwargs)
#         context['paystack_public_key'] = settings.PAYSTACK_PUBLIC_KEY
#         return context
        
        
    
    
    

@login_required
def add_product(request):
    if request.method=='POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        seller_name = request.user
        product = Product(name=name, price=price,desc=desc,image=image, seller_name=seller_name)
        product.save()
        return redirect('myapp:mylistings')
    return render(request, 'myapp/addproduct.html')

#class based view for creting product

#@login_required
# class ProductCreateView(CreateView):
#     model = Product
#     fields = ['name','price','desc','image','seller_name']
    #product_form.html
    
    #template_name = "myapp/addproduct.html"


#@login_required
def update_product(request, id):
    
    product = Product.objects.get(id=id)
    if request.method=='POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.desc = request.POST.get('desc')
        product.image = request.FILES['upload']
        #product = Product(name=name, price=price,desc=desc,image=image)
        product.save()
        return redirect('myapp:mylistings')
        #product=Product.objects.get(id=id)
    context={
        'product':product,
    }    
    return render(request, 'myapp/updateproduct.html',context)



# class ProductUpdateView(UpdateView):
#     model = Product
#     fields = ['name','price','desc','image','seller_name']
#     template_name_suffix = '_update_form'
    #product_form.html
    


#@login_required
def delete_product(request,id):
    product = Product.objects.get(id=id)
    context={
        'product':product,
    }
    if request.method=='POST':
        product.delete()
        #return redirect('/myapp/products')
        return redirect('myapp:mylistings')
    return render(request,'myapp/delete.html',context)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('myapp:mylistings')
    
    #template_name = "TEMPLATE_NAME"



def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context={
        'products':products,
    }
    return render(request,'myapp/mylistings.html',context)
    

@csrf_exempt
def create_checkout_session(request,id):
    product = get_object_or_404(Product,pk=id)
    paystack.api_key = settings.PAYSTACK_SECRET_KEY
    checkout_session = paystack.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'naira',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':int(product.price*100),
                },
                'quantity':1
            }
        ],
        mode = 'payment',
        success_url = request.build_absolute_url(reverse('myapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_url(reverse('myapp:failed')),
           
        
    )
    
    order = OrderDetail()
    order.customer_username = request.user.username
    order.product = product
    order.paystack_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price*100)
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})



class PaymentSuccessView(TemplateView):
    template_name = "myapp/payment_success.html"
    
    def get(self,request,*args,**kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        paystack.checkout.Session.retrieve(session_id)
        paystack.api_key = settings.PAYSTACK_SECRET_KEY
        order = get_object_or_404(OrderDetail,paystack_payment_intent = session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)
    

class PaymentFailedView(TemplateView):
    template_name = "myapp/payment_failed.html"
    
    
def process_payment(name,email,amount,phone):
     auth_token= env('SECRET_KEY')
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"KES",
                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"card",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Supa Electronics Store",
                    "description":"Best store in town",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')    


# def customer_info(request):
#     if request.method == 'POST':
#         customer_form = CustomerInfoForm(request.method)
#         if customer_form.is_valid()and customer_form.cleaned_data:
#             customer_form.save()
#             return render(request, 'template_folder/payment.html
#                           {'email':customer_form.email})
#         else:
#             return HttpResponse('Invalid input try again!!!')
#     else:
#         customer_form = CustomerInfoForm()
#    return render(request, 'template_folder/customer_info.html
#                     {'customer_form': customer_form})




