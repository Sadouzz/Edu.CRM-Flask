from app import db
from app.models import Course, Teacher, Student, CourseAssignment, User
import json

def list_courses(page=1, per_page=5, search=None):
    """Récupère les cours avec pagination et recherche"""
    query = Course.query
    
    # Ajouter la recherche si spécifiée
    if search:
        query = query.filter(Course.title.ilike(f'%{search}%'))
    
    # Pagination
    offset = (page - 1) * per_page
    total = query.count()
    
    courses = query.offset(offset).limit(per_page).all()
    
    result = []
    for course in courses:
        # Récupérer le nom de l'enseignant
        teacher = Teacher.query.get(course.teacher_id)
        teacher_name = None
        if teacher:
            user = User.query.get(teacher.id)
            teacher_name = user.name if user else f"Teacher {teacher.id}"
        
        # Compter le nombre d'étudiants inscrits
        student_count = CourseAssignment.query.filter_by(course_id=course.id).count()
        
        result.append({
            "id": course.id,
            "title": course.title,
            "teacher_id": course.teacher_id,
            "teacher_name": teacher_name,
            "student_count": student_count
        })
    
    return {
        "courses": result,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

def add_course(title, teacher_id):
    """Ajoute un nouveau cours"""
    try:
        # Vérifier que l'enseignant existe
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            raise ValueError(f"L'enseignant avec l'ID {teacher_id} n'existe pas")
        
        course = Course(
            title=title,
            teacher_id=teacher_id
        )
        
        db.session.add(course)
        db.session.commit()
        
        # Retourner les infos du cours créé
        user = User.query.get(teacher_id)
        teacher_name = user.name if user else f"Teacher {teacher_id}"
        
        return {
            "id": course.id,
            "title": course.title,
            "teacher_id": course.teacher_id,
            "teacher_name": teacher_name,
            "student_count": 0
        }
    except Exception as e:
        db.session.rollback()
        raise e

def get_course_by_id(course_id):
    """Récupère un cours par son ID avec tous les détails"""
    course = Course.query.get(course_id)
    if not course:
        return None
    
    # Récupérer l'enseignant
    teacher = Teacher.query.get(course.teacher_id)
    teacher_name = None
    if teacher:
        user = User.query.get(teacher.id)
        teacher_name = user.name if user else f"Teacher {teacher.id}"
    
    # Récupérer tous les étudiants assignés
    assignments = CourseAssignment.query.filter_by(course_id=course_id).all()
    students = []
    
    for assignment in assignments:
        student = Student.query.get(assignment.student_id)
        if student:
            user = User.query.get(student.id)
            if user:
                students.append({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                })
    
    return {
        "id": course.id,
        "title": course.title,
        "teacher_id": course.teacher_id,
        "teacher_name": teacher_name,
        "students": students,
        "student_count": len(students)
    }

def update_course(course_id, course_data):
    """Met à jour les informations d'un cours"""
    try:
        course = Course.query.get(course_id)
        if not course:
            return None
        
        # Mettre à jour le titre
        if 'title' in course_data:
            course.title = course_data['title']
        
        # Mettre à jour l'enseignant si spécifié
        if 'teacher_id' in course_data:
            teacher = Teacher.query.get(course_data['teacher_id'])
            if teacher:
                course.teacher_id = course_data['teacher_id']
        
        db.session.commit()
        
        # Récupérer les infos mises à jour
        teacher = Teacher.query.get(course.teacher_id)
        teacher_name = None
        if teacher:
            user = User.query.get(teacher.id)
            teacher_name = user.name if user else f"Teacher {teacher.id}"
        
        return {
            "id": course.id,
            "title": course.title,
            "teacher_id": course.teacher_id,
            "teacher_name": teacher_name,
            "student_count": CourseAssignment.query.filter_by(course_id=course_id).count()
        }
    except Exception as e:
        db.session.rollback()
        raise e

def assign_student_to_course(course_id, student_id):
    """Assigne un étudiant à un cours"""
    try:
        # Vérifier que le cours existe
        course = Course.query.get(course_id)
        if not course:
            raise ValueError(f"Le cours avec l'ID {course_id} n'existe pas")
        
        # Vérifier que l'étudiant existe
        student = Student.query.get(student_id)
        if not student:
            raise ValueError(f"L'étudiant avec l'ID {student_id} n'existe pas")
        
        # Vérifier si l'étudiant est déjà assigné
        existing_assignment = CourseAssignment.query.filter_by(
            course_id=course_id, 
            student_id=student_id
        ).first()
        
        if existing_assignment:
            return get_course_by_id(course_id)  # Déjà assigné
        
        # Créer l'assignation
        assignment = CourseAssignment(
            course_id=course_id,
            student_id=student_id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        return get_course_by_id(course_id)
        
    except Exception as e:
        db.session.rollback()
        raise e

def remove_student_from_course(course_id, student_id):
    """Retire un étudiant d'un cours"""
    try:
        assignment = CourseAssignment.query.filter_by(
            course_id=course_id,
            student_id=student_id
        ).first()
        
        if assignment:
            db.session.delete(assignment)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        raise e

def delete_course(course_id):
    """Supprime un cours et toutes ses assignations"""
    try:
        course = Course.query.get(course_id)
        if course:
            # Supprimer d'abord toutes les assignations liées
            CourseAssignment.query.filter_by(course_id=course_id).delete()
            
            # Puis supprimer le cours
            db.session.delete(course)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False

def get_available_teachers():
    """Récupère la liste des enseignants pour le formulaire"""
    teachers = db.session.query(User, Teacher).join(
        Teacher, User.id == Teacher.id
    ).all()
    
    return [{"id": user.id, "name": user.name} for user, teacher in teachers]

def get_available_students():
    """Récupère la liste des étudiants pour l'assignation"""
    students = db.session.query(User, Student).join(
        Student, User.id == Student.id
    ).all()
    
    return [{"id": user.id, "name": user.name, "email": user.email} 
            for user, student in students]

def get_courses_count():
    """Retourne le nombre total de cours"""
    from app.models import Course
    return Course.query.count()