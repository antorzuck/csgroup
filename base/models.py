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
    title = models.CharField(max_length=200, null=True, blank=True)
    number = models.CharField(max_length=50)
    balance = models.FloatField(default=00)
    shopping_balance = models.IntegerField(default=0)
    refer_link = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    reset_code = models.CharField(max_length=100, null=True, blank=True)
    referred_by = models.ForeignKey(User, related_name='teams', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)

    def total_refer(self):
        return Referral.objects.filter(referrer=self, generation=1).count()

    def total_team(self):
        return Referral.objects.filter(referrer=self).count()
        
    def totalwithdraw(self):
        w = Withdraw.objects.filter(profile=self)
        money = sum([i.amount for i in w])
        
        print(money)
        return money
        
        
    
    def total_refer_income(self):
        tf = Referral.objects.filter(referrer=self, generation=1).count()
        return 40 * tf


    def total_gen_income(self):
      
        referrals = Referral.objects.filter(referrer=self, generation__lte=10)
        generation_counts = {i: 0 for i in range(1, 11)}
        
        for referral in referrals:
            generation_counts[referral.generation] += 1
        
        multipliers = {
            1: 10,
            2: 5,
            3: 4,
            4: 3,
            5: 2,
            6: 2,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
                }
        sums = sum(generation_counts[g] * multipliers[g] for g in generation_counts)

        return sums
        
    def lti(self):
        if self.balance == 0:
            return 00
        referrals = Referral.objects.filter(referrer=self, generation__lte=10)
        generation_counts = {i: 0 for i in range(1, 11)}
        
        for referral in referrals:
            generation_counts[referral.generation] += 1
        
        multipliers = {
            1: 50,
            2: 5,
            3: 4,
            4: 3,
            5: 2,
            6: 2,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
                }
        sums = sum(generation_counts[g] * multipliers[g] for g in generation_counts)
        return sums

class Withdraw(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} withdraw of {str(self.profile.user.username)}"





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
            1: 50, 2: 5, 3: 4, 4: 3, 5: 2,
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
            
            
            
            

         

class FundPackage(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name
        

class Counter(models.Model):
    num = models.IntegerField(default=1)
    package = models.ForeignKey(FundPackage, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return str(self.num)
   

class Funded(models.Model):
    profle = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='funding')
    package = models.ForeignKey(FundPackage, on_delete=models.CASCADE, related_name='pack')
    balance = models.IntegerField(default=00)
    is_rewarded = models.BooleanField(default=False)

    def total_bal(self):
        fnf = Funded.objects.filter(profle=self.profle)
        money = sum([i.balance for i in fnf])
        return money
        
    def __str__(self):
        return f'funding by {str(self.profle.name)} on {str(self.package.name)}'



class Profit(models.Model):
    alltime = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    profits = models.IntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Profit of {str(self.profile.name)}"


class FundWithdraw(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    method = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} withdraw of {str(self.profile.user.username)}"



def transfer_fund_auto(pid, user):
    print("i run bro after reward complete")
    pack = FundPackage.objects.filter(id__gt=pid)[0]
    print("heeeeeee", pack)
    print(FundPackage.objects.filter(id__gt=pid))
    try:
        fund = Funded.objects.filter(profle=user, is_rewarded=True).order_by('-id')[0]
        print("after checking balance")

        if fund.balance >= pack.price:
            print("yes, greater")
            Funded.objects.create(package=pack,  profle=user, balance=pack.price)
            print("yes created")
            fund.balance = fund.balance - pack.price
            fund.save()
            pro = Profit.objects.get(profile=user)
            pro.balance = pro.balance - pack.price
            pro.alltime = pro.alltime + pack.price
            pro.save()
        else:
            pass
    except Exception as e:
        print("arey buij", e)


@receiver(post_save, sender=Funded)
def reward(sender, instance, created, **kwargs):
    print("reward")
    if not Profit.objects.filter(profile=instance.profle).exists():
        Profit.objects.create(profile=instance.profle, alltime=instance.package.price)
    if created:
        ff = Funded.objects.filter(package=instance.package, is_rewarded=False).exclude(id=instance.id).order_by('-id')
        try:
            xxx = Counter.objects.get(package=instance.package)
            get_rwrd_id = ff[xxx.num]
            fx = Funded.objects.get(id=get_rwrd_id.id)
            fx.balance = fx.balance + instance.package.price
            fx.is_rewarded = True
            fx.save()
            xxx.num = xxx.num + 1
            xxx.save()
            
            pro = Profit.objects.get(profile=get_rwrd_id.profle)
            pro.balance = pro.balance + instance.package.price * 2
            pro.profits = pro.profits + instance.package.price * 2
            pro.save()
            id = instance.package.id
            print("the id is", id)
            transfer_fund_auto(pid=id, user=get_rwrd_id.profle)
            print("fun called")
            
          
            
                


        except Exception as e:
            print(e)
            if not Counter.objects.filter(package=instance.package).exists():
                Counter.objects.create(package=instance.package)
                


