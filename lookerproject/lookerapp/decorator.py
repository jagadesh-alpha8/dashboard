from functools import wraps
from django.http import HttpResponseForbidden

def group_required(groups=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and any(request.user.groups.filter(name=group).exists() for group in groups):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper
    return decorator
