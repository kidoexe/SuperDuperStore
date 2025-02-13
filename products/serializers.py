from rest_framework import serializers 
from products.models import Review, Product, Cart, ProductTag , FavoriteProduct

class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['product_id', 'content', 'rating']

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
        return Review.objects.create(product=product, user=user, **validated_data)
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']


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


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'product', 'tag_name']

class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    Product_id = serializers.IntegerField(write_only = True)

    class Meta:
         model = FavoriteProduct
         fields = ['id', 'user', 'product_id', 'product']
         read_only_fields = ['id', 'product']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("given prduct_id doesnt exist")
        return value
    def create(self, validated_data):
        user = validated_data.pop('user')
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)

        favorite_product, created = FavoriteProduct.objects.get_or_create(user = user, product = product)

        if not created:
            raise serializers.ValidationError("product with given id is already in favorites")
        return favorite_product



# #class ReviewSerializer(serializers.ModelSerializer):
#     product_id = serializers.IntegerField(write_only=True)

#     class Meta:
#         model = Review
#         fields = ['id', 'product_id', 'content', 'rating']

#     def validate_product_id(self, value):
#         try:
#             Product.objects.get(id=value)
#         except Product.DoesNotExist:
#             raise serializers.ValidationError("Invalid product_id. Product does not exist.")
#         return value

#     def validate_rating(self, value):
#         if value < 1 or value > 5:
#             raise serializers.ValidationError("Rating must be between 1 and 5.")
#         return value

#     def create(self, validated_data):
#         product = Product.objects.get(id=validated_data['product_id'])
#         user = self.context['request'].user

#         review = Review.objects.create(
#             product=product,
#             user=user,
#             content=validated_data['content'],
#             rating=validated_data['rating'],
#         )
#         return review