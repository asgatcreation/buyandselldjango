from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import secrets
from .paystack import Paystack

# Create your models here.

class Payment(models.Model):
    price = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self) -> str:
        return f"Payment: {self.amount}"
    
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        
        super().save(*args, **kwargs)
        
    def amount_value(self) -> int:
        return self.amount*100
    
    
    
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.price)
        if status:
            if result['amount']/100 ==self.price:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False