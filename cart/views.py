from urllib import response
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    totals = cart.cart_total()
    print(quantities, "==============")
    return render(
        request,
        "cart_summary.html",
        {"cart_products": cart_products, "quantities": quantities, "totals": totals},
    )


def cart_add(request):

    cart = Cart(request)

    print("카트========", cart)

    if request.POST.get("action") == "post":
        print("=========")

        # get stuff
        product_id = int(request.POST.get("product_id"))
        print("product_id", product_id)

        product_qty = int(request.POST.get("product_qty"))
        # lookup proudct in DB
        product = get_object_or_404(Product, id=product_id)

        print("프로덕트", product)

        # save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        response = JsonResponse({"qty": cart_quantity})
        messages.success(request, "Product Added To Cart...")

        return response

    print("카트========마지막")


def cart_delete(request):
    pass


def cart_update(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        print("=========")

        # get stuff
        product_id = int(request.POST.get("product_id"))
        print("product_id =============== ", product_id)

        product_qty = int(request.POST.get("product_qty"))
        print("product_qty ===========", product_qty)

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({"qty": product_qty})
        messages.success(request, "Your Cart Has benn Updated...")
        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        print("=========")

        # get stuff
        product_id = int(request.POST.get("product_id"))
        print("product_id =============== ", product_id)

        cart.delete(product=product_id)

        response = JsonResponse({"product": product_id})
        messages.success(request, "Item Deleted From Shopping Cart...")
        return response
