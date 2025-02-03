from django.urls import path, include
from products.views import *

urlpatterns = [
    path('products/', products_view, name='products'),
    path('cart/', cart_view, name='cart'),
    path('product-tags/', product_tag_view, name='product-tags'),
    path('favorite-products/', favorite_product_view, name='favorite-products'),
    path('products/<int:pk>/', get_product, name='product', ),
]
