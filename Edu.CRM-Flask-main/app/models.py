from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'student', 'teacher'

class Teacher(db.Model):
    __tablename__ = 'teachers'
    # Héritage : l'ID est lié à User.id
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    speciality = db.Column(db.String(100))
    
    # Un enseignant a plusieurs cours
    courses = db.relationship('Course', backref='teacher', lazy=True)

class Student(db.Model):
    __tablename__ = 'students'
    # Héritage : l'ID est lié à User.id
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    # Relation vers les assignations (via la classe d'association)
    assignments = db.relationship('CourseAssignment', back_populates='student')

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    
    # Relation vers les assignations
    assignments = db.relationship('CourseAssignment', back_populates='course')

class CourseAssignment(db.Model):
    __tablename__ = 'course_assignments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow) # Optionnel : date d'inscription

    # Liens bidirectionnels
    student = db.relationship('Student', back_populates='assignments')
    course = db.relationship('Course', back_populates='assignments')