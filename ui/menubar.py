from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction
from core.eventbus import Appbus


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        board_actions = [
            (QAction("Flip Board", self), lambda: Appbus.emit("flip_board")),
            (QAction("Reset Board", self), None),
            (QAction("Load Position", self), None),
            (QAction("Load game", self), None),
        ]

        analysis_actions = [
            (QAction("Analysis", self), None),
            (QAction("Top lines", self), None),
        ]

        learn_actions = [
            (QAction("Opening", self), None),
            (QAction("End games", self), None),
            (QAction("Patterns", self), None),
        ]

        menus = [(QMenu("Board", self), board_actions), (QMenu("Analysis", self), analysis_actions), (QMenu("Learn", self), learn_actions)]

        self.load_menus(menus)
        self.setStyleSheet(
            """
        QMenu {
            padding: 5px;
            border-radius: 0px;
            border: 1px solid rgba(0, 0, 0, 50);
        }  
        """
        )

    def load_menus(self, items):
        for menu, actions in items:
            for action, callback in actions:
                if callback:
                    action.triggered.connect(callback)
                menu.addAction(action)
            self.addMenu(menu)