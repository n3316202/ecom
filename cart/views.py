from urllib import response
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    return render(request, "cart_summary.html",{})

def cart_add(request):
    
    cart  = Cart(request)

    print("카트========",cart)

    if request.POST.get('action') == 'post':
        print('=========')
        
        #get stuff
        product_id = int(request.POST.get('product_id'))
        print('product_id', product_id)

        # lookup proudct in DB
        product = get_object_or_404(Product,id=product_id)

        print("프로덕트",product)

        #save to session
        cart.add(product=product)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})

        return response
    
    print("카트========마지막")

def cart_delete(request):
    pass

def cart_update(request):
    pass

