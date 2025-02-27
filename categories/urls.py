from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CategoryImageViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('category-images', CategoryImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]