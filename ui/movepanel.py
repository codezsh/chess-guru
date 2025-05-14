from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer  # Import QSvgRenderer to handle SVG files
import os

from core.eventbus import Appbus

class MoveHistory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.moves = []  # List of (white_move_dict, black_move_dict)
        self.current_halfmove = 0
        self.temp_move = None

        # Layout for the Move History
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

        # Hook into Appbus to listen for moves
        Appbus.on("piece_moved", self.piece_moved)

    def piece_moved(self, move):
        move["notation"] = self.generate_notation(move)

        # Pairing white and black moves
        if self.current_halfmove == 0:
            self.temp_move = move
            self.current_halfmove = 1
        else:
            self.moves.append((self.temp_move, move))
            self.temp_move = None
            self.current_halfmove = 0
            self.refresh()

    def refresh(self):
        # Clear previous annotations
        while self.move_list_layout.count():
            child = self.move_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add all moves
        for i, (white, black) in enumerate(self.moves, start=1):
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(20)

            move_num = QLabel(f"{i}.")
            move_num.setStyleSheet("color: white; font-size: 14px;")
            row_layout.addWidget(move_num)

            row_layout.addLayout(self.render_move(white))  # White move
            row_layout.addLayout(self.render_move(black))  # Black move
            row_layout.addStretch()

            self.move_list_layout.addWidget(row)

    def render_move(self, move):
        layout = QHBoxLayout()
        layout.setSpacing(4)

        # Icon for the piece (if any)
        piece_icon = move.get("piece", "")
        
        if piece_icon:
            # Construct the correct path to the pieces folder
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'pieces', piece_icon)

            if os.path.exists(icon_path):
                icon = QLabel()
                icon.setFixedSize(20, 20)
                
                # Load the SVG using QSvgRenderer
                renderer = QSvgRenderer(icon_path)
                if renderer.isValid():
                    # Create a pixmap and render the SVG on it
                    pixmap = QPixmap(20, 20)
                    pixmap.fill(Qt.GlobalColor.transparent)  # Set the background to transparent
                    
                    # Paint the SVG onto the pixmap
                    painter = QPainter(pixmap)
                    renderer.render(painter)
                    painter.end()
                    
                    # Set the pixmap to the QLabel
                    icon.setPixmap(pixmap)
                else:
                    print(f"Failed to load SVG icon from {icon_path}")
                    # Optional: use a fallback image if SVG fails
                    fallback_pixmap = QPixmap("path_to_default_icon.svg")
                    icon.setPixmap(fallback_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

                layout.addWidget(icon)
            else:
                print(f"Icon file does not exist at {icon_path}")
        else:
            print("No piece icon provided")

        # Move notation (e.g., e4, Nf3, O-O)
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

        piece_letter = move["piece"].upper() if move["piece"] else ''
        from_square = f"{col_map[from_col]}{row_map[from_row]}"
        to_square = f"{col_map[to_col]}{row_map[to_row]}"

        # Castling notation (e.g., O-O or O-O-O)
        if piece_letter == "K" and abs(to_col - from_col) == 2:
            return "O-O" if to_col > from_col else "O-O-O"

        is_capture = self.is_capture(from_square, to_square)
        capture_symbol = "x" if is_capture else ""

        
        if piece_letter == "P":
            if is_capture:
                return f"{from_square[0]}x{to_square}"
            return to_square

        return f"{piece_letter}{capture_symbol}{to_square}"

    def is_capture(self, from_square, to_square):
        from_row, from_col = self.get_position_from_square(from_square)
        to_row, to_col = self.get_position_from_square(to_square)
        target_piece = Appbus.emit_with_return("get_piece_at", to_row, to_col)[0]

        
        if target_piece != ".":
            moving_piece = Appbus.emit_with_return("get_piece_at", from_row, from_col)[0]
            if moving_piece.isupper() and target_piece.islower():
                return True
            elif moving_piece.islower() and target_piece.isupper():
                return True

        return False

    def get_position_from_square(self, square):
        col_map = "abcdefgh"
        row_map = "87654321"
        col = col_map.index(square[0])
        row = row_map.index(square[1])
        return row, col
