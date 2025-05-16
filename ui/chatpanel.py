from PyQt6.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout

from PyQt6.QtGui import QFont

class ChatPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        heading = QLabel("DISCUSSION PANEL")
        font = QFont("Arial", 11)
        font.setBold(True)
        heading.setFont(font)


        analysis = QWidget()
        analysis.setLayout(QVBoxLayout())
        analysis.layout().addWidget(QLabel("Analysis and responses from AI"))

        chatinput = QWidget()
        chatinput.setLayout(QHBoxLayout())

        textbox = QTextEdit()
        textbox.setPlaceholderText("Enter your message")
        textbox.setFont(QFont("Arial", 12))
        textbox.setStyleSheet("padding: 10px;")
        textbox.setFixedHeight(60)

        button = QPushButton("send")
        button.setFixedHeight(60)

        chatinput.layout().addWidget(textbox)
        chatinput.layout().addWidget(button)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(heading)
        self.layout().addWidget(analysis)
        self.layout().addWidget(chatinput)
        self.layout().setStretchFactor(analysis, 1)
        self.layout().setStretchFactor(chatinput, 0)
