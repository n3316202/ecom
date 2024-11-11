from django.shortcuts import render



def checkout(request):
    return render(request, "payment/checkout.html",{})

# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html",{})