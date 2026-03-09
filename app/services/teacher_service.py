teachers = [
    {"id": 1, "name": "Mme. Dupont", "email": "mme.dupont@educrm.com", "speciality": "Mathématiques"},
    {"id": 2, "name": "M. Martin", "email": "m.martin@educrm.com", "speciality": "Physique"},
    {"id": 3, "name": "Mme. Ndiaye", "email": "mme.ndiaye@educrm.com", "speciality": "Informatique"}
]


def add_teacher(name, email, speciality):
    new_id = len(teachers) + 1

    teachers.append({
        "id": new_id,
        "name": name,
        "email": email,
        "speciality": speciality
    })

    return True


def list_teachers():
    return teachers


def delete_teacher(teacher_id):
    global teachers
    teachers = [t for t in teachers if t["id"] != teacher_id]


def get_teacher_by_id(teacher_id):
    for teacher in teachers:
        if teacher["id"] == teacher_id:
            return teacher
    return None