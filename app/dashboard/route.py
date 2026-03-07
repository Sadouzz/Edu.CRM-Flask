from flask import Blueprint, render_template
from app.services.student_service import list_students
from app.services.teacher_service import list_teachers
from app.services.course_service import list_courses
from app.auth.route import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    total_students = len(list_students())
    total_teachers = len(list_teachers())
    total_courses = len(list_courses())

    return render_template(
        "dashboard/index.html",
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses
    )