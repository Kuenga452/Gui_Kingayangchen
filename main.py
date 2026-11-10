
import sys
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QHeaderView,
    QScrollArea
)


# DATABASE CLASS
class Student:

    def __init__(self):
        self.connection = sqlite3.connect("students.db")
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                gender TEXT,
                course TEXT,
                phone TEXT,
                marks REAL
            )
        """)

        self.connection.commit()

    def add_student(self, student):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO students
            VALUES (?, ?, ?, ?, ?, ?)
        """, student)

        self.connection.commit()

    def get_students(self):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM students ORDER BY student_id"
        )

        return cursor.fetchall()

    def update_student(self, student):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE students
            SET full_name = ?,
                gender = ?,
                course = ?,
                phone = ?,
                marks = ?
            WHERE student_id = ?
        """, (
            student[1],
            student[2],
            student[3],
            student[4],
            student[5],
            student[0]
        ))

        self.connection.commit()

    def delete_student(self, student_id):
        cursor = self.connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )

        self.connection.commit()


# MAIN WINDOW CLASS
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.db = Student()
        self.selected_id = None

        self.setWindowTitle("Student Record Management System")
        self.resize(1150, 800)
        self.setMinimumSize(800, 600)

        self.create_interface()
        self.apply_styles()
        self.load_students()

    # CREATE INTERFACE
    def create_interface(self):

        # SCROLL AREA
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.setCentralWidget(scroll_area)

        # CONTENT WIDGET INSIDE SCROLL AREA
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        content_widget.setLayout(main_layout)

        # TITLE
        title = QLabel("STUDENT RECORD MANAGEMENT SYSTEM")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel(
            "Manage student information and academic records"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # STUDENT INFORMATION SECTION
        self.form_group = QGroupBox("Student Information")

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(25, 25, 25, 25)

        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("Enter Student ID")

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Enter Full Name")

        self.gender = QComboBox()
        self.gender.addItems([
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ])

        self.course = QComboBox()
        self.course.addItems([
            "Select Course",
            "B.Ed ICT",
            "B.Ed Secondary",
            "B.Ed Primary",
            "B.A English",
            "B.A History"
        ])

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Enter Phone Number")

        self.marks = QDoubleSpinBox()
        self.marks.setRange(0, 100)
        self.marks.setDecimals(2)
        self.marks.setSuffix(" marks")

        form_layout.addRow("Student ID:", self.student_id)
        form_layout.addRow("Full Name:", self.full_name)
        form_layout.addRow("Gender:", self.gender)
        form_layout.addRow("Course:", self.course)
        form_layout.addRow("Phone Number:", self.phone)
        form_layout.addRow("Marks:", self.marks)

        self.form_group.setLayout(form_layout)

        main_layout.addWidget(self.form_group)

        # BUTTONS - HORIZONTAL
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.add_button = QPushButton("Add Student")
        self.update_button = QPushButton("Update Student")
        self.delete_button = QPushButton("Delete Student")
        self.clear_button = QPushButton("Clear Fields")

        self.add_button.setObjectName("addButton")
        self.update_button.setObjectName("updateButton")
        self.delete_button.setObjectName("deleteButton")
        self.clear_button.setObjectName("clearButton")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        # SEARCH SECTION
        search_layout = QHBoxLayout()

        search_label = QLabel("Search Student:")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by Student ID or Full Name"
        )

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        main_layout.addLayout(search_layout)

        # STUDENT RECORDS TABLE
        self.table_group = QGroupBox("Student Records")

        table_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Student ID",
            "Full Name",
            "Gender",
            "Course",
            "Phone Number",
            "Marks"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        # TABLE HEIGHT
        self.table.setMinimumHeight(300)

        table_layout.addWidget(self.table)

        self.table_group.setLayout(table_layout)

        main_layout.addWidget(self.table_group)

        # EXTRA SPACE AT BOTTOM
        main_layout.addStretch()

        # BUTTON CONNECTIONS
        self.add_button.clicked.connect(self.add_student)
        self.update_button.clicked.connect(self.update_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.clear_button.clicked.connect(self.clear_fields)

        self.table.cellClicked.connect(self.select_student)
        self.search_input.textChanged.connect(self.search_students)

    # ADD STUDENT
    def add_student(self):

        student = self.get_form_data()

        if not student:
            return

        try:
            self.db.add_student(student)

            QMessageBox.information(
                self,
                "Success",
                "Student added successfully!"
            )

            self.load_students()
            self.clear_fields()

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Duplicate ID",
                "This Student ID already exists."
            )

    # UPDATE STUDENT
    def update_student(self):

        if not self.selected_id:
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select a student from the table."
            )
            return

        student = self.get_form_data()

        if not student:
            return

        try:
            self.db.update_student(student)

            QMessageBox.information(
                self,
                "Success",
                "Student updated successfully!"
            )

            self.load_students()
            self.clear_fields()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

    # DELETE STUDENT
    def delete_student(self):

        if not self.selected_id:
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select a student to delete."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this student?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.db.delete_student(self.selected_id)

            QMessageBox.information(
                self,
                "Deleted",
                "Student deleted successfully!"
            )

            self.load_students()
            self.clear_fields()

    # GET FORM DATA
    def get_form_data(self):

        student_id = self.student_id.text().strip()
        full_name = self.full_name.text().strip()
        gender = self.gender.currentText()
        course = self.course.currentText()
        phone = self.phone.text().strip()
        marks = self.marks.value()

        if not student_id or not full_name or not phone:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please complete Student ID, Full Name and Phone Number."
            )
            return None

        if gender == "Select Gender" or course == "Select Course":
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please select Gender and Course."
            )
            return None

        return (
            student_id,
            full_name,
            gender,
            course,
            phone,
            marks
        )

    # LOAD STUDENTS
    def load_students(self):

        students = self.db.get_students()

        self.table.setRowCount(len(students))

        for row, student in enumerate(students):

            for column, value in enumerate(student):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(row, column, item)

    # SELECT STUDENT
    def select_student(self, row, column):

        self.selected_id = self.table.item(row, 0).text()

        self.student_id.setText(
            self.table.item(row, 0).text()
        )

        self.student_id.setReadOnly(True)

        self.full_name.setText(
            self.table.item(row, 1).text()
        )

        self.gender.setCurrentText(
            self.table.item(row, 2).text()
        )

        self.course.setCurrentText(
            self.table.item(row, 3).text()
        )

        self.phone.setText(
            self.table.item(row, 4).text()
        )

        self.marks.setValue(
            float(self.table.item(row, 5).text())
        )

    # SEARCH STUDENTS
    def search_students(self, text):

        students = self.db.get_students()

        filtered = [
            student for student in students
            if text.lower() in student[0].lower()
            or text.lower() in student[1].lower()
        ]

        self.table.setRowCount(len(filtered))

        for row, student in enumerate(filtered):

            for column, value in enumerate(student):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(row, column, item)

    # CLEAR FIELDS
    def clear_fields(self):

        self.student_id.clear()
        self.student_id.setReadOnly(False)

        self.full_name.clear()
        self.gender.setCurrentIndex(0)
        self.course.setCurrentIndex(0)
        self.phone.clear()
        self.marks.setValue(0)

        self.selected_id = None

        self.table.clearSelection()

    # STYLING
    def apply_styles(self):

        self.setStyleSheet("""

            QMainWindow {
                background-color: #F1F5F9;
            }

            QScrollArea {
                border: none;
                background-color: #F1F5F9;
            }

            QWidget {
                background-color: transparent;
            }

            QLabel#title {
                color: #FFFFFF;
                font-size: 25px;
                font-weight: bold;
                padding: 5px;
            }

            QLabel#subtitle {
                color: #FFFFFF;
                font-size: 13px;
                padding-bottom: 10px;
            }

            QGroupBox {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 10px;
                margin-top: 1px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                color: #0F172A;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 6px;
            }

            QLabel {
                color: #FFFFFF;
                font-size: 13px;
            }

            QLineEdit,
            QComboBox,
            QDoubleSpinBox,
            QComboBox QLineEdit,
            QDoubleSpinBox QLineEdit {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 9px;
                min-height: 20px;
                selection-background-color: #BFDBFE;
                selection-color: #000000;
            }

            QLineEdit:focus,
            QComboBox:focus,
            QDoubleSpinBox:focus {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #3B82F6;
            }

            QLineEdit:read-only {
                background-color: #FFFFFF;
                color: #000000;
            }

            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #000000;
                selection-background-color: #DBEAFE;
                selection-color: #000000;
            }

            QPushButton {
                background-color: #475569;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 11px 18px;
                font-size: 13px;
                font-weight: bold;
                min-height: 20px;
            }

            QPushButton:hover {
                background-color: #334155;
            }

            QPushButton:pressed {
                background-color: #1E293B;
            }

            QPushButton#addButton {
                background-color: #2563EB;
            }

            QPushButton#addButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton#updateButton {
                background-color: #475569;
            }

            QPushButton#deleteButton {
                background-color: #64748B;
            }

            QPushButton#clearButton {
                background-color: #94A3B8;
            }

            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F8FAFC;
                color: #1E293B;
                gridline-color: #E2E8F0;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                selection-background-color: #DBEAFE;
                selection-color: #000000;
            }

            QHeaderView::section {
                background-color: #334155;
                color: #FFFFFF;
                padding: 11px;
                border: none;
                font-weight: bold;
            }

        """)


# RUN APPLICATION
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
