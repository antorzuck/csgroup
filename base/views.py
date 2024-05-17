from django.shortcuts import render
from base.models import *
from django.contrib.auth import authenticate, login, logout
import random

def home(request):
    return render(request, 'csgrp.html')


def handle_reg(request):
    if request.method == 'GET':
        return render(request, 'register.html')
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

        return render(request, 'dashboard.html', context={
            'user': c,
            'p' : p,
        })

