from django.urls import path, include
from rest_framework.routers import SimpleRouter
from products.views import *


router = SimpleRouter()


router.register('products', ProductViewSet)
router.register('products/(?P<product_id>\d+)/reviews', ReviewViewSet)
router.register('favorite-products', FavoriteProductViewSet)
router.register('cart', CartViewSet)
router.register('product-tags', ProductTagViewSet)
router.register('products/(?P<product_id>\d+)/images', ProductImageViewSet)


urlpatterns = [
    path('', include(router.urls)),
]