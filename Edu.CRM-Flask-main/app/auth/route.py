from flask import Blueprint, render_template, request, redirect, session, flash
from .service import authenticate
from .decorators import login_required
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = authenticate(email, password)

        if user:
            session['user_id'] = user.id
            session['role'] = user.role

            flash("Connexion réussie")
            return redirect('/')
        else:
            flash("Identifiants incorrects")

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté")
    return redirect('/auth/login')

@auth_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('auth/profile.html', user=user)