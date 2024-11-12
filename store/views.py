from django.shortcuts import redirect, render
from .models import Category, Product, Profile

from PIL import Image
from pathlib import Path
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart


from payment.forms import ShippingForm
from payment.models import ShippingAddress

#로그인 로그아웃 관련
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.forms import ChangePasswordForm, SignUpForm,UpdateUserForm, UserInfoForm

def search(request):
    #Determin if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) )
        print("서치=======", searched)

        #Test for null
        if not searched:
            messages.success(request,"That Product Does not Exist...")
            return render(request, "search.html",{})
        else:
            return render(request, "search.html",{'searched':searched})
    else:
        return render(request, "search.html",{})
   

def update_info(request):
    
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        
        #Get Current user's shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        #Get original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)

        #Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            #Save shipping form
            shipping_form.save()

            messages.success(request, "Your info has been updated!!")
            return redirect('home')
                
        return render(request, "update_info.html",{'form':form, 'shipping_form':shipping_form})
    else:
         messages.success(request, "You Must be logged In To Access That Page!!")
         return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            #Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request," Your password has been updated")
                login(request,current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html",{'form':form})
    else:
         messages.success(request, "You must be logged In to")
         return redirect('home')

    return render(request, "update_password.html",{})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated!!")
            return redirect('home')
        
        print("유저 폼",user_form)
        return render(request, "update_user.html",{'user_form':user_form})
    else:
         messages.success(request, "You Must be logged In To Access That Page!!")
         return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    print('카테고리', categories)
    return render(request,'category_summary.html',{'categories':categories})

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

            #Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            
            #Get their saved cart from database
            saved_cart = current_user.old_cart

            if saved_cart:
                #Convert to dictionary using JOSN
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart dictionary to our session
                #Get the cart
                cart = Cart(request)
                #Loop thru the cart and add the items from the database
                for key, value in converted_cart.items():
                    print("===========",key,value)
                    #cart.add(product=key,quantity=value)
                    cart.db_add(product=key,quantity=value)

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
    
    #print(path_dir)
    #print(os.path.abspath(settings.MEDIA_URL))

    for product in products:
        try:
            fname = os.path.join(path_dir, product.image.path)
            #print(fname)
            
            img = Image.open(fname)
            re_img = img.resize((450,300), Image.LANCZOS)  # Image.ANTIALIAS
            re_img.save(fname, quality=100)
            #print("success : " + str(fname))
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
            #print("success : " + str(fname))
        except Exception as e:
            print(e)
            pass