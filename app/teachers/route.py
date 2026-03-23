from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import (
    list_teachers,
    add_teacher,
    delete_teacher
)
from app.auth.route import login_required

teachers_bp = Blueprint(
    "teachers",
    __name__,
    url_prefix="/teachers"
)


@teachers_bp.route("/")
@login_required
def teachers_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    result = list_teachers(page=page, search=search)

    return render_template(
        "teachers/list.html", 
        teachers=result['teachers'],
        total=result['total'],
        page=result['page'],
        total_pages=result['total_pages'],
        search=search
    )


@teachers_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_teacher():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        speciality = request.form.get("speciality")

        if not name or not email or not speciality:
            flash("All fields are required", "danger")
            return render_template("teachers/create.html")

        # Le service s'occupe de la double insertion User/Teacher
        add_teacher(name, email, speciality)

        flash("Teacher added successfully", "success")
        return redirect(url_for("teachers.teachers_list"))

    return render_template("teachers/create.html")

@teachers_bp.route("/delete/<int:id>")
@login_required
def delete_teacher_route(id):
    delete_teacher(id)
    flash("Teacher deleted successfully", "success")
    return redirect(url_for("teachers.teachers_list"))