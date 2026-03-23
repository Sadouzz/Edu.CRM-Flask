from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.services.teacher_service import *
from app.auth.decorators import login_required, roles_required

teachers_bp = Blueprint("teachers", __name__)

@teachers_bp.route("/")
@login_required
@roles_required('admin', 'teacher')  # Admin et prof peuvent voir la liste
def teachers_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    result = list_teachers(page=page, search=search)
    
    return render_template("teachers/list.html", 
                         teachers=result['teachers'],
                         total=result['total'],
                         page=result['page'],
                         total_pages=result['total_pages'],
                         search=search)

@teachers_bp.route("/create", methods=["GET","POST"])
@login_required
@roles_required('admin')  # Seul admin peut créer
def create_teacher():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        speciality = request.form["speciality"]
        
        new_teacher = add_teacher(name, email, speciality)
        flash(f"Enseignant {new_teacher['name']} créé avec succès! Mot de passe: {new_teacher['password']}", "success")
        
        return redirect(url_for("teachers.teachers_list"))
    
    return render_template("teachers/create.html")

@teachers_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@roles_required('admin')  # Seul admin peut modifier
def edit_teacher(id):
    teacher = get_teacher_by_id(id)
    if not teacher:
        flash("Enseignant non trouvé!", "error")
        return redirect(url_for("teachers.teachers_list"))
    
    if request.method == "POST":
        teacher_data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "speciality": request.form["speciality"]
        }
        
        updated_teacher = update_teacher(id, teacher_data)
        if updated_teacher:
            message = f"Enseignant {updated_teacher['name']} modifié avec succès!"
            if updated_teacher.get('password'):
                message += f" Nouveau mot de passe: {updated_teacher['password']}"
            flash(message, "success")
        else:
            flash("Erreur lors de la modification!", "error")
        
        return redirect(url_for("teachers.teachers_list"))
    
    return render_template("teachers/edit.html", teacher=teacher)

@teachers_bp.route("/delete/<id>")
@login_required
@roles_required('admin')  # Seul admin peut supprimer
def delete(id):
    teacher = get_teacher_by_id(id)
    if teacher:
        delete_teacher(id)
        flash(f"Enseignant {teacher['name']} supprimé avec succès!", "success")
    
    return redirect(url_for("teachers.teachers_list"))