from django import forms
from django.contrib.auth.models import User

from payment.models import ShippingAddress



class ShippingForm(forms.ModelForm):
    
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        exclude = ['user']