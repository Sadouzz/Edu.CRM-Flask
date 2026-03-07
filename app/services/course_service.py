courses = []

def add_course(title, teacher_id):
    course = {
        "id": len(courses) + 1,
        "title": title,
        "teacher_id": teacher_id,
        "student_ids": []
    }
    courses.append(course)


def assign_student_to_course(course_id, student_id):
    for course in courses:
        if course["id"] == course_id:
            course["student_ids"].append(student_id)


def list_courses():
    return courses

def delete_course(course_id):
    global courses
    courses = [c for c in courses if c["id"] != course_id]