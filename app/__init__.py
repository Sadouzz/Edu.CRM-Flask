from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Importer les blueprints
  
    # from app.auth.route import auth_bp
    from app.students.route import students_bp
    # from app.teachers.route import teachers_bp
    # from app.courses.route import courses_bp
    # from app.dashboard.route import dashboard_bp

    # Enregistrer les blueprints
  
    # app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp, url_prefix="/students")
    # app.register_blueprint(teachers_bp, url_prefix="/teachers")
    # app.register_blueprint(courses_bp, url_prefix="/courses")
    # app.register_blueprint(dashboard_bp)

    return app
