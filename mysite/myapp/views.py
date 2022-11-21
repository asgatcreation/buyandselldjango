from django.shortcuts import render
from django.http import HttpResponse
from . import views
from .models import Product

# Create your views here.

def index(request):
    return HttpResponse("Hello World") 

def products(request):
    products = Product.objects.all()
    context ={
        'products': products
    }
    return render(request, 'myapp/index.html', context)
    #products = ["iphone","imac","ipads"]
    #return HttpResponse(products)
    #return HttpResponse("<h1>List of products</h1>")
    
def product_detail(request,id):
    product = Product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request,'myapp/detail.html', context )
    #return HttpResponse('The product id is:'+ str(id))

def add_product(request):
    if request.method=='POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        product = Product(name=name, price=price,desc=desc,image=image)
        product.save()
    return render(request, 'myapp/addproduct.html')

def update_product(request, id):
    return render(request, 'myapp/updateproduct.html')