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
    path('leaderboard', leaderboard),
    path('support', support),
    path('success', success),
    path('forget-password', reset_email),
    path('reset-code', reset_code),
    path('change-password', change_password),
    path('teams/<str:username>', get_teams)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "CS Group Admin"
admin.site.site_title = "CS Group Admin Portal"
admin.site.index_title = "Welcome to CS Group Head Quarter"
