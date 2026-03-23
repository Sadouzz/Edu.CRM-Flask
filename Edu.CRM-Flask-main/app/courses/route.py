from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.services.course_service import *
from app.auth.decorators import login_required, roles_required

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/")
@login_required
@roles_required('admin', 'teacher', 'student')  # Tous les rôles peuvent voir les cours
def courses_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    result = list_courses(page=page, search=search)
    
    return render_template("courses/list.html", 
                         courses=result['courses'],
                         total=result['total'],
                         page=result['page'],
                         total_pages=result['total_pages'],
                         search=search)

@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
@roles_required('admin')  # Seul admin peut créer
def create_course():
    if request.method == "POST":
        title = request.form["title"]
        teacher_id = request.form["teacher_id"]
        
        try:
            new_course = add_course(title, teacher_id)
            flash(f"Cours '{new_course['title']}' créé avec succès!", "success")
            return redirect(url_for("courses.courses_list"))
        except Exception as e:
            flash(f"Erreur lors de la création: {str(e)}", "error")
    
    teachers = get_available_teachers()
    return render_template("courses/create.html", teachers=teachers)

@courses_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@roles_required('admin')  # Seul admin peut modifier
def edit_course(id):
    course = get_course_by_id(id)
    if not course:
        flash("Cours non trouvé!", "error")
        return redirect(url_for("courses.courses_list"))
    
    if request.method == "POST":
        course_data = {
            "title": request.form["title"],
            "teacher_id": request.form["teacher_id"]
        }
        
        updated_course = update_course(id, course_data)
        if updated_course:
            flash(f"Cours '{updated_course['title']}' modifié avec succès!", "success")
        else:
            flash("Erreur lors de la modification!", "error")
        
        return redirect(url_for("courses.courses_list"))
    
    teachers = get_available_teachers()
    return render_template("courses/edit.html", course=course, teachers=teachers)

@courses_bp.route("/delete/<int:id>")
@login_required
@roles_required('admin')  # Seul admin peut supprimer
def delete_course_route(id):
    course = get_course_by_id(id)
    if course:
        delete_course(id)
        flash(f"Cours '{course['title']}' supprimé avec succès!", "success")
    else:
        flash("Cours non trouvé!", "error")
    
    return redirect(url_for("courses.courses_list"))

@courses_bp.route("/details/<int:course_id>")
@login_required
@roles_required('admin', 'teacher', 'student')  # Tous peuvent voir les détails
def course_details(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash("Cours non trouvé!", "error")
        return redirect(url_for("courses.courses_list"))
    
    return render_template("courses/details.html", course=course)

@courses_bp.route("/assign/<int:course_id>", methods=["GET", "POST"])
@login_required
@roles_required('admin', 'teacher')  # Admin et prof peuvent assigner
def assign_student(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash("Cours non trouvé!", "error")
        return redirect(url_for("courses.courses_list"))
    
    if request.method == "POST":
        student_id = request.form.get("student_id")
        if student_id:
            try:
                assign_student_to_course(course_id, student_id)
                flash("Étudiant assigné avec succès!", "success")
            except Exception as e:
                flash(f"Erreur: {str(e)}", "error")
        return redirect(url_for("courses.course_details", course_id=course_id))
    
    students = get_available_students()
    return render_template("courses/assign.html", course=course, students=students)

@courses_bp.route("/remove/<int:course_id>/<int:student_id>")
@login_required
@roles_required('admin', 'teacher')  # Admin et prof peuvent retirer
def remove_student(course_id, student_id):
    try:
        remove_student_from_course(course_id, student_id)
        flash("Étudiant retiré du cours avec succès!", "success")
    except Exception as e:
        flash(f"Erreur: {str(e)}", "error")
    
    return redirect(url_for("courses.course_details", course_id=course_id))