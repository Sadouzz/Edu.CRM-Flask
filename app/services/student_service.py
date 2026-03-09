students = [
    {"id": 1, "name": "Alice Dupont", "email": "alice@educrm.com"},
    {"id": 2, "name": "Jean Martin", "email": "jean@educrm.com"},
    {"id": 3, "name": "Fatou Ndiaye", "email": "fatou@educrm.com"}
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