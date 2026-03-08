students = [
    {"id": 1, "name": "Ousman", "email": "ousman@ism.edu.sn"},
    {"id": 2, "name": "Kazi OTP", "email": "kazi@ism.edu.sn"},
    {"id": 3, "name": "Fadil", "email": "fadil@ism.edu.sn"},
]

def add_student(name, email):
    new_id = len(students) + 1

    students.append({
        "id": new_id,
        "name": name,
        "email": email
    })

    return True


def list_students():
    return students


def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]


def get_student_by_id(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None