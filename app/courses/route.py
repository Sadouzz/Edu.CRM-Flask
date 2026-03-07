from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course_service import *
from app.services.teacher_service import list_teachers
from app.auth.route import login_required

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

@courses_bp.route("/")
@login_required
def index():
    courses = list_courses()
    teachers = list_teachers()
    return render_template("courses/list.html", courses=courses, teachers=teachers)

@courses_bp.route("/create", methods=["POST"])
@login_required
def create():
    title = request.form.get("title")
    teacher_id = int(request.form.get("teacher_id"))

    success = add_course(title, teacher_id)

    if success:
        flash("Cours ajouté avec succès", "success")
    else:
        flash("Teacher introuvable", "danger")

    return redirect(url_for("courses.index"))

@courses_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_course(id)
    flash("Cours supprimé", "info")
    return redirect(url_for("courses.index"))