from django.shortcuts import redirect, render
from .models import Product

from PIL import Image
from pathlib import Path
from django.conf import settings
import os

#로그인 로그아웃 관련
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages

def register_user(request):
    return render(request, 'register.html',{})

def home(request):
    products = Product.objects.all()
    print(products)
    
    image_size_change_products()

    return render(request,'home.html',{'products': products})

def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request,"You Have been logged in")
            return redirect('home')
        else:
            messages.success(request,("There was an error, please try again"))
            return redirect('login')
    else:    
        return render(request, 'login.html',{})
    

def logout_user(request):
    logout(request)
    return redirect('home')


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