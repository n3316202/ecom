from ast import mod
from itertools import product
from pickletools import decimalnl_short
from django.db import models
from django.contrib.auth.models import User

from store.models import Product

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True,blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True,blank=True)
    shipping_country = models.CharField(max_length=255)

    # Dont' plurallize address
    #어드민 패널을 만지다 보면 내가 등록한 모델 이름을 장고 어드민이 알아서 복수로 만들어 주는 것을 알 수 있다. 그럴때 가끔 -y 로 끝나는 단어의 끝에도 그냥 s를 붙이는 경우가 있는데, 이때 메타 클래스의 verbose_name을 이용해서 바꿔줄 수 있다.
    
    class Meta:
        verbose_name_plural = "Shipping Address"
    
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    

# Create order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2) #$12.56
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Order - {str(self.id)}'
  

# Create order Items Model

class OrderItem(models.Model):
    #Forign Keys
    order = models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)

    quantity = models.PositiveBigIntegerField(default=1) #양수: PositiveBigIntegerField, 4바이트 정수 필드 (unsigned).
    price = models.DecimalField(max_digits=7,decimal_places=2) #최대 숫자 자리수:7 최대 소수점 자리수 : 2

    def __str__(self) -> str:
        return f'Order Item - {str(self.id)}'




