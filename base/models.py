from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)
    balance = models.FloatField(default=00)
    refer_link = models.IntegerField()
    team = models.ManyToManyField(User, related_name='teams', null=True, blank=True)

    def __str__(self):
        return self.number