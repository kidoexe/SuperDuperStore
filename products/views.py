from rest_framework.response import Response
from products.models import Product, Cart, ProductTag, FavoriteProduct, Review
from rest_framework import status
from products.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

class ProductListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
           return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
        
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
       
    def put(self, request, *args, **kwargs ):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ReviewViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs ):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs ):
        return self.update(request, *args, **kwargs)

class DeteiledProductViewUpdate(APIView):   
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        obj = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
 

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class ProductTagAPIView(APIView):
    def get(self, request):
        product_id = request.query_params.get('product_id')
        tags = ProductTag.objects.filter(product_id=product_id)
        serializer = ProductTagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Favorite_product_view(ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericAPIView):
 queryset = FavoriteProduct.objects.all()
 serializer_class = FavoriteProductSerializer
 permission_classes = [IsAuthenticated]

 def get_queryset(self):
     queryset = self.queryset.filter(user=self.request.user)
     return queryset
 
 def get(self, request, pk=None, *args, **kwargs):
    if pk:
        return self.retrieve(request, *args, **kwargs)
    return self.list(request, *args, **kwargs)
 

 def post(self, request, *args, **kwargs):
     return self.create(request, *args, **kwargs)
 
 def delete(self, request, *args, **kwargs):
     return self.destroy(request, *args, **kwargs)   
 
class ProductTagListView(ListModelMixin, GenericAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ProductImageViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset.filter(product__id = self.kwargs['product_id'])
    def get(self, request, pk = None, *args, **kwargs):
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)   
 
