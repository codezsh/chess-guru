from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from core.eventbus import Appbus


class MoveHistory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.moves = []  # List of (white_move_dict, black_move_dict)
        self.current_halfmove = 0
        self.temp_move = None

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(10)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(container)

        title = QLabel("MOVE HISTORY")
        title.setStyleSheet("font: bold 12pt 'Arial'; color: white;")
        container_layout.addWidget(title)

        self.move_list_widget = QWidget()
        self.move_list_layout = QVBoxLayout()
        self.move_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.move_list_widget.setLayout(self.move_list_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.move_list_widget)
        scroll.setWidgetResizable(True)
        container_layout.addWidget(scroll)

        self.setFixedHeight(560)
