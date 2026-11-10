
import database


class StudentManager:

    def __init__(self):
        database.create_table()

    def add_student(self, student):
        database.add_student(student)

    def get_students(self):
        return database.get_students()

    def update_student(self, student):
        return database.update_student(student)

    def delete_student(self, student_id):
        return database.delete_student(student_id)

    def search_students(self, keyword):
        return database.search_students(keyword)
