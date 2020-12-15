from django.db import models

# Create your models here.
from django.db.models import BooleanField, CharField, DecimalField, ForeignKey, CASCADE


class Company(models.Model):
    name = CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    ELECTRONICS = 'electronics'
    CLOTHES = 'clothes'
    FOOD = 'food'
    name = CharField(max_length=100)
    category = CharField(max_length=20, choices=[(ELECTRONICS, ELECTRONICS), (CLOTHES, CLOTHES), (FOOD, FOOD)])
    price = DecimalField(max_digits=5, decimal_places=2)
    company = ForeignKey(Company, on_delete=CASCADE)
    is_available = BooleanField(default=True)
