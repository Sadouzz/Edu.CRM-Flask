from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "supersecretkey"

    # IMPORTER LES BLUEPRINTS
    from app.auth.route import auth_bp
    from app.students.route import students_bp
    from app.teachers.route import teachers_bp
    from app.courses.route import courses_bp
    from app.dashboard.route import dashboard_bp

    # ENREGISTRER LES BLUEPRINTS
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(dashboard_bp)

    return app