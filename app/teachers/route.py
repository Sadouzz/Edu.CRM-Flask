from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.teacher_service import *
from app.auth.route import login_required

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

@teachers_bp.route("/")
@login_required
def index():
    teachers = list_teachers()
    return render_template("teachers/list.html", teachers=teachers)


@teachers_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        speciality = request.form.get("speciality")

        if not name or not email or not speciality:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("teachers.create")) 

        add_teacher(name, email, speciality)
        flash("Enseignant ajouté avec succès", "success")
        return redirect(url_for("teachers.index"))
    
    
    return render_template("teachers/create.html")

@teachers_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_teacher(id)
    flash("Enseignant supprimé", "info")
    return redirect(url_for("teachers.index"))