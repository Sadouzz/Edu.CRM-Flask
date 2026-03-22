from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course_service import add_course, list_courses, delete_course
from app.auth.route import login_required
from app.services.teacher_service import list_teachers
from app.services.student_service import list_students
from app.services.course_service import *

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
@login_required
def courses_list():

    courses = list_courses()
    teachers = list_teachers()
    students = list_students()

    return render_template(
        "courses/list.html",
        courses=courses,
        teachers=teachers,
        students=students
    )


@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_course():

    teachers = list_teachers()

    if request.method == "POST":

        title = request.form.get("title")
        teacher_id = int(request.form.get("teacher_id"))

        add_course(title, teacher_id)

        flash("Cours ajouté avec succès", "success")

        return redirect(url_for("courses.courses_list"))

    return render_template("courses/create.html", teachers=teachers)


@courses_bp.route("/delete/<int:id>")
@login_required
def remove_course(id):

    delete_course(id)

    flash("Cours supprimé", "info")

    return redirect(url_for("courses.courses_list"))

@courses_bp.route("/assign/<int:course_id>", methods=["GET", "POST"])
@login_required
def assign_student(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash("Cours introuvable", "error")
        return redirect(url_for("courses.courses_list"))

    students = list_students()

    if request.method == "POST":
        student_id = int(request.form.get("student_id"))
        assign_student_to_course(course_id, student_id)
        flash("Étudiant assigné au cours", "success")
        return redirect(url_for("courses.courses_list"))

    return render_template("courses/assign.html", course=course, students=students)

@courses_bp.route("/details/<int:course_id>")
@login_required
def course_details(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash("Cours introuvable", "error")
        return redirect(url_for("courses.courses_list"))

    teacher = next((t for t in list_teachers() if t["id"] == course['teacher_id']), None)

    students = [s for s in list_students() if s["id"] in course['student_ids']]

    return render_template(
        "courses/details.html",
        course=course,
        teacher=teacher,
        students=students
    )