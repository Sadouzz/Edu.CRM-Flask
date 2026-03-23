from app import db
from app.models import User, Teacher

def list_teachers(page=1, per_page=5, search=None):
    """Récupère les enseignants avec pagination et recherche"""
    query = db.session.query(User, Teacher).join(
        Teacher, User.id == Teacher.id
    )
    
    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f'%{search}%'),
                Teacher.speciality.ilike(f'%{search}%')
            )
        )
    
    offset = (page - 1) * per_page
    total = query.count()
    
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

def add_teacher(name, email, speciality):
    """Ajoute un enseignant"""
    name_parts = name.strip().split()
    initials = ''.join([part[0].upper() for part in name_parts])
    
    user = User(
        name=name,
        email=email,
        password="temp",
        role="teacher"
    )
    db.session.add(user)
    db.session.flush()
    
    password = f"{initials}{user.id}"
    user.password = password
    
    teacher = Teacher(
        id=user.id,
        speciality=speciality
    )
    db.session.add(teacher)
    db.session.commit()
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "speciality": speciality,
        "password": password
    }

def get_teacher_by_id(teacher_id):
    """Récupère un enseignant par son ID"""
    teacher = Teacher.query.get(teacher_id)
    if teacher:
        user = User.query.get(teacher_id)
        if user:
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "speciality": teacher.speciality
            }
    return None

def update_teacher(teacher_id, teacher_data):
    """Met à jour les informations d'un enseignant et regénère le mot de passe si le nom change"""
    try:
        user = User.query.get(teacher_id)
        if not user:
            return None
        
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return None
        
        old_name = user.name
        new_name = teacher_data.get('name', old_name)
        
        # Mettre à jour les champs
        if 'name' in teacher_data:
            user.name = teacher_data['name']
        if 'email' in teacher_data:
            user.email = teacher_data['email']
        if 'speciality' in teacher_data:
            teacher.speciality = teacher_data['speciality']
        
        # Si le nom a changé, regénérer le mot de passe
        password_changed = False
        if old_name != new_name:
            name_parts = new_name.strip().split()
            initials = ''.join([part[0].upper() for part in name_parts])
            user.password = f"{initials}{teacher_id}"
            password_changed = True
        
        db.session.commit()
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "speciality": teacher.speciality,
            "password": user.password if password_changed else None
        }
    except Exception as e:
        db.session.rollback()
        raise e

def delete_teacher(teacher_id):
    """Supprime un enseignant"""
    try:
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            db.session.delete(teacher)
            
            user = User.query.get(teacher_id)
            if user:
                db.session.delete(user)
            
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        raise e
    
def get_teachers_count():
    """Retourne le nombre total d'enseignants"""
    from app.models import Teacher
    return Teacher.query.count()