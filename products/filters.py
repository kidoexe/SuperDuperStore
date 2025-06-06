from django_filters import FilterSet, NumberFilter
from products.models import Product, Review

class ProductFilter(FilterSet):
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model  = Product
        fields = ['categories', 'price_min', 'price_max']

class ReviewFilter(FilterSet):
    rateing_min = NumberFilter(field_name='rating', lookup_expr="gte")
    rateing_max = NumberFilter(field_name='rating', lookup_expr="lte")

    class Meta:
        model = Review
        fields = ['rating']