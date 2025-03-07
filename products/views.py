
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from products.models import *
from products.serializers import *
from products.filters import ProductFilter, ReviewFilter
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter
from products.pagination import ProductPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle

class ProductViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin, GenericViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = ProductPagination
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

class ReviewViewSet(ModelViewSet):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    def perform_update(self, serializer):
        isinstance = self.get_object()
        if isinstance.user != self.request.user:
            raise PermissionDenied("you cant change this")
        isinstance.delete()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("you cant delete this")
        instance.delete()
class FavoriteProductViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,GenericViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'likes'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
        
class CartViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)    
    
class TagViewSet(mixins.ListModelMixin,
              GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

class ProductImageViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,GenericViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You dont have permission to delete this cart")
        instance.delete()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You dont have permission to update ")
        serializer.save()