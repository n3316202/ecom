from django.shortcuts import redirect, render

from store.forms import SignUpForm
from .models import Category, Product

from PIL import Image
from pathlib import Path
from django.conf import settings
import os

#로그인 로그아웃 관련
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages

def category(request, foo):
    #Replace Hyphens with Spaces

    foo = foo.replace('-',' ')
    print(foo)

    # Grab the category from the url
    try:
        #Look up the category
        category = Category.objects.get(name=foo)
        print(category)
        
        products = Product.objects.filter(category=category)
        print(products)
        
        return render(request, 'category.html',{'products':products,'category':category})
    
    except:
        messages.success(request, ("That Category Does't ex"))        
        return redirect('home')
    

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def register_user(request):
    print("register.. 실행")
    
    if request.method == "POST":
        print("register.. 실행.....")
        form = SignUpForm(request.POST)

        if form.is_valid():
            print(form)
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,('You Have Registered'))
            return redirect('home')
        else:
            print(form.errors)
            for field in form:
                print("Field Error:",  field.errors)

            messages.success(request,('Whoops! There was a problem Registering, Please Try again'))
            return redirect('register')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html',{'form':form})


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