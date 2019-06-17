# models.py
from django.db import models
 
class Test(models.Model):
    name = models.CharField(max_length=100)


class phone(models.Model):
    link = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    comment= models.CharField(max_length=100)
    img_url = models.CharField(max_length=200)