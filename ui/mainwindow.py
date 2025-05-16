from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout
)
from ui.menubar import MenuBar
from ui.movepanel import MoveHistory
from ui.chatpanel import ChatPanel
from ui.board import ChessBoardView


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

        hlayout = QHBoxLayout()
        chat_widget = ChatPanel()
        board_widget = ChessBoardView()
        move_widget = MoveHistory()

        hlayout.addWidget(chat_widget)
        hlayout.addWidget(board_widget)
        hlayout.addWidget(move_widget)

        central_widget.setLayout(hlayout)

