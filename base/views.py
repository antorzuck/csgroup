from django.shortcuts import render, redirect
from base.models import *
from django.contrib.auth import authenticate, login, logout
import random
from django.http import JsonResponse
import requests
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from base.decorators import onlyuser


def home(request):
    products = Product.objects.all()
    cats = Cat.objects.all()
    context = {
        'pro' : products,
        'cats' : cats
    }
    return render(request, 'home.html', context=context)


def active(request):
    url = "https://pay.csgroup.my.id/api/checkout-v2"
    payload = {
    "full_name": request.user.username,
    "email": request.user.email,
    "amount": "1",
    "metadata": {
        "order_id": "16",
        "product_id": "5"
    },
    "redirect_url": "https://csgroup.my.id",
    "return_type": "GET",
    "cancel_url": "https://csgroup.my.id"
    }
    headers = {
    "accept": "application/json",
    "RT-UDDOKTAPAY-API-KEY": "f1d5bd54b659a131aad3020f1bbcd15e5bd275d9",
    "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    xx = json.loads(response.text)
    return redirect(xx['payment_url'])

"""

def active(request):
    p = Profile.objects.get(user=request.user)
    p.is_verified = True
    p.save()
    return redirect(dashboard)
"""

@onlyuser
def withdrawl(request):
    p = Profile.objects.get(user=request.user)
    ww = Withdraw.objects.filter(profile=p).order_by('-id')
    if request.method == "POST":
        amount = request.POST.get('amount')
        method = request.POST.get('method')

        if int(amount) > int(p.balance):
            return JsonResponse({'message' : 'Withdraw amount should be less then balance'})
        w = Withdraw.objects.create(profile=p, amount=amount,method=method, status='pending')
        return redirect('/withdraw')
    return render(request, 'withdraw.html', context={'p':p, 'ww':ww})


@onlyuser
def leaderboard(request):
    return render(request, 'lead.html')


def dashboard(request):
    if request.user.is_authenticated:
        pr = Profile.objects.get(user=request.user)
        r = pr.total_refer()
        rf = Referral.objects.filter(referrer=pr, generation=1).order_by('-id')[0:5]

        context = {'rf':rf, 'r':r, 'p':pr}
        return render(request, 'dashhome.html', context)
    return render(request, 'login.html')


def handle_login(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        ath = authenticate(username=username,password=password)
        print(ath)
        if ath is not None:
            login(request, ath)
            return redirect(dashboard)
        return redirect('/')



@onlyuser
def handle_logout(request):
    logout(request)
    return redirect(handle_login)


def handle_reg(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    if request.method == 'GET':
        r = None
        if request.GET.get('ref'):
            r = request.GET.get('ref')
        return render(request, 'register.html',context={'r':r})

    if request.method == 'POST':
        data = request.POST
        name = data.get('fname')
        username = data.get('uname')
        email = data.get('email')
        number = data.get('number')
        refer = data.get('refer')
        print(refer)
        pasword = data.get('password')

        c = User.objects.create_user(
            username=username,
            email=email,
            password=pasword
        )
        print("cccccccccccccccccccccc777777777", c)
        c.save()
 
        try:
            print("ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            refer_user = Profile.objects.get(refer_link=refer)

            print(refer_user)
            print("xxxxxxxxxxxxxxx")
            if refer_user:
                print("yes")

                p = Profile.objects.create(user=c, referred_by=refer_user.user, name=name, number=number, refer_link=number)
        except Exception as e:
            p = Profile.objects.create(user=c, name=name, number=number, refer_link=number)
            print("opps", e)
            pass
        login(request, c)

        return redirect(dashboard)

@onlyuser
@csrf_exempt
def get_teams(request, username):
    if request.method == 'GET':
        gen = request.GET.get('gen')
        genon = 1
        if gen:
            genon = gen
        p = Profile.objects.get(user__username=username)
        ref = Referral.objects.filter(referrer=p, generation=genon).order_by('-id')
        paginator = Paginator(ref, 10)
        page_number = request.GET.get('page')
        ref = paginator.get_page(page_number)
        context = {'ref':ref, 'gen':genon, 'username':username}
        return render(request, 'team.html', context)


