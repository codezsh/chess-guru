from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QTextEdit
from PyQt6.QtGui import QFont
from ui.board import ChessBoard
from core.statehandler import state_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess Guru")
        self.setGeometry(100, 100, 800, 600)
        self.uiLayout()

    def uiLayout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        chessboard = ChessBoard(state_manager.board)
        infobox = QWidget()

        hlayout = QHBoxLayout()
        hlayout.addWidget(chessboard, 6)
        hlayout.addWidget(infobox, 2)

        heading = QLabel("Discussion panel")
        heading.setFont(QFont("Arial", 12))

        analysis = QWidget()
        analysis.setLayout(QVBoxLayout())
        analysis.layout().addWidget(QLabel("Analysis and responses from AI"))

        chatinput = QWidget()
        chatinput.setLayout(QHBoxLayout())

        textbox = QTextEdit()
        textbox.setPlaceholderText("Enter your message")
        textbox.setFont(QFont("Arial", 12))
        textbox.setStyleSheet("padding: 10px;")
        textbox.setFixedHeight(60)  # Set a reasonable height

        button = QPushButton("send")
        button.setFixedHeight(60)  # Match the height of the textbox

        chatinput.layout().addWidget(textbox)
        chatinput.layout().addWidget(button)

        infobox.setLayout(QVBoxLayout())
        infobox.layout().addWidget(heading)
        infobox.layout().addWidget(analysis)
        infobox.layout().addWidget(chatinput)
        infobox.layout().setStretchFactor(analysis, 1)
        infobox.layout().setStretchFactor(chatinput, 0)
        central_widget.setLayout(hlayout)


# Run Application
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
