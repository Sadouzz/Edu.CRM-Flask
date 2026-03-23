from app.models import User
from werkzeug.security import check_password_hash

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        return user

    return None