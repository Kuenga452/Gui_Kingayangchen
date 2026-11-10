import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)


class HelloWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("PyQt6 Hello World")
        self.setGeometry(100, 100, 350, 200)

        # Create a label
        self.label = QLabel("Hello, World!")
        self.label.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        # Create a button
        self.button = QPushButton("Click Me")

        # Connect button click event
        self.button.clicked.connect(self.show_message)

        # Arrange widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_message(self):
        self.label.setText("Welcome to PyQt6!")


# Run the application
app = QApplication(sys.argv)

window = HelloWindow()
window.show()

sys.exit(app.exec())