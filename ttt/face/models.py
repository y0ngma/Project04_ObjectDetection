from django.db import models

# Create your models here.
class Customers(models.Model):
    objects  = models.Manager() # vs code 오류 제거용
    
    customer_id = models.AutoField(primary_key=True)
    eng_name    = models.CharField(max_length=64)
    han_name    = models.CharField(max_length=16)
    gender      = models.CharField(max_length=1, null=True, blank=True)
    age         = models.CharField(max_length=5, null=True, blank=True)
    regdate     = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Menus(models.Model):
    menu_id     = models.AutoField(primary_key=True)
    menu_name   = models.CharField(max_length=30)
    menu_price  = models.IntegerField()

class Sales(models.Model):
    sales_id    = models.AutoField(primary_key=True)
    customer    = models.ForeignKey(Customers, on_delete=models.CASCADE)
    menu        = models.ForeignKey(Menus, on_delete=models.CASCADE)
    regdate     = models.DateTimeField(auto_now_add=True)