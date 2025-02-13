from django.shortcuts import render
from rest_framework.decorators import api_view
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
    serializer_class = FavoriteProductSerializer
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
 







#  #@api_view(['GET', 'POST'])
# def product_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data) 
    
#     elif request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             product = serializer.save()
#             return Response({'id': product.id}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def review_view(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response({'reviews': serializer.data}) 
    
#     elif request.method == 'POST':
#         serializer = ReviewSerializer(data=request.data, context={"request": request})
#         if serializer.is_valid():
#             review = serializer.save()
#             return Response({'id': review.id, 'message': 'Review created successfully!'},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def cart_view(request):
#     if request.method == 'GET':
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         products = cart.products.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response({'cart': serializer.data})
    
#     elif request.method == 'POST':
#         product_id = request.data.get('product_id')
#         quantity = request.data.get('quantity', 1)
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart.products.add(product)
#         return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# def product_tag_view(request):
#     if request.method == 'GET':
#         product_id = request.query_params.get('product_id')
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
#         tags = product.tags.all()
#         tag_names = [tag.name for tag in tags]
#         return Response({'tags': tag_names})
    
#     elif request.method == 'POST':
#         product_id = request.data.get('product_id')
#         tag_name = request.data.get('tag_name')
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
#         tag, created = ProductTag.objects.get_or_create(name=tag_name)
#         product.tags.add(tag)
#         return Response({'message': 'Tag added to product'}, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'POST'])
# def favorite_product_view(request):
#     if request.method == 'GET':
#         favorites = FavoriteProduct.objects.filter(user=request.user)
#         products = [fav.product for fav in favorites]
#         serializer = ProductSerializer(products, many=True)
#         return Response({'favorites': serializer.data})
    
#     elif request.method == 'POST':
#         product_id = request.data.get('product_id')
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
#         FavoriteProduct.objects.get_or_create(user=request.user, product=product)
#         return Response({'message': 'Product added to favorites'}, status=status.HTTP_201_CREATED)