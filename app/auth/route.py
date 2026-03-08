from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            session["user"] = {"name": username, "id": 1}
            flash("Connexion réussie", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Identifiants incorrects", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Déconnexion réussie", "info")
    return redirect(url_for("auth.login"))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Veuillez vous connecter", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function