from django.shortcuts import render, redirect
from base.models import *
from django.contrib.auth import authenticate, login, logout
import random

def home(request):
    return render(request, 'csgrp.html')

def dashboard(request):
    if request.user.is_authenticated:
        pr = Profile.objects.get(user=request.user)
        tm = pr.team.all()
        for t in tm:
            print(t.username)
        context = {'tm':tm, 'p':pr}
        return render(request, 'dashboard.html', context)
    return render(request, 'login.html')




def handle_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        ath = authenticate(username=username,password=password)
        if ath is not None:
            return redirect(dashboard)
        return redirect('/')





def handle_reg(request):
    if request.method == 'GET':
        r = None
        if request.GET.get('ref'):
            r = request.GET.get('ref')
        return render(request, 'register.html',context={'r':r})
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        number = data.get('number')
        refer = data.get('refer')
        pasword = data.get('pass1')

        c = User.objects.create(
            username=username,
            email=email,
            password=pasword
        )
        print("cccccccccccccccccccccc777777777", c)
        c.save()
        p = Profile.objects.create(user=c, number=number, refer_link=random.randint(100000, 999999))
 
        try:
            get_refer_user = Profile.objects.get(refer_link=refer)
            get_refer_user.team.add(c)

            get_refer_user.team.all()
        except:
            pass
        login(request, c)

        return redirect(dashboard)

def get_teams(request, username):
    p = Profile.objects.get(user__username=username)
    print(p)
    tms = p.team.all()
    context = {'p':p, 'tms':tms}
    return render(request, 'teams.html', context)


