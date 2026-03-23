from functools import wraps
from flask import session, redirect, flash, abort

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter", "warning")
            return redirect('/auth/login')
        return f(*args, **kwargs)
    return decorated

def role_required(role):
    """Vérifie que l'utilisateur a un rôle spécifique"""
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') != role:
                flash("Accès non autorisé", "danger")
                return abort(403)
            return f(*args, **kwargs)
        return decorated
    return wrapper

def roles_required(*roles):
    """Vérifie que l'utilisateur a l'un des rôles spécifiés"""
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') not in roles:
                flash("Accès non autorisé", "danger")
                return abort(403)
            return f(*args, **kwargs)
        return decorated
    return wrapper