from django.shortcuts import render, redirect
from base.models import *
from django.contrib.auth import authenticate, login, logout
import random


def home(request):
    products = Product.objects.all()
    cats = Cat.objects.all()
    context = {
        'pro' : products,
        'cats' : cats
    }
    return render(request, 'home.html', context=context)


def dashboard(request):
    if request.user.is_authenticated:
        pr = Profile.objects.get(user=request.user)

        context = {'tm':"hi", 'p':pr}
        return render(request, 'dashboard.html', context)
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

def get_teams(request, username):
    p = Profile.objects.get(user__username=username)
    print(p)
    tms = 'hi'
    context = {'p':p, 'tms':tms}
    return render(request, 'teams.html', context)


