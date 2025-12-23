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


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only apply to pages with Looker Studio iframes
        if 'nmiframe' in request.path or 'edutech' in request.path:
            response['Content-Security-Policy'] = (
                "frame-src 'self' https://lookerstudio.google.com https://*.google.com; "
                "script-src 'self' 'unsafe-inline' https://lookerstudio.google.com https://*.google.com; "
                "frame-ancestors 'self';"
            )
            response['Referrer-Policy'] = 'no-referrer-when-downgrade'
            
            # Remove X-Frame-Options
            if 'X-Frame-Options' in response:
                del response['X-Frame-Options']
        
        return response