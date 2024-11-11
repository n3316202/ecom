from turtle import back
from unicodedata import category
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender,instance, created, **kwargs):    
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
    

post_save.connect(create_profile,sender=User)


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    #vrbose_name_plural
    #어드민 패널을 만지다 보면 내가 등록한 모델 이름을 장고 어드민이 알아서 복수로 만들어 주는 것을 알 수 있다. 
    #그럴때 가끔 -y 로 끝나는 단어의 끝에도 그냥 s를 붙이는 경우가 있는데, 이때 메타 클래스의 verbose_name을 이용해서 바꿔줄 수 있다.
    class Meta:
        verbose_name_plural = 'categories'

    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6) #9999.99
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=250,default='',blank=True, null=True)
   
	# 업로드 파일의 경로		#업로드 파일의 파일 이름
    # <img src="{{ article.image.url }}" alt="{{ article.image }}">
    image = models.ImageField(upload_to='upload/product')
    
    # Add Sale Stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=6) #9999.99


    def __str__(self):
        return self.name

#Coustomer orders
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20,default='',blank=True)
    date = models.DateField(default = datetime.today)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.product