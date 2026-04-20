from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            
            # Allow login, register, static, media, and admin
            allowed_paths = [
                settings.LOGIN_URL,
                '/accounts/register/',
            ]
            
            if any(path.startswith(p) for p in ['/static/', '/media/', '/admin/', '/accounts/login/', '/accounts/register/', '/login/', '/register/']):
                return self.get_response(request)
                
            if path not in allowed_paths:
                return redirect(f"{settings.LOGIN_URL}?next={path}")
                
        return self.get_response(request)
