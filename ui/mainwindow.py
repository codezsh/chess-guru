from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtGui import QFont
from ui.board import Board
from core.statehandler import state_manager
from ui.menubar import MenuBar
from ui.movepanel import MoveHistory


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess Guru")
        self.setGeometry(100, 100, 800, 600)
        self.setMenuBar(MenuBar(self))
        self.uiLayout()

    def uiLayout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        infobox = QWidget()

        hlayout = QHBoxLayout()

        move_widget = MoveHistory()

        hlayout.addWidget(infobox)
        hlayout.addWidget(Board(state_manager.board))
        hlayout.addWidget(move_widget)


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

        infobox.setLayout(QVBoxLayout())
        infobox.layout().addWidget(heading)
        infobox.layout().addWidget(analysis)
        infobox.layout().addWidget(chatinput)
        infobox.layout().setStretchFactor(analysis, 1)
        infobox.layout().setStretchFactor(chatinput, 0)
        central_widget.setLayout(hlayout)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
