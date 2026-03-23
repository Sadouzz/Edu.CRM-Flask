from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import *

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")


@teachers_bp.route("/")
def teachers_list():
    query = request.args.get("q")
    page = int(request.args.get("page", 1))
    per_page = 5

    if query:
        all_teachers = search_teachers(query)
    else:
        all_teachers = list_teachers()

    start = (page - 1) * per_page
    end = start + per_page

    teachers = all_teachers[start:end]

    has_next = len(all_teachers) > end
    has_prev = start > 0

    return render_template(
        "teachers/list.html",
        teachers=teachers,
        page=page,
        has_next=has_next,
        has_prev=has_prev
    )


@teachers_bp.route("/create", methods=["GET", "POST"])
def create_teacher():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        speciality = request.form.get("speciality")

        if not name or not email or not password or not speciality:
            flash("All fields required", "error")
            return redirect(url_for("teachers.create_teacher"))

        add_teacher(name, email, password, speciality)
        flash("Teacher added", "success")

        return redirect(url_for("teachers.teachers_list"))

    return render_template("teachers/create.html")


@teachers_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_teacher(id):
    teacher = get_teacher_by_id(id)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        speciality = request.form.get("speciality")

        update_teacher(id, name, email, speciality)
        flash("Updated", "success")

        return redirect(url_for("teachers.teachers_list"))

    return render_template("teachers/edit.html", teacher=teacher)


@teachers_bp.route("/delete/<int:id>")
def delete_teacher_route(id):
    delete_teacher(id)
    flash("Deleted", "success")

    return redirect(url_for("teachers.teachers_list"))