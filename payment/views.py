from urllib import response
from django.shortcuts import get_object_or_404, render
from cart.cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

from payment.forms import ShippingForm
from payment.models import ShippingAddress


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:

        shipping_user = ShippingAddress.objects.get(id=request.user.id)
        # checkout as logged in user
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )
    else:
        # checkout as guest
        shipping_form = ShippingForm(request.POST or None)

        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )


# Create your views here.
# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html", {})
