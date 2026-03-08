from flask import Flask, redirect, url_for
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    from app.auth.route import auth_bp
    from app.students.route import students_bp
    from app.teachers.route import teachers_bp
    from app.courses.route import courses_bp
    from app.dashboard.route import dashboard_bp

    
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(teachers_bp, url_prefix="/teachers")
    app.register_blueprint(courses_bp, url_prefix="/courses")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    
    @app.route('/')
    def index():
        from flask import session
        if 'user' in session:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    return app