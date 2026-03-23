from flask import Blueprint, render_template, request, redirect, url_for
from app.services.student_service import *

students_bp = Blueprint("students", __name__)

@students_bp.route("/")
def students_list():

    students = list_students()

    return render_template("students/students.html", students=students)


@students_bp.route("/create", methods=["GET","POST"])
def create_student():

    if request.method == "POST":

        student = {
            "id": request.form["id"],
            "name": request.form["name"],
            "email": request.form["email"]
        }

        add_student(student)

        return redirect(url_for("students.students_list"))

    return render_template("students/create_student.html")


@students_bp.route("/delete/<id>")
def delete(id):

    delete_student(id)

    return redirect(url_for("students.students_list"))
