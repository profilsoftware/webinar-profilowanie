from django.core.management.base import BaseCommand, CommandError
from example_app.models import Product, Company

import faker


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        fake = faker.Faker()
        companies = []
        for i in range(100):
            companies.append(Company(name=fake.company()))
        Company.objects.bulk_create(companies)

        products = []
        categories = [Product.FOOD, Product.CLOTHES, Product.ELECTRONICS]
        companies = Company.objects.all()
        for i in range(10000):
            product = Product(
                name=f"{fake.color_name()} {fake.word()}",
                price=fake.pydecimal(right_digits=2, positive=True, max_value=1000),
                company=fake.random.choice(companies),
                category=fake.random.choice(categories),
                is_available=fake.pybool()
            )
            products.append(product)
        Product.objects.bulk_create(products)
