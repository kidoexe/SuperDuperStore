from rest_framework import serializers 
from products.models import *
class ProductTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductTag
        fields = ['id', 'name']
class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_id', 'product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user = self.context['request'].user

        exisiting_reviews = Review.objects.filter(user = user, product = product)
        if exisiting_reviews.exists():
            raise serializers.ValidationError('You already have review on this product U stupid nigger')
        
        return Review.objects.create(product=product, user=user, **validated_data)   
    
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        source = 'tags',
        queryset= ProductTag.objects.all(),
        many = True,
        write_only = True,
    )
    tags = ProductTagSerializer(many = True, write_only = True)
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        product = product.objects.create(**validated_data)   
        product.tags.set(tags) 
        return product
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)
        return super().update(instance, validated_data)

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    products = ProductSerializer(many = True, read_only = True)
    products_ids = serializers.PrimaryKeyRelatedField(
    source='products',
    queryset=Product.objects.all(),
    write_only = True,
    many = True,
    )
    class Meta:
        model = Cart
        fields = ['product_ids', 'user', 'product',]

    def create(self, validated_data):
        user = validated_data.pop('user')
        products = validated_data.pop('products')

        cart, _ = Cart.objects.get_or_create(user = user)
    
        cart.products.add(*products)

        return cart

class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    Product_id = serializers.IntegerField(write_only = True)

    class Meta:
         model = FavoriteProduct
         fields = ['id', 'user', 'product_id', 'product']
         read_only_fields = ['id', 'product']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("given product_id doesnt exist")
        return value
    def create(self, validated_data):
        user = validated_data.pop('user')
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)

        favorite_product, created = FavoriteProduct.objects.get_or_create(user = user, product = product)

        if not created:
            raise serializers.ValidationError("product with given id is already in favorites")
        return favorite_product

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity',
                  'price_at_time_of_addition', 'total_price']
        read_only_fields = ['price_at_time_of_addition']
    
    def get_total_price(self, obj):
        return obj.total_price()
    
    def create(self, validated_data):
        product = validated_data.get('product')
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user)
        validated_data['cart'] = cart
        validated_data['price_At_time_of_addition'] = product.price

        return super().create(validated_data)

    def update(self, instance, validated_data):
        quantity = validated_data.pop('quantity')
        instance.quantity = quantity
        instance.save()
        return instance                

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total']
    
    def get_total(self, obj):
        return sum(item.total_price() for item in obj.items.all() if item.total_price())