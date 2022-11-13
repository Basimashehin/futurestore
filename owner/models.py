
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import date,timedelta

# Create your models here.
class Categories(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.category_name


class Products(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images",null=True)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=250,null=True)
    def __str__(self) -> str:
        return self.product_name


class Carts(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True,null=True)
    options=(
        ("in_cart","in_cart"),
        ("order_placed","order_placed"),
        ("cancelled","cancelled")
        )
    status=models.CharField(max_length=120,choices=options,default="in_cart")
    qty=models.PositiveIntegerField(default=1)


class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True,null=True)
    options=(
         ("order_placed","order_placed"),
          ("dispatched","dispatched"),
           ("in_transit","in_transit") ,
           ("delivered","delivered"),
            ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="order_placed")
    delivery_address=models.CharField(max_length=200,null=True)
    expected_delivery_date=models.DateField(null=True,)


class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.CharField(max_length=120)
    rating=models.PositiveIntegerField()

