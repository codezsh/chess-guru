from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt

class ChessBoard(QWidget):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.setFixedSize(520, 520)  # Adjusted board size

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.load_board()

    def load_board(self):
        """ Load board UI with alternating colors and correct piece placement """
        for row in range(8):
            for col in range(8):
                square = QLabel(self)
                square.setFixedSize(65, 65)  # Ensure uniform square size
                square.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Set alternating square colors
                if (row + col) % 2 == 0:
                    square.setStyleSheet("background-color: #f0d9b5;")  # Light
                else:
                    square.setStyleSheet("background-color: #b58863;")  # Dark

                # Create a layout to hold the piece (if any)
                square_layout = QVBoxLayout(square)
                square_layout.setContentsMargins(0, 0, 0, 0)
                square_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Place pieces
                piece = self.board[row * 8 + col]
                if piece != ".":
                    svg_widget = QSvgWidget(f"pieces/{self.get_svg_name(piece)}")
                    svg_widget.setFixedSize(55, 55)  # Ensure it fits inside squares
                    square_layout.addWidget(svg_widget)

                self.layout.addWidget(square, row, col)
                self.squares[row][col] = square  # Store the QLabel

    def get_svg_name(self, piece):
        """ Convert piece notation to SVG filenames """
        piece_map = {
            "P": "wP.svg", "N": "wN.svg", "B": "wB.svg", "R": "wR.svg", "Q": "wQ.svg", "K": "wK.svg",
            "p": "bP.svg", "n": "bN.svg", "b": "bB.svg", "r": "bR.svg", "q": "bQ.svg", "k": "bK.svg"
        }
        return piece_map.get(piece, "")
