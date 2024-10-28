from django.shortcuts import render
from .models import Product

from PIL import Image
from pathlib import Path
from django.conf import settings
import os


def home(request):
    products = Product.objects.all()
    print(products)
    
    image_size_change_products()

    return render(request,'home.html',{'products': products})

def image_size_change_products():

    products = Product.objects.all()
    path_dir = os.path.join(settings.BASE_DIR, '')
    
    print(path_dir)
    print(os.path.abspath(settings.MEDIA_URL))

    for product in products:
        try:
            fname = os.path.join(path_dir, product.image.path)
            print(fname)
            img = Image.open(fname)
            re_img = img.resize((450,300), Image.LANCZOS)  # Image.ANTIALIAS
            re_img.save(fname, quality=100)
            print("success : " + str(fname))
        except Exception as e:
            print(e)
            pass

def image_size_change():

    path_dir = os.path.join(settings.MEDIA_URL, '')
    print(path_dir)

    for fname in Path(path_dir).iterdir():
        try:
            img = Image.open(fname)
            re_img = img.resize((450,300), Image.LANCZOS)  # Image.ANTIALIAS
            re_img.save(fname, quality=100)
            print("success : " + str(fname))
        except Exception as e:
            print(e)
            pass