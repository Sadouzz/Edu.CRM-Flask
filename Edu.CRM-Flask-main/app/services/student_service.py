from app import db
from app.models import User, Student

def list_students(page=1, per_page=5, search=None):
    """Récupère les étudiants avec pagination et recherche"""
    # Base query
    query = db.session.query(User, Student).join(
        Student, User.id == Student.id
    )
    
    # Ajouter la recherche si spécifiée
    if search:
        query = query.filter(User.name.ilike(f'%{search}%'))
    
    # Pagination
    offset = (page - 1) * per_page
    total = query.count()
    
    students_data = query.offset(offset).limit(per_page).all()
    
    result = []
    for user, student in students_data:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    
    return {
        "students": result,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

def add_student(student_data):
    """Ajoute un étudiant dans la base de données"""
    from app.models import User
    
    # Générer les initiales
    name_parts = student_data["name"].strip().split()
    initials = ''.join([part[0].upper() for part in name_parts])
    
    # Créer l'utilisateur
    user = User(
        name=student_data["name"],
        email=student_data["email"],
        password="temp",
        role="student"
    )
    db.session.add(user)
    db.session.flush()
    
    # Générer le mot de passe
    password = f"{initials}{user.id}"
    user.password = password
    
    # Créer l'étudiant
    student = Student(id=user.id)
    db.session.add(student)
    db.session.commit()
    
    return {"id": user.id, "name": user.name, "email": user.email, "password": password}

def get_student_by_id(student_id):
    """Récupère un étudiant par son ID"""
    student = Student.query.get(student_id)
    if student:
        user = User.query.get(student_id)
        if user:
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
    return None

def update_student(student_id, student_data):
    """Met à jour les informations d'un étudiant et regénère le mot de passe si le nom change"""
    try:
        user = User.query.get(student_id)
        if not user:
            return None
        
        old_name = user.name
        new_name = student_data.get('name', old_name)
        
        # Mettre à jour les champs
        if 'name' in student_data:
            user.name = student_data['name']
        if 'email' in student_data:
            user.email = student_data['email']
        
        # Si le nom a changé, regénérer le mot de passe
        if old_name != new_name:
            name_parts = new_name.strip().split()
            initials = ''.join([part[0].upper() for part in name_parts])
            user.password = f"{initials}{student_id}"
        
        db.session.commit()
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password if old_name != new_name else None  # Retourner le nouveau mot de passe si changé
        }
    except Exception as e:
        db.session.rollback()
        raise e

def delete_student(id):
    """Supprime un étudiant"""
    from app.models import CourseAssignment
    
    try:
        student = Student.query.get(id)
        if student:
            # Supprimer les assignations
            CourseAssignment.query.filter_by(student_id=id).delete()
            db.session.delete(student)
            
            user = User.query.get(id)
            if user:
                db.session.delete(user)
            
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        raise e
    
def get_students_count():
    """Retourne le nombre total d'étudiants"""
    from app.models import Student
    return Student.query.count()