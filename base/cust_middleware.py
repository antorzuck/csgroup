
from django.shortcuts import render
from django.conf import settings


def MaintenanceMiddleware(get_response):
    def middleware(request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            if request.user.is_authenticated and request.user.is_staff:
                return get_response(request)
            return render(request, 'busy.html')
        response = get_response(request)
        return response

    return middleware
