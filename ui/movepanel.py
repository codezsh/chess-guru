from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MoveHistory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        
        container = QWidget()
        container.setObjectName("MoveHistoryContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(10)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(container)

        title = QLabel("MOVE HISTORY")
        font = QFont("Arial", 11)
        font.setBold(True)
        title.setFont(font)

        container_layout.addWidget(title)

        self.move_list = QWidget()
        self.move_layout = QVBoxLayout()
        self.move_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.move_list.setLayout(self.move_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.move_list)
        scroll.setWidgetResizable(True)
        
        container_layout.addWidget(scroll)
        self.setFixedHeight(560)
       

    def add_move(self, move_number, white_move, black_move):
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(16)

        label_style = "color: white; font-size: 15px;"
        row_layout.addWidget(self._styled_label(f"{move_number}.", label_style))
        row_layout.addWidget(self._styled_label(white_move, label_style))
        row_layout.addWidget(self._styled_label(black_move, label_style))
        row_layout.addStretch()

        row_widget = QWidget()
        row_widget.setLayout(row_layout)
        self.move_layout.addWidget(row_widget)

    def _styled_label(self, text, style):
        label = QLabel(text)
        label.setStyleSheet(style)
        return label
