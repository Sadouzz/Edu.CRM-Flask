from functools import wraps
from flask import session, redirect, flash

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter")
            return redirect('/auth/login')
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') != role:
                return "Accès refusé", 403
            return f(*args, **kwargs)
        return decorated
    return wrapper