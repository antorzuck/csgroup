from django.shortcuts import render
from django.conf import settings

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)
            return render(request, 'busy.html')
        return self.get_response(request)
        