from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.services.student_service import *
from app.auth.decorators import login_required, roles_required

students_bp = Blueprint("students", __name__)

@students_bp.route("/")
@login_required
@roles_required('admin', 'teacher')  # Admin et prof peuvent voir la liste
def students_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    result = list_students(page=page, search=search)
    
    return render_template("students/students.html", 
                         students=result['students'],
                         total=result['total'],
                         page=result['page'],
                         total_pages=result['total_pages'],
                         search=search)

@students_bp.route("/create", methods=["GET","POST"])
@login_required
@roles_required('admin')  # Seul admin peut créer
def create_student():
    if request.method == "POST":
        student = {
            "name": request.form["name"],
            "email": request.form["email"]
        }
        
        new_student = add_student(student)
        flash(f"Étudiant {new_student['name']} créé avec succès! Mot de passe: {new_student['password']}", "success")
        
        return redirect(url_for("students.students_list"))
    
    return render_template("students/create_student.html")

@students_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@roles_required('admin')  # Seul admin peut modifier
def edit_student(id):
    student = get_student_by_id(id)
    if not student:
        flash("Étudiant non trouvé!", "error")
        return redirect(url_for("students.students_list"))
    
    if request.method == "POST":
        student_data = {
            "name": request.form["name"],
            "email": request.form["email"]
        }
        
        updated_student = update_student(id, student_data)
        if updated_student:
            message = f"Étudiant {updated_student['name']} modifié avec succès!"
            if updated_student.get('password'):
                message += f" Nouveau mot de passe: {updated_student['password']}"
            flash(message, "success")
        else:
            flash("Erreur lors de la modification!", "error")
        
        return redirect(url_for("students.students_list"))
    
    return render_template("students/edit.html", student=student)

@students_bp.route("/delete/<id>")
@login_required
@roles_required('admin')  # Seul admin peut supprimer
def delete(id):
    student = get_student_by_id(id)
    if student:
        delete_student(id)
        flash(f"Étudiant {student['name']} supprimé avec succès!", "success")
    
    return redirect(url_for("students.students_list"))