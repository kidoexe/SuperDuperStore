from django.db import models
from config.util_models.models import TimeStampdModel
from products.choices import Currency
from django.core.validators import MaxValueValidator

class Product(TimeStampdModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.Gel)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class ProductTag(TimeStampdModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='product_tags')

    def __str__(self):
        return self.name

class Review(TimeStampdModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        unique_together = ['product', 'user']
        
    def __str__(self):
        return f"{self.user} - {self.product} - {self.rating}"

class Cart(TimeStampdModel):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.user}"

class FavoriteProduct(TimeStampdModel):
    product = models.ForeignKey('products.Product', related_name='favorite_products', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='favorite_products', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.product}"

class ProductImage(TimeStampdModel):
    product = models.ForeignKey('products.Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image {self.product}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_of_addition = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} items"
    
    def total_price(self):
        return self.quantity * self.price_at_time_of_addition