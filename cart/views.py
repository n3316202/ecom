from urllib import response
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(reqeust):
    return render(reqeust, "cart_summary.html",{})

def cart_add(reqeust):
    cart  = Cart(reqeust)
    if reqeust.POST.get('action') == 'POST':
        #get stuff
        product_id = int(reqeust.POST.get('prodcut_id'))
        # lookup proudct in DB
        prodcut = get_object_or_404(Product,id=product_id)

        #save to session
        cart.add(prodcut=prodcut)
        response = JsonResponse({'Product Name': prodcut.name})
        
        return response

def cart_delete(reqeust):
    pass

def cart_update(reqeust):
    pass

