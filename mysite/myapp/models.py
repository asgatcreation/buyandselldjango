from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price  = models.IntegerField()
    desc = models.CharField(max_length=300)
    image = models.ImageField(blank=True, upload_to='images')
    

    def __str__(self):
        return self.name 

    # def __unicode__(self):
    #     return 



