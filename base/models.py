from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='products')
    star = models.FloatField(default=5.00)
    price = models.IntegerField(default=100)

class Cat(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='cats')


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)
    balance = models.FloatField(default=00)
    refer_link = models.IntegerField()
    team = models.ManyToManyField(User, related_name='teams', null=True, blank=True)

    def __str__(self):
        return self.number