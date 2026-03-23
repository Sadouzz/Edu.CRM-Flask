from flask import Blueprint, render_template
from app.auth.route import login_required
from app.services.student_service import list_students
from app.services.teacher_service import list_teachers
from app.services.course_service import list_courses

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def dashboard():
    # On récupère les dictionnaires de données
    # On peut mettre per_page=1 car on ne veut que le chiffre 'total'
    students_data = list_students(page=1, per_page=1)
    teachers_data = list_teachers(page=1, per_page=1)
    courses_data = list_courses(page=1, per_page=1)
    
    return render_template(
        "dashboard.html",
        students=students_data['total'], # On utilise la clé 'total'
        teachers=teachers_data['total'],
        courses=courses_data['total']
    )