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





"""

@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):
    # Ensure this code runs only when a Profile is newly verified
    if not created and instance.is_verified:
        referrer_user = instance.referred_by

        reward = {
            1: 60, 2: 5, 3: 4, 4: 3, 5: 2,
            6: 2, 7: 1, 8: 1, 9: 1, 10: 1
        }

        # Track processed referrer profiles
        processed_referrers = set()

        for generation in range(1, 11):
            if not referrer_user:
                break

            try:
                referrer_profile = Profile.objects.get(user=referrer_user)
            except Profile.DoesNotExist:
                referrer_profile = None

            if referrer_profile:
                generation, username = generation, referrer_profile.user.username
                print(generation, username)

                # Update total referral balance for this generation
                referrer_profile.balance += reward[generation]
                referrer_profile.save()

                # Skip processing if already earned for this referral chain
                if referrer_profile.balance >= reward[1]:  # Assuming reward[1] is 60
                    referrer_user = None  # Skip processing further

                # Create a referral record if not exists
                Referral.objects.get_or_create(
                    referrer=referrer_profile,
                    referred_user=instance,
                    generation=generation
                )

                # Mark this referrer as processed
                processed_referrers.add(referrer_user.id)

                # Move up one generation (only if not skipped)
                if referrer_user:
                    referrer_user = referrer_profile.referred_by



"""






# signals.py
"""
@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):
    # Ensure this code runs only when a Profile is newly verified
    if not created and instance.is_verified:
        referrer_user = instance.referred_by

        reward = {
            1: 60, 2: 5, 3: 4, 4: 3, 5: 2,
            6: 2, 7: 1, 8: 1, 9: 1, 10: 1
        }

        # Track processed referrer profiles
        processed_referrers = set()

        for generation in range(1, 11):
            if not referrer_user:
                break

            if referrer_user.id in processed_referrers:
                break

            try:
                referrer_profile = Profile.objects.get(user=referrer_user)
            except Profile.DoesNotExist:
                referrer_profile = None

            if referrer_profile:
                print(generation, referrer_profile.user.username)  # Print for debugging

                # Add the reward for the specific generation
                referrer_profile.balance += reward[generation]
                referrer_profile.save()

                # Create a referral record if not exists
                Referral.objects.get_or_create(
                    referrer=referrer_profile,
                    referred_user=instance,
                    generation=generation
                )

                # Mark this referrer as processed
                processed_referrers.add(referrer_user.id)

                # Move up one generation
                referrer_user = referrer_profile.referred_by



"""










"""
@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):
    # Ensure this code runs only when a Profile is newly created and verified
    if not created and instance.is_verified:
        referrer_user = instance.referred_by

        reward = {
            1: 60, 2: 5, 3: 4, 4: 3, 5: 2, 
            6: 2, 7: 1, 8: 1, 9: 1, 10: 1
        }

        for generation in range(1, 11):
            if not referrer_user:
                break

            try:
                referrer_profile = Profile.objects.get(user=referrer_user)
            except Profile.DoesNotExist:
                referrer_profile = None

            if referrer_profile:
                print(generation, referrer_profile)
                # Add the reward for the specific generation
                referrer_profile.balance += reward[generation]
                referrer_profile.save()

                # Create a referral record if not exists
                Referral.objects.get_or_create(
                    referrer=referrer_profile,
                    referred_user=instance,
                    generation=generation
                )

                # Move up one generation
                referrer_user = referrer_profile.referred_by




"""


"""

@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):

    if not created and instance.is_verified:
        referrer_user = instance.referred_by

        reward = {
            1 : '60', 2:'5', 3:'4', 4:'3',5:'2', 6:'2', 7:'1', 8:'1', 9:'1', 10:'1'
        }
        if referrer_user:
            try:
                referrer_profile = Profile.objects.get(user=referrer_user)
            except Profile.DoesNotExist:
                referrer_profile = None

            for generation in range(1, 11):
                if not referrer_profile:
                    break

                referrer_profile.balance += int(reward[generation])
                referrer_profile.save()

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

"""

"""
@receiver(post_save, sender=Profile)
def create_referral(sender, instance, created, **kwargs):
    if not created and instance.is_verified:
        referrer_user = instance.referred_by

        reward = {
            1: 60, 2: 5, 3: 4, 4: 3, 5: 2, 
            6: 2, 7: 1, 8: 1, 9: 1, 10: 1
        }
        if referrer_user:
            try:
                referrer_profile = Profile.objects.get(user=referrer_user)
            except Profile.DoesNotExist:
                referrer_profile = None

            for generation in range(1, 11):
                if not referrer_profile:
                    break

                # Add the reward to the current referrer's balance
                referrer_profile.balance += reward[generation]
                referrer_profile.save()

                # Create a referral record
                Referral.objects.create(referrer=referrer_profile, referred_user=instance, generation=generation)

                # Move up one generation
                referrer_user = referrer_profile.referred_by
                print("i just renned&&&&*********")
                if referrer_user:
                    try:
                        referrer_profile = Profile.objects.get(user=referrer_user)
                    except Profile.DoesNotExist:
                        referrer_profile = None
                else:
                    referrer_profile = None

"""
