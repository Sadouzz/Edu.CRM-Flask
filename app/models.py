from app import db

# =========================
# TABLE DE LIAISON (Many-to-Many)
# =========================
course_assignments = db.Table(
    'course_assignments',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True)
)

# =========================
# USERS (TABLE PRINCIPALE)
# =========================
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, student, teacher

    # relations
    student = db.relationship('Student', backref='user', uselist=False)
    teacher = db.relationship('Teacher', backref='user', uselist=False)


# =========================
# STUDENTS
# =========================
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # relation Many-to-Many
    courses = db.relationship(
        'Course',
        secondary=course_assignments,
        backref='students'
    )


# =========================
# TEACHERS
# =========================
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    speciality = db.Column(db.String(100))

    # relation One-to-Many
    courses = db.relationship('Course', backref='teacher', lazy=True)


# =========================
# COURSES
# =========================
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))