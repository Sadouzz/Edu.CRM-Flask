from flask import Blueprint, render_template
from app.auth.route import login_required
from app.services.student_service import list_students
from app.services.teacher_service import list_teachers
from app.services.course_service import list_courses

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def dashboard():
    total_students = len(list_students())
    total_teachers = len(list_teachers())
    total_courses = len(list_courses())
    return render_template(
        "dashboard.html",
        students=total_students,
        teachers=total_teachers,
        courses=total_courses
    )