from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product, Cart, ProductTag, FavoriteProduct, Review
from rest_framework import status
from  products.serializers import *
from django.shortcuts import get_object_or_404

@api_view(['GET',"POST"])
def products_view(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'id': product.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def cart_view(request):
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        cart_items = Cart.objects.filter(user_id=user_id)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def product_tag_view(request):
    if request.method == 'GET':
        product_id = request.query_params.get('product_id')
        tags = ProductTag.objects.filter(product_id=product_id)
        serializer = ProductTagSerializer(tags, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def favorite_product_view(request):
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        favorites = FavoriteProduct.objects.filter(user_id=user_id)
        serializer = FavoriteProductSerializer(favorites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FavoriteProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])   
def get_product(request, pk):
        product = get_object_or_404(Product, pk = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

