from app import db
from app.models import User, Teacher

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
    user = User.query.get(teacher_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def get_teacher_by_id(id):
    result = db.session.query(User, Teacher).join(Teacher, User.id == Teacher.id).filter(User.id == id).first()
    if result:
        user, teacher = result
        return {"id": user.id, "name": user.name, "email": user.email, "speciality": teacher.speciality}
    return None