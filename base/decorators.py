from django.shortcuts import redirect, render
from functools import wraps
import datetime
from django.utils import timezone
from django.http import JsonResponse
from base.models import *
def onlyuser(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/signin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def restrict_withdraw_time(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        current_time = timezone.localtime().time()
        start_time = datetime.time(10, 0)
        end_time = datetime.time(22, 0)

        if not (start_time <= current_time <= end_time):
            return render(request, 'withdrawoff.html')

        return func(request, *args, **kwargs)

    return wrapper




def check_withdrawal_limit(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            today = timezone.now().date()
            if Withdraw.objects.filter(profile=Profile.objects.get(user=request.user), created_at__date=today).exists():
                return render(request, 'withdrawlimit.html')
            if FundWithdraw.objects.filter(profile=Profile.objects.get(user=request.user), created_at__date=today).exists():
                return render(request, 'withdrawlimit.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
