from django.shortcuts import render, redirect
from base.models import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import random
from django.http import JsonResponse
import requests
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from base.decorators import onlyuser, restrict_withdraw_time, check_withdrawal_limit
from django.core.mail import send_mail
from django.conf import settings


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
    "amount": "100",
    "metadata": {
        "order_id": "16",
        "product_id": "5"
    },
    "redirect_url": "https://csgroup.my.id/success",
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


def success(request):
    print("success is runned")
    request.GET.get('invoice_id')
    if request.GET.get('invoice_id'):
        request.GET.get('invoice_id')
        url = "https://pay.csgroup.my.id/api/verify-payment"
        payload = { "invoice_id": request.GET.get('invoice_id') }
        headers = {
        "accept": "application/json",
        "RT-UDDOKTAPAY-API-KEY": "f1d5bd54b659a131aad3020f1bbcd15e5bd275d9",
        "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        xx = json.loads(response.text)

        stats = xx['status']

        if stats == 'COMPLETED':
            p = Profile.objects.get(user__username=xx['full_name'])
            p.is_verified = True
            p.shopping_balance = 100
            p.save()
            return redirect('/dashboard')
        return redirect('/dashboard')


@onlyuser
@restrict_withdraw_time
@check_withdrawal_limit
def withdrawl(request):
    p = Profile.objects.get(user=request.user)
    ww = Withdraw.objects.filter(profile=p).order_by('-id')
    if request.method == "POST":
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        number = request.POST.get('number')

        if int(amount) > int(p.balance):
            return JsonResponse({'message' : 'Withdraw amount should be less then balance'})
        w = Withdraw.objects.create(profile=p, amount=amount, number=number, method=method, status='pending')
        p.balance = p.balance - float(amount)
        p.save()
        return redirect('/withdraw')
    return render(request, 'withdraw.html', context={'p':p, 'ww':ww})


@onlyuser
def leaderboard(request):
    p = Profile.objects.all().order_by('-balance')[0:10]
    return render(request, 'lead.html', context={'p':p})

"""
def dashboard(request):
    if request.user.is_authenticated:
        pr = Profile.objects.get(user=request.user)
        r = pr.total_refer()
        rf = Referral.objects.filter(referrer=pr, generation=1).order_by('-id')[0:5]

        context = {'rf':rf, 'r':r, 'p':pr}
        return render(request, 'dashhome.html', context)
    return render(request, 'login.html')
"""


def dashboard(request):
    if request.user.is_authenticated:
        
        con = False
        if request.GET.get('confetti'):
            con = True
        pr = Profile.objects.get(user=request.user)
        r = pr.total_refer()
        rf = Referral.objects.filter(referrer=pr, generation=1).order_by('-id')[0:5]
        fund = 0
        profit = 0
        try:
            fn = Funded.objects.filter(profle=pr)[0]
            fund = fn.total_bal()
            profit = Profit.objects.get(profile=pr)
        except:
            pass

        context = {'profit':profit, 'rf':rf, 'r':r, 'p':pr, 'fund':fund, 'con':con}
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

        ath = authenticate(username=username.strip(), password=password.strip())
        if ath is not None:
            login(request, ath)
            return redirect(dashboard)
        return render(request, 'login.html', context={'error': 'No user found!'})



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
        cpasword = data.get('confirm-password')
        
        if " " in username:
            username = username.replace(" ", "")
        
        if pasword != cpasword:
            return render(request, 'register.html', context={"error" : "Both password are not matched"})
            
        if Profile.objects.filter(refer_link=number).exists():
            return render(request, 'register.html', context={"error" : "Try with different number"})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', context={"error" : "Username already exist."})

        c = User.objects.create_user(
            username=username.strip(),
            email=email,
            password=pasword.strip()
        )
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


def support(request):
    return render(request, 'support.html')
    

def reset_email(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            pr = Profile.objects.get(user__email=email)
            print("here we go prof", pr)
            six = random.randint(100000,999999)
            pr.reset_code = six
            pr.save()
            subject = 'CS Group reset password'
            message = f'Here is your 6 digit code for reset password: {six}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('/reset-code')
        except Exception as e:
            print("mailing error bro", e)
            print(e)
            return render(request, 'forgot.html', context={'error' : 'No user found with this mail bro.'})
            
    return render(request, 'forgot.html')
    
def reset_code(request):
    if request.method == 'POST':
        thefuckingcode = request.POST.get('reset-code')
        try:
            pr = Profile.objects.get(reset_code=thefuckingcode)
            pr.reset_code = ''
            pr.save()
            login(request, pr.user)
            return redirect('/change-password')
        except:
            return render(request, 'subcode.html', context={'error': 'sorry wrong code. check you email again.'})
    return render(request, 'subcode.html')

@onlyuser
def change_password(request):
    if request.method == 'POST':
        new = request.POST.get('new-password')
        confirm = request.POST.get('confirm-password')
        
        if new != confirm:
            return render(request, 'changepass.html', context={'error': 'Both password are not matched. try again'})
        u = User.objects.get(username=request.user.username)
        u.set_password(new)
        u.save()
        update_session_auth_hash(request, u)
        return render(request, 'changepass.html', context={'suc': 'Password changed sucessfully.'})
    return render(request, 'changepass.html')
    
    
    



@onlyuser
def pack(request):
    if request.method == 'GET':
        return render(request, 'pack.html', context={'pg': FundPackage.objects.all()})


@onlyuser
def create_fund(request, name):
    gf = FundPackage.objects.get(name=name)
    if Funded.objects.filter(profle= Profile.objects.get(user=request.user), package=gf).exists():
        return render(request, 'pack.html', context={'pg': FundPackage.objects.all(), 'msg': 'You already donated on this package'})
    
    if request.GET.get('active') == 'balance':
        pr = Profile.objects.get(user=request.user)
        if not pr.balance >= gf.price:
            return render(request, 'pack.html', context={'pg': FundPackage.objects.all(), 'msg': 'You do not have balance for buy this package'})
        else:
            Funded.objects.create(profle=pr, package=gf, balance=gf.price)
            pr.balance = pr.balance - gf.price
            pr.save()
            """
            try:
                pro = Profit.objects.get(profile=pr)
                pro.alltime = pro.alltime + gf.price
                pro.save()
            except Exception as e:
                print(e)
                Profit.objects.create(profile=pr, alltime=gf.price)"""
            return redirect('/dashboard?confetti=true')
    
    url = "https://pay.csgroup.my.id/api/checkout-v2"
    payload = {
    "full_name": request.user.username,
    "email": request.user.email,
    "amount": gf.price,
    "metadata": {
        "pak_name": name
    },
    "redirect_url": "https://csgroup.my.id/fundcheck",
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


@onlyuser
def fundcheck(request):
    print("checking fund...")
    request.GET.get('invoice_id')
    if request.GET.get('invoice_id'):
        request.GET.get('invoice_id')
        url = "https://pay.csgroup.my.id/api/verify-payment"
        payload = { "invoice_id": request.GET.get('invoice_id') }
        headers = {
        "accept": "application/json",
        "RT-UDDOKTAPAY-API-KEY": "f1d5bd54b659a131aad3020f1bbcd15e5bd275d9",
        "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        xx = json.loads(response.text)

        stats = xx['status']

        if stats == 'COMPLETED':
            fp = FundPackage.objects.get(name=xx['metadata']['pak_name'])
            p = Profile.objects.get(user__username=xx['full_name'])
            
            f = Funded.objects.create(
                    package= fp ,
                    profle=p,
                    balance= fp.price)

            return redirect('/dashboard?confetti=true')
        return redirect('/dashboard')

@onlyuser
def transfer_fund(request):
    p= Profile.objects.get(user=request.user)
    ff = Funded.objects.filter(profle=p).order_by('-id')
    if ff.exists():
        fff = ff[0]
        price = fff.package.price
        
       
        for_transfer = FundPackage.objects.filter(price__gt=price)[0]
       
        print("for transfer", for_transfer)
        return render(request, 'transfer.html', context={'fortrans': for_transfer})
    else:
        return render(request, 'transfer.html', context={'msg': 'You have not active any fund yet. please go to the saving fund and buy one.'})
        

@onlyuser
def transfer_fund_handle(request, id):
    pack = FundPackage.objects.get(id=id)
    try:
        fund = Funded.objects.filter(profle=Profile.objects.get(user=request.user), is_rewarded=True).order_by('-id')[0] 
        
        if fund.balance >= pack.price:
            Funded.objects.create(package=pack,  profle=Profile.objects.get(user=request.user), balance=pack.price)
            fund.balance = fund.balance - pack.price
            fund.save()
            pro = Profit.objects.get(profile=Profile.objects.get(user=request.user))
            pro.balance = pro.balance - pack.price
            pro.alltime = pro.alltime + pack.price
            pro.save()
            return redirect('/dashboard?confetti=true')
        else:
            return render(request, 'transfer.html', context={'msg':'You are not finished the current fund game. once you got your reward then you can transfer your fund.'})
    except Exception as e:
        print("arey buij", e)
        return render(request, 'transfer.html', context={'msg': 'You have to finish one fund reward. then you can transfet to another.'})
            
            
        
        
    
@onlyuser
@restrict_withdraw_time
@check_withdrawal_limit
def fund_withdraw(request):
    
    p = Profile.objects.get(user=request.user)
    ww = FundWithdraw.objects.filter(profile=p).order_by('-id')
    try:
        pr = Profit.objects.get(profile=p)
    except Exception as e:
        print("hi im from fund withraw", e)
        return redirect('/package')
    
    if request.method == "POST":
        print("ahhha uhhu fuckin gshit im just runned man")
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        number = request.POST.get('number')
        
        
        print(amount, method, number, p)

        if int(amount) > int(pr.balance):
            return JsonResponse({'message' : 'Withdraw amount should be less then balance'})
        w = FundWithdraw.objects.create(profile=p, amount=amount, number=number, method=method, status=False)
        pr.balance = pr.balance - float(amount)
        pr.save()
        return redirect('/fund-withdraw')
    return render(request, 'fundwithdraw.html', context={'pr':pr, 'ww':ww})
    
def check_serial(request, id):
    pack =FundPackage.objects.get(id=id)
    fund_users =Funded.objects.filter(
        is_rewarded=False,
        package = pack)
    print("funded users data here we go", fund_users)
    context = {'fund_users' : fund_users}
    return render(request, 'serial.html', context)
    
    

            

    