from functools import wraps
from django.http import HttpResponseForbidden

def group_required(group_name):
    """
    Custom decorator to check if the user belongs to a specific group.
    Usage: @group_required('group_name')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                # User belongs to the specified group, grant access to the view
                return view_func(request, *args, **kwargs)
            else:
                # User does not belong to the group, deny access
                return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator