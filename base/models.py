from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




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
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=50)
    balance = models.FloatField(default=00)
    refer_link = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    referred_by = models.ForeignKey(User, related_name='teams', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.number


class Referral(models.Model):
    referrer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referrals_made')
    referred_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referrals_received')
    generation = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.referrer} referred {self.referred_user} (Generation {self.generation})"

"""
@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):
    if created and instance.referred_by:
        referrer = instance.referred_by

        for generation in range(1, 11):
            if not referrer:
                break
            
            Referral.objects.create(referrer=referrer, referred_user=instance, generation=generation)
            referrer = referrer.referred_by  # Move up one generation
            print(referrer)
            print("just runned *********&$$$%^$%^$%^$%^")

"""


@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):
    if created and instance.referred_by:
        referrer_user = instance.referred_by

        # Get the Profile instance for the referrer_user
        try:
            referrer_profile = Profile.objects.get(user=referrer_user)
        except Profile.DoesNotExist:
            referrer_profile = None

        for generation in range(1, 11):
            if not referrer_profile:
                break

            Referral.objects.create(referrer=referrer_profile, referred_user=instance, generation=generation)
            referrer_user = referrer_profile.referred_by  # Move up one generation

            if referrer_user:
                try:
                    referrer_profile = Profile.objects.get(user=referrer_user)
                except Profile.DoesNotExist:
                    referrer_profile = None
            else:
                referrer_profile = None

            print(referrer_profile)
            print("just runned *********&$$$%^$%^$%^$%^")



