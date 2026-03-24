from app import db
from app.models import *

courses = []
STATUTS = ["Planifié", "En cours", "Terminé"]
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]

def sync_list_from_db():
    """Rafraîchit la liste mémoire à partir des données réelles de la BD."""
    global courses
    all_db_courses = Course.query.all()
    courses.clear()
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
    new_course = Course(
        title=title,
        teacher_id=teacher_id,
        jour=jour,
        heure=heure,
        statut=statut
    )
    db.session.add(new_course)
    db.session.commit()
    
    sync_list_from_db()
    return new_course

def assign_student_to_course(course_id, student_id):
    """Prépare l'inscription d'un étudiant dans la session (sans commit)."""
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
            if assign_student_to_course(course_id, sid):
                changes_made = True
        
        if changes_made:
            db.session.commit()
            sync_list_from_db() 
            
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erreur : {e}")
        return False

def delete_course(course_id):
    """Supprime un cours et ses assignations associées."""
    course_db = Course.query.get(course_id)
    if course_db:
        try:
            CourseAssignment.query.filter_by(course_id=course_id).delete()
            
            db.session.delete(course_db)
            db.session.commit()
            
            sync_list_from_db()
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la suppression : {e}")
            raise e

def list_courses(page=1, per_page=5, search=None):
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
            "teacher_name": teacher_name,
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
    for c in courses:
        if c["id"] == course_id:
            return c
            
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