from flask import Blueprint, render_template, request, redirect, url_for
from app.services.student_service import *
from app.auth.route import login_required

students_bp = Blueprint("students", __name__)

@students_bp.route("/")
@login_required
def students_list():

    students = list_students()

    return render_template("students/students.html", students=students)


@students_bp.route("/create", methods=["GET","POST"])
@login_required
def create_student():

    if request.method == "POST":

        student = {
            "name": request.form["name"],
            "email": request.form["email"]
        }

        add_student(student)

        return redirect(url_for("students.students_list"))

    return render_template("students/create_student.html")


@students_bp.route("/delete/<id>")
@login_required
def delete(id):

    delete_student(id)

    return redirect(url_for("students.students_list"))
