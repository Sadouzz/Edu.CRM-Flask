from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.student_service import *
from app.auth.route import login_required

students_bp = Blueprint("students", __name__, url_prefix="/students")

@students_bp.route("/")
@login_required
def index():
    students = list_students()
    return render_template("students/list.html", students=students)

@students_bp.route("/create", methods=["POST"])
@login_required
def create():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        flash("Tous les champs sont obligatoires", "danger")
        return redirect(url_for("students.index"))

    add_student(name, email)
    flash("Étudiant ajouté avec succès", "success")

    return redirect(url_for("students.index"))

@students_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_student(id)
    flash("Étudiant supprimé", "info")
    return redirect(url_for("students.index"))