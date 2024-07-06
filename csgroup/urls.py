from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from base.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('register', handle_reg),
    path('signin', handle_login),
    path('logout', handle_logout),
    path('dashboard', dashboard),
    path('active', active),
    path('withdraw', withdrawl),
    path('fund-withdraw', fund_withdraw),
    path('leaderboard', leaderboard),
    path('support', support),
    path('success', success),
    path('package', pack),
    #path('transfer-fund', transfer_fund),
    #path('transfer-fund/<int:id>', transfer_fund_handle),
    path('createfund/<str:name>', create_fund),
    path('fundcheck', fundcheck),
    path('forget-password', reset_email),
    path('reset-code', reset_code),
    path('change-password', change_password),
    path('teams/<str:username>', get_teams),
    path('check-serial/<int:id>', check_serial)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "CS Group Admin"
admin.site.site_title = "CS Group Admin Portal"
admin.site.index_title = "Welcome to CS Group Head Quarter"
