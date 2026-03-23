from flask import Blueprint, render_template, session
from app.auth.decorators import login_required
from app.services.student_service import get_students_count
from app.services.teacher_service import get_teachers_count
from app.services.course_service import get_courses_count
from app.models import User, CourseAssignment

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def dashboard():
    role = session.get('role')
    user_id = session.get('user_id')
    
    # Statistiques générales (pour admin)
    total_students = 0
    total_teachers = 0
    total_courses = 0
    
    # Données spécifiques selon le rôle
    if role == 'admin':
        total_students = get_students_count()
        total_teachers = get_teachers_count()
        total_courses = get_courses_count()
        
    elif role == 'teacher':
        total_courses = get_courses_count()
        # Récupérer les cours de l'enseignant connecté
        from app.models import Teacher, Course
        teacher = Teacher.query.get(user_id)
        if teacher:
            my_courses = Course.query.filter_by(teacher_id=user_id).count()
        else:
            my_courses = 0
            
    elif role == 'student':
        # Récupérer les cours de l'étudiant connecté
        from app.models import CourseAssignment
        my_courses = CourseAssignment.query.filter_by(student_id=user_id).count()
    
    return render_template(
        "dashboard.html",
        role=role,
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses,
        user_id=user_id
    )