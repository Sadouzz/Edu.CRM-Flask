teachers = []

def list_teachers():
    return teachers

def add_teacher(name, email, speciality):
    new_teacher = {
        "id": len(teachers) + 1,
        "name": name,
        "email": email,
        "speciality": speciality
    }

    teachers.append(new_teacher)

    return new_teacher

def delete_teacher(teacher_id):
    global teachers
    teachers = [t for t in teachers if t["id"] != teacher_id]