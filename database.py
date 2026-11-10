
import sqlite3

DATABASE_NAME = "students.db"


def connect_database():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            class_name TEXT NOT NULL,
            phone TEXT,
            marks REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_student(student):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (student_id, name, gender, class_name, phone, marks)
        VALUES (?, ?, ?, ?, ?, ?)
    """, student)

    connection.commit()
    connection.close()


def get_students():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students ORDER BY student_id")

    records = cursor.fetchall()
    connection.close()

    return records


def update_student(student):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?, gender=?, class_name=?, phone=?, marks=?
        WHERE student_id=?
    """, (
        student[1], student[2], student[3],
        student[4], student[5], student[0]
    ))

    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    connection.commit()
    connection.close()


def search_students(keyword):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE student_id LIKE ? OR name LIKE ?
        ORDER BY student_id
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()
    connection.close()

    return records
