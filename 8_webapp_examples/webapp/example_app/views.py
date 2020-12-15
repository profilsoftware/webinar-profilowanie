from time import sleep

# Create your views here.
from django.shortcuts import render
from .models import Product


def index(request):
    query = Product.objects.all()[:1000]
    return render(request, 'example_app/index.html', {'products': query})
