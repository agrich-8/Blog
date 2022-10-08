from functools import wraps
from ﬂask import abort
from ﬂask_login import current_user

from .models import Permission
def permission_required(permission):
    def decorator(f): 
        @wraps(f) # вызывает код ошибки 403(сделать страницу обработки)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission): 
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)