from app import db

# Table de liaison pour la relation Many-to-Many
assignments = db.Table('course_assignments',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True)
)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    speciality = db.Column(db.String(100))
    # Relation : Un enseignant peut avoir plusieurs cours
    courses = db.relationship('Course', backref='instructor', lazy=True)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    # Relation Many-to-Many avec Students
    students = db.relationship('Student', secondary=assignments, backref='enrolled_courses')