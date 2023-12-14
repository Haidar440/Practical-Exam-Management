from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:  
            return redirect(reverse('home'))
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None;
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("U not Authorize")
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='examiners':
            return redirect('user')
        if group == 'admin':
            return view_func(request,*args,**kwargs)
    return wrapper_func

from functools import wraps
from django.shortcuts import redirect

def locked_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        is_locked = request.session.get('is_locked', False)  # Check if 'is_locked' is set in session

        if is_locked:
            # If user is locked, redirect to a locked access page or a different view
            return redirect('locked_access_page')  # Replace 'locked_access_page' with the actual URL name or path

        # If user is not locked, proceed to the view
        return view_func(request, *args, **kwargs)

    return _wrapped_view
