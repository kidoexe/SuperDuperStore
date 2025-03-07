from django.core.management.base import BaseCommand
import random
from faker import Faker
from products.choices import *
from products.models import Product



faker = Faker()

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        products_to_create = [] 
        currency =[
        Currency.GEL,
        Currency.USD,
        Currency.EURO,
    ]
        for _ in range(1000):
            name = faker.name()
            description = faker.text()
            price = round(random.uniform(1,1000), 0)
            quantity = random.randint(1,100)
            Currency = random.choice(currency)

        product = Product(
            name = name,
            description = description,
            price = price,
            quantity = quantity,
            currency = currency,
        )
        products_to_create.append(product)

        Product.objects.bulk_create(products_to_create, batch_size=100)
        print("created")