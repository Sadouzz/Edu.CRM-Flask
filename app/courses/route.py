from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course_service import * 
from app.services.teacher_service import list_teachers
from app.services.student_service import list_students
from app.auth.route import login_required

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

@courses_bp.route("/")
@login_required
def index():
    courses = list_courses()
    teachers = list_teachers()
    return render_template("courses/list.html", courses=courses, teachers=teachers)


@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        teacher_id = int(request.form.get("teacher_id"))

        success = add_course(title, teacher_id)

        if success:
            flash("Cours ajouté avec succès", "success")
        else:
            flash("Enseignant introuvable", "danger") 

        return redirect(url_for("courses.index"))
    
    teachers = list_teachers() 
    return render_template("courses/create.html", teachers=teachers)


@courses_bp.route("/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign_student(id):
    course = get_course_by_id(id)  
    students = list_students()      
    
    if request.method == "POST":
        student_id = int(request.form.get("student_id"))
        success = assign_student_to_course(id, student_id) 
        
        if success:
            flash("Étudiant assigné avec succès", "success")
        else:
            flash("Erreur lors de l'assignation", "danger")
        
        return redirect(url_for("courses.index"))
    
    return render_template("courses/assign.html", course=course, students=students)


@courses_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_course(id)
    flash("Cours supprimé", "info")
    return redirect(url_for("courses.index"))