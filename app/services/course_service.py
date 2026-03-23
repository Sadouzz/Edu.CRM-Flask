from app import db
from app.models import *

# Ta liste globale (utilisée pour la lecture)
courses = []
STATUTS = ["Planifié", "En cours", "Terminé"]
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]

def sync_list_from_db():
    """Rafraîchit la liste mémoire à partir des données réelles de la BD."""
    global courses
    all_db_courses = Course.query.all()
    courses.clear() # On vide sans perdre la référence globale
    for c in all_db_courses:
        courses.append({
            "id": c.id,
            "title": c.title,
            "teacher_id": c.teacher_id,
            "student_ids": [a.student_id for a in c.assignments],
            "jour": c.jour,
            "heure": c.heure,
            "statut": c.statut
        })

def add_course(title, teacher_id, jour=None, heure=None, statut="Planifié"):
    # 1. Action directe en BD
    new_course = Course(
        title=title,
        teacher_id=teacher_id,
        jour=jour,
        heure=heure,
        statut=statut
    )
    db.session.add(new_course)
    db.session.commit()
    
    # 2. On synchronise la liste pour que l'affichage soit à jour
    sync_list_from_db()
    return new_course

def assign_student_to_course(course_id, student_id):
    """Prépare l'inscription d'un étudiant dans la session (sans commit)."""
    # Vérification en BD
    existing = CourseAssignment.query.filter_by(
        course_id=course_id, 
        student_id=student_id
    ).first()
    
    if not existing:
        new_assign = CourseAssignment(course_id=course_id, student_id=student_id)
        db.session.add(new_assign)
        return True
    return False

def assign_multiple_students(course_id, student_ids):
    """Inscrit plusieurs étudiants en appelant la logique unitaire."""
    try:
        changes_made = False
        for sid in student_ids:
            # On appelle la fonction unitaire pour chaque ID
            if assign_student_to_course(course_id, sid):
                changes_made = True
        
        # On valide tout le bloc d'un coup
        if changes_made:
            db.session.commit()
            sync_list_from_db() # Sync la liste mémoire une seule fois
            
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erreur : {e}")
        return False

def update_statut(course_id, nouveau_statut):
    """Modifie le statut directement en BD."""
    course_db = Course.query.get(course_id)
    if course_db and nouveau_statut in STATUTS:
        course_db.statut = nouveau_statut
        db.session.commit()
        
        # Sync la liste
        sync_list_from_db()
        return True
    return False

def delete_course(course_id):
    """Supprime un cours et ses assignations associées."""
    course_db = Course.query.get(course_id)
    if course_db:
        try:
            # 1. Supprimer manuellement les assignations liées
            CourseAssignment.query.filter_by(course_id=course_id).delete()
            
            # 2. Supprimer le cours
            db.session.delete(course_db)
            db.session.commit()
            
            # Sync la liste mémoire
            sync_list_from_db()
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la suppression : {e}")
            raise e

# --- Fonctions utilitaires (Lecture seule sur la liste) ---
def list_courses(page=1, per_page=5, search=None):
    # On joint Course -> Teacher -> User pour avoir le nom
    query = db.session.query(Course, User.name).join(
        Teacher, Course.teacher_id == Teacher.id
    ).join(
        User, Teacher.id == User.id
    )
    
    if search:
        query = query.filter(Course.title.ilike(f'%{search}%'))
    
    total = query.count()
    db_results = query.offset((page - 1) * per_page).limit(per_page).all()
    
    result_list = []
    for c, teacher_name in db_results:
        result_list.append({
            "id": c.id,
            "title": c.title,
            "teacher_name": teacher_name, # On ajoute le nom ici !
            "student_ids": [a.student_id for a in c.assignments],
            "jour": c.jour,
            "heure": c.heure,
            "statut": c.statut
        })
    
    return {
        "courses": result_list,
        "total": total,
        "page": page,
        "total_pages": (total + per_page - 1) // per_page
    }
def get_course_by_id(course_id):
    # 1. Check in memory list first
    for c in courses:
        if c["id"] == course_id:
            return c
            
    # 2. Backup: Check Database if not in list
    c = Course.query.get(course_id)
    if c:
        return {
            "id": c.id,
            "title": c.title,
            "teacher_id": c.teacher_id,
            "student_ids": [a.student_id for a in c.assignments],
            "jour": c.jour,
            "heure": c.heure,
            "statut": c.statut
        }
    return None

def check_conflit(teacher_id, jour, heure, exclude_id=None):
    # On vérifie sur la liste synchronisée
    if not courses: sync_list_from_db()
    for course in courses:
        if exclude_id and course["id"] == exclude_id:
            continue
        if (course["teacher_id"] == teacher_id and 
            course["jour"] == jour and 
            course["heure"] == heure):
            return course
    return None