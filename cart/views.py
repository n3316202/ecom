from urllib import response
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    print(quantities , "==============")
    return render(request, "cart_summary.html",{"cart_products": cart_products,"quantities": quantities})

def cart_add(request):
    
    cart  = Cart(request)

    print("카트========",cart)

    if request.POST.get('action') == 'post':
        print('=========')
        
        #get stuff
        product_id = int(request.POST.get('product_id'))
        print('product_id', product_id)
        
        product_qty = int(request.POST.get('product_qty'))
        # lookup proudct in DB
        product = get_object_or_404(Product,id=product_id)

        print("프로덕트",product)

        #save to session
        cart.add(product=product, quantity = product_qty)

        #Get Cart Quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})

        return response
    
    print("카트========마지막")

def cart_delete(request):
    pass

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        print('=========')
        
        #get stuff
        product_id = int(request.POST.get('product_id'))
        print('product_id =============== ', product_id)


        product_qty = int(request.POST.get('product_qty'))
        print('product_qty ===========', product_qty)

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        return response
    
