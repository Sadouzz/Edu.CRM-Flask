from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course_service import add_course, list_courses, delete_course
from app.auth.route import login_required
from app.services.teacher_service import list_teachers
from app.services.student_service import list_students
from app.services.course_service import *

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
@login_required
def courses_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    # On utilise la nouvelle version paginée
    data = list_courses(page=page, search=search)
    
    # On a toujours besoin des profs pour afficher les noms dans la liste
    teachers = list_teachers() 

    return render_template(
        "courses/list.html",
        courses=data['courses'], # On passe la liste réelle
        total_pages=data['total_pages'],
        page=data['page'],
        search=search,
        teachers=teachers
    )


@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_course():
    # Préparation des données pour le formulaire (GET)
    teachers_data = list_teachers()
    # Gestion du format (dict si paginé, list sinon)
    teachers = teachers_data['teachers'] if isinstance(teachers_data, dict) else teachers_data

    if request.method == "POST":
        # RÉCUPÉRATION DES DONNÉES DU FORMULAIRE
        title = request.form.get("title")
        teacher_id = int(request.form.get("teacher_id"))
        jour = request.form.get("jour")
        heure = request.form.get("heure")
        statut = request.form.get("statut", "Planifié")

        # VÉRIFICATION DES CONFLITS
        conflit = check_conflit(teacher_id, jour, heure)
        if conflit:
            flash(f"Conflit ! L'enseignant a déjà le cours '{conflit['title']}' ce jour à cette heure.", "danger")
            return render_template("courses/create.html", 
                                 teachers=teachers, jours=JOURS, statuts=STATUTS)

        # APPEL AU SERVICE POUR CRÉATION EN BD
        try:
            add_course(title, teacher_id, jour, heure, statut)
            flash(f"Le cours '{title}' a été créé avec succès.", "success")
            return redirect(url_for("courses.courses_list"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la création : {str(e)}", "danger")

    return render_template(
        "courses/create.html",
        teachers=teachers,
        jours=JOURS,
        statuts=STATUTS
    )

@courses_bp.route("/delete/<int:id>")
@login_required
def remove_course(id):
    delete_course(id)
    flash("Cours supprimé", "info")
    return redirect(url_for("courses.courses_list"))

@courses_bp.route("/assign/<int:course_id>", methods=["GET", "POST"])
@login_required
def assign_students(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash("Cours introuvable", "error")
        return redirect(url_for("courses.courses_list"))

    # Étudiants pas encore inscrits à ce cours
    data_students = list_students() 
    all_students = data_students['students'] # <--- C'est ici que se trouve la liste
    
    students_disponibles = [
        s for s in all_students if s["id"] not in course["student_ids"]
    ]
    students_disponibles = [
        s for s in all_students if s["id"] not in course["student_ids"]
    ]

    if request.method == "POST":
        # getlist récupère toutes les cases cochées
        student_ids = [int(sid) for sid in request.form.getlist("student_ids")]

        if not student_ids:
            flash("Veuillez cocher au moins un étudiant.", "warning")
            return render_template(
                "courses/assign.html",
                course=course,
                students=students_disponibles
            )

        assign_multiple_students(course_id, student_ids)
        flash(f"{len(student_ids)} étudiant(s) inscrit(s) avec succès !", "success")
        return redirect(url_for("courses.courses_list"))

    return render_template(
        "courses/assign.html",
        course=course,
        students=students_disponibles
    )


@courses_bp.route("/assign-multiple/<int:course_id>", methods=["GET", "POST"])
@login_required
def assign_multiple(course_id):
    course = get_course_by_id(course_id)
    if not course:
        flash("Cours introuvable", "error")
        return redirect(url_for("courses.courses_list"))

    # Étudiants pas encore inscrits à ce cours
    all_students = list_students()
    students_disponibles = [
        s for s in all_students if s["id"] not in course["student_ids"]
    ]

    if request.method == "POST":
        # getlist récupère toutes les cases cochées
        student_ids = [int(sid) for sid in request.form.getlist("student_ids")]

        if not student_ids:
            flash("Veuillez cocher au moins un étudiant.", "warning")
            return render_template(
                "courses/assign_multiple.html",
                course=course,
                students=students_disponibles
            )

        assign_multiple_students(course_id, student_ids)
        flash(f"{len(student_ids)} étudiant(s) inscrit(s) avec succès !", "success")
        return redirect(url_for("courses.courses_list"))

    return render_template(
        "courses/assign_multiple.html",
        course=course,
        students=students_disponibles
    )


@courses_bp.route("/statut/<int:course_id>", methods=["POST"])
@login_required
def changer_statut(course_id):
    nouveau_statut = request.form.get("statut")
    success = update_statut(course_id, nouveau_statut)

    if success:
        flash(f"Statut mis à jour : {nouveau_statut}", "success")
    else:
        flash("Statut invalide.", "danger")

    return redirect(url_for("courses.courses_list"))

@courses_bp.route("/details/<int:course_id>")
@login_required
def course_details(course_id):
    # 1. Get the course (from cache list or DB)
    course = get_course_by_id(course_id)
    if not course:
        flash("Cours introuvable", "error")
        return redirect(url_for("courses.courses_list"))

    # 2. FIX: Extract teachers list from the dictionary
    teachers_data = list_teachers()
    # Check if it's a dict (paginated) or a list
    all_teachers = teachers_data['teachers'] if isinstance(teachers_data, dict) else teachers_data
    
    # 3. Find the specific teacher
    teacher = next((t for t in all_teachers if t["id"] == course["teacher_id"]), None)
    
    # 4. Get student details
    all_students_data = list_students()
    all_students = all_students_data['students']
    
    # Filter students assigned to this course
    students_assigned = [s for s in all_students if s["id"] in course["student_ids"]]

    return render_template(
        "courses/details.html",
        course=course,
        teacher=teacher,
        students=students_assigned,
        statuts=STATUTS
    )
