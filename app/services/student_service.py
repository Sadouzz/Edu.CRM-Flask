students = []

def add_student(student):
    student["id"] = len(students) + 1
    students.append(student)

def list_students():
    return students

def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]

def get_student_by_id(id):
    for s in students:
        if s["id"] == id:
            return s
