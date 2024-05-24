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
    refer_link = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    referred_by = models.ForeignKey(User, related_name='teams', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    def total_refer(self):
        return Referral.objects.filter(referrer=self, generation=1).count()

    def total_team(self):
        return Referral.objects.filter(referrer=self).count()

    def total_refer_income(self):
        tf = Referral.objects.filter(referrer=self, generation=1).count()
        return 50 * tf


class Referral(models.Model):
    referrer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referrals_made')
    referred_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referrals_received')
    generation = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.referrer} referred {self.referred_user} (Generation {self.generation})"



@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):
    print("i just fenned")
    # Ensure this code runs only when a Profile is newly verified
    if not created and instance.is_verified:
        referrer_user = instance.referred_by

        reward = {
            1: 60, 2: 5, 3: 4, 4: 3, 5: 2,
            6: 2, 7: 1, 8: 1, 9: 1, 10: 1
        }

        generation = 1  # Initialize generation counter

        while referrer_user and generation <= 10:
            try:
                referrer_profile = Profile.objects.get(user=referrer_user)
            except Profile.DoesNotExist:
                break  # No valid referrer profile, stop the loop

            # Create a referral record if not exists
            referral, created = Referral.objects.get_or_create(
                referrer=referrer_profile,
                referred_user=instance,
                generation=generation
            )

            if created:
                # Update the balance for the current generation
                referrer_profile.balance += reward[generation]
                referrer_profile.save()

            # Move up one generation
            referrer_user = referrer_profile.referred_by

            # Increment generation counter
            generation += 1
