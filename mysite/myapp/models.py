from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import secrets

# Create your models here.

class Product(models.Model):
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price  = models.IntegerField()
    desc = models.CharField(max_length=300)
    image = models.ImageField(blank=True, default='product.jpg', upload_to='images')
    

    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse('myapp:mylistings')

    # def __unicode__(self):
    #     return 



class OrderDetail(models.Model):
    customer_username = models.CharField(max_length=200)
    product = models.ForeignKey(to='Product', on_delete=models.PROTECT)
    #email = models.EmailField()
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add=True)
    updted_on = models.DateTimeField(auto_now_add=True)


class CustomerInfo(models.Model):
    full_name= models.CharField(max_length  = 150)
    email= models.EmailField()
    phone_number = models.CharField(max_length= 20)
    address = models.CharField(max_length = 150)
    
# class Payment(models.Model):
#     amount = models.PositiveIntegerField()
#     ref = models.CharField(max_length=200)
#     email = models.EmailField()
#     verified = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ('-date_created',)
        
#     def __str__(self) -> str:
#         return f"Payment: {self.amount}"
    
    
#     def save(self, *arg, **kwargs):
#         while not self.ref:
#             ref = secrets.token_urlsafe(50)
#             object_with_similar_ref = Payment.objects.filter(ref=ref)
#             if not object_with_similar_ref:
#                 self.ref = ref
        
#         super().save(*args, **kwargs)
    
    
    

# class CustomerInfo(models.Model):
#     firstname= models.CharField(max_length  = 150)
#     lastname= models.CharField(max_length  = 150)
#     email= models.EmailField()
#     phonenumber = models.CharField(max_length= 20)
#     amount=models.IntegerField(default=1000)
#     state = models.CharField(default='enter state',max_length = 150)
   
#     def __str__(self):
#         return f'{self.firstname} {self.lastname}'


