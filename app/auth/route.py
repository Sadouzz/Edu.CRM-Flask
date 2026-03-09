from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

USERS_FILE = "app/Data/users.txt"


def check_user(username, password):

    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r") as f:

        for line in f:
            data = line.strip().split(",")

            file_username = data[0]
            file_password = data[1]

            if username == file_username and password == file_password:
                return True

    return False


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if check_user(username, password):

            session["user"] = username
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