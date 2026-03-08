from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import (
    list_teachers,
    add_teacher,
    delete_teacher
)

teachers_bp = Blueprint(
    "teachers",
    __name__,
    url_prefix="/teachers"
)


@teachers_bp.route("/")
def teachers_list():
    teachers = list_teachers()

    return render_template("teachers/list.html", teachers=teachers)


@teachers_bp.route("/create", methods=["GET", "POST"])
def create_teacher():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        speciality = request.form.get("speciality")

        if not name or not email or not speciality:
            flash("All fields are required", "error")
            return redirect(url_for("teachers.create_teacher"))

        add_teacher(name, email, speciality)

        flash("Teacher added successfully", "success")

        return redirect(url_for("teachers.teachers_list"))

    return render_template("teachers/create.html")


@teachers_bp.route("/delete/<int:id>")
def delete_teacher_route(id):

    delete_teacher(id)

    flash("Teacher deleted successfully", "success")

    return redirect(url_for("teachers.teachers_list"))