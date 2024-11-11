from urllib import response
from django.shortcuts import get_object_or_404, render
from cart.cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages



def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    print("아아",quantities)
    return render(request, "payment/checkout.html",{"cart_products": cart_products,"quantities": quantities,"totals":totals})


# Create your views here.
# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html",{})