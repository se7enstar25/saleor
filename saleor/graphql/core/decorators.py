from functools import wraps

from django.core.exceptions import PermissionDenied


def permission_required(permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = args[1]
            user = info.context.user
            if not user.has_perm(permissions):
                raise PermissionDenied(
                    'You have no permission to use %s' % info.field_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator
