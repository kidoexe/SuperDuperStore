from django.urls import path, include
from products.views import *

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='products'),
    path('products/<int:pk>/', ProductListCreateView.as_view(), name='product', ),
    path('reviews', ReviewViewSet.as_view(), name='reviews'),


    path('favorite-products/', Favorite_product_view.as_view(), name='favorite-products'),
    path('favorite-products/<int:pk>/', Favorite_product_view.as_view(), name='favorite-products'),

    path('cart/', CartViewSet.as_view(), name='cart'),
   
   path('product-tags/', ProductTagListView.as_view(), name='tags'),

   path('products/<int:product_id>/images/', ProductImageViewSet.as_view(), name='images'),
   path('products/<int:product_id>/images/<int:pk>/', ProductImageViewSet.as_view(), name='images')
]

