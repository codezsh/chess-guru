from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from core.eventbus import Appbus

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        board_menu = QMenu("Board", self)
        flip_action = QAction("Flip Board", self)
        

        flip_action.triggered.connect(lambda: Appbus.emit("flip_board"))
        board_menu.addAction(flip_action)
        
        self.addMenu(board_menu)


        self.setStyleSheet("""
        QMenu {
            padding: 6px;
            border-radius: 0px;
            border:1px solid #4a4a4a;
        }

        QMenu::item {
            padding: 5px 25px 5px 20px;
        }

        QMenu::item:selected {
            background-color: #3d3d3d;
        }
    
        """)
