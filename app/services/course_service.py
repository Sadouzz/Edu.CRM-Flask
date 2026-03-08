courses = []

from app.services.teacher_service import list_teachers
from app.services.student_service import get_student_by_id
from app.services.teacher_service import get_teacher_by_id


def add_course(title, teacher_id):
    teacher_exists = any(t["id"] == teacher_id for t in list_teachers())

    if not teacher_exists:
        return False

    new_id = len(courses) + 1
    courses.append({
        "id": new_id,
        "title": title,
        "teacher_id": teacher_id,
        "student_ids": []
    })

    return True


def list_courses():
    return courses


def delete_course(course_id):
    global courses
    courses = [c for c in courses if c["id"] != course_id]


def assign_student_to_course(course_id, student_id):
    student = get_student_by_id(student_id)
    if not student:
        return False

    for course in courses:
        if course["id"] == course_id:
            course["student_ids"].append(student_id)
            return True

    return False