from functools import wraps
from flask import abort
from flask_login import current_user

def permission_required(permission_code):
    """Decorator to require specific permission for a route"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401, "Authentication required")
            if not current_user.can_access(permission_code):
                abort(403, f"Permission denied: {permission_code}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(role_name):
    """Decorator to require specific role for a route"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401, "Authentication required")
            if not current_user.has_role(role_name):
                abort(403, f"Role required: {role_name}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401, "Authentication required")
        if not current_user.is_admin:
            abort(403, "Admin access required")
        return f(*args, **kwargs)
    return decorated_function