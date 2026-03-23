from app import db
from app.models import *

def list_teachers(page=1, per_page=5, search=None):
    """Récupère les enseignants avec pagination et recherche"""
    # Jointure entre User et Teacher
    query = db.session.query(User, Teacher).join(Teacher, User.id == Teacher.id)
    
    # Recherche par nom ou par spécialité
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | 
            (Teacher.speciality.ilike(f'%{search}%'))
        )
    
    total = query.count()
    offset = (page - 1) * per_page
    
    teachers_data = query.offset(offset).limit(per_page).all()
    
    result = []
    for user, teacher in teachers_data:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "speciality": teacher.speciality
        })
    
    return {
        "teachers": result,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

def add_teacher(name, email, speciality, password="password123"):
    # Vérification email unique
    if User.query.filter_by(email=email).first():
        return None

    try:
        new_user = User(name=name, email=email, password=password, role='teacher')
        db.session.add(new_user)
        db.session.flush()

        new_teacher = Teacher(id=new_user.id, speciality=speciality)
        db.session.add(new_teacher)
        
        db.session.commit()
        return {"id": new_user.id, "name": name, "email": email}
    except Exception:
        db.session.rollback()
        return None

def delete_teacher(teacher_id):
    try:
        # 1. Récupérer tous les cours associés à ce professeur
        courses = Course.query.filter_by(teacher_id=teacher_id).all()
        
        for course in courses:
            # 2. Supprimer les inscriptions des étudiants pour CHAQUE cours
            CourseAssignment.query.filter_by(course_id=course.id).delete()
            # 3. Supprimer le cours lui-même
            db.session.delete(course)
        
        # 4. Supprimer l'entrée dans la table 'teachers'
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            db.session.delete(teacher)
            
        # 5. Supprimer l'entrée dans la table 'users'
        user = User.query.get(teacher_id)
        if user:
            db.session.delete(user)
            
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression du professeur : {e}")
        return False

def get_teacher_by_id(id):
    result = db.session.query(User, Teacher).join(Teacher, User.id == Teacher.id).filter(User.id == id).first()
    if result:
        user, teacher = result
        return {"id": user.id, "name": user.name, "email": user.email, "speciality": teacher.speciality}
    return None