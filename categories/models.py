from django.db import models
from config.util_models.models import TimeStampdModel

class Category(TimeStampdModel, models.Model):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('products.Product', related_name='categories')

    

class CategoryImage(TimeStampdModel, models.Model):
    image = models.ImageField(upload_to='categories/')
    category = models.ForeignKey('categories.Category', related_name='images', on_delete=models.CASCADE) 
    is_active = models.BooleanField(default=False)
