from functools import wraps

from flask import current_app, request
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS


def role_required(*roles):
    """
    A decorator to enforce role-based access control.
    :param roles: Tuple of allowed roles for the route.
    """

    def decorator(func):
        @wraps(func)
        def wrapped_view(*args, **kwargs):
            if request.method in EXEMPT_METHODS or current_app.config.get(
                "LOGIN_DISABLED"
            ):
                pass
            elif (
                current_user.get_role() not in roles
                or not current_user.is_authenticated
            ):
                return current_app.login_manager.unauthorized()

            # flask 1.x compatibility
            # current_app.ensure_sync is only available in Flask >= 2.0
            if callable(getattr(current_app, "ensure_sync", None)):
                return current_app.ensure_sync(func)(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapped_view

    return decorator
