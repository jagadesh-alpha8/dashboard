# lookerapp/middleware.py

from django.contrib.auth import logout

class LogoutOnCloseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Check if a flag to logout is set in the session
        if request.session.pop('_logout_on_close', False):
            logout(request)
        return response
