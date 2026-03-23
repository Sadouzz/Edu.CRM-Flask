from app.db import get_connection

def list_teachers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.id, u.name, u.email, t.speciality
        FROM users u
        JOIN teachers t ON u.id = t.id
        WHERE u.role='teacher'
        ORDER BY u.id DESC
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()

    return data


def get_teacher_by_id(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.id, u.name, u.email, t.speciality
        FROM users u
        JOIN teachers t ON u.id = t.id
        WHERE u.id=%s
    """, (id,))

    teacher = cur.fetchone()
    cur.close()
    conn.close()

    return teacher


def add_teacher(name, email, password, speciality):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, 'teacher')
        RETURNING id
    """, (name, email, password))

    user_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO teachers (id, speciality)
        VALUES (%s, %s)
    """, (user_id, speciality))

    conn.commit()
    cur.close()
    conn.close()


def update_teacher(id, name, email, speciality):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users SET name=%s, email=%s WHERE id=%s
    """, (name, email, id))

    cur.execute("""
        UPDATE teachers SET speciality=%s WHERE id=%s
    """, (speciality, id))

    conn.commit()
    cur.close()
    conn.close()


def delete_teacher(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=%s", (id,))

    conn.commit()
    cur.close()
    conn.close()


def search_teachers(query):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.id, u.name, u.email, t.speciality
        FROM users u
        JOIN teachers t ON u.id = t.id
        WHERE u.role='teacher'
        AND (
            LOWER(u.name) LIKE %s OR
            LOWER(t.speciality) LIKE %s
        )
    """, (f"%{query.lower()}%", f"%{query.lower()}%"))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return data