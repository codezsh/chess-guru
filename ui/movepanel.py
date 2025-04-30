from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from core.eventbus import Appbus
import os


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

        Appbus.on("piece_moved", self.piece_moved)

    def piece_moved(self, move):
        move["notation"] = self.generate_notation(move)

        if self.current_halfmove == 0:
            self.temp_move = move
            self.current_halfmove = 1
        else:
            self.moves.append((self.temp_move, move))
            self.temp_move = None
            self.current_halfmove = 0
            self.refresh()

    def refresh(self):
        while self.move_list_layout.count():
            child = self.move_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i, (white, black) in enumerate(self.moves, start=1):
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(20)

            move_num = QLabel(f"{i}.")
            move_num.setStyleSheet("color: white; font-size: 14px;")
            row_layout.addWidget(move_num)

            row_layout.addLayout(self.render_move(white))
            row_layout.addLayout(self.render_move(black))
            row_layout.addStretch()

            self.move_list_layout.addWidget(row)

    def render_move(self, move):
        layout = QHBoxLayout()
        layout.setSpacing(4)

        if os.path.exists(move.get("piece", "")):
            icon = QLabel()
            icon.setFixedSize(20, 20)
            icon.setPixmap(QPixmap(move["piece"]).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            layout.addWidget(icon)

        notation = move.get("notation", "?")
        text = QLabel(notation)
        text.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(text)

        return layout

    def reset_moves(self):
        self.moves.clear()
        self.temp_move = None
        self.current_halfmove = 0
        self.refresh()

    def generate_notation(self, move):
        piece_map = {
            "K": "K",
            "Q": "Q",
            "R": "R",
            "B": "B",
            "N": "N",
            "P": ""
        }

        from_row, from_col = move["from"]
        to_row, to_col = move["to"]
        col_map = "abcdefgh"
        row_map = "87654321"

        filename = os.path.basename(move["piece"])
        if not filename or len(filename) < 2:
            return "?"

        piece_letter = filename[1]  # e.g., 'N' from 'wN.svg'
        piece_notation = piece_map.get(piece_letter, "")
        from_square = f"{col_map[from_col]}{row_map[from_row]}"
        to_square = f"{col_map[to_col]}{row_map[to_row]}"

        # Castling
        if piece_letter == "K" and abs(to_col - from_col) == 2:
            return "O-O" if to_col > from_col else "O-O-O"

        # Capture detection: If destination square has enemy piece
        is_capture = self.is_capture(from_square, to_square)  # Optional: basic heuristic
        capture_symbol = "x" if is_capture else ""

        if piece_letter == "P":
            if is_capture:
                return f"{from_square[0]}x{to_square}"
            return to_square
        else:
            return f"{piece_notation}{capture_symbol}{to_square}"

    def is_capture(self, from_square, to_square):
        # TODO: Hook into actual board state to determine real captures.
        # Placeholder: return True if you want to test "x" notation
        return False
