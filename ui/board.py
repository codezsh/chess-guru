from PyQt6.QtWidgets import QWidget, QGridLayout
from core.eventbus import Appbus
from ui.square import Square
from ui.piece import Piece


class Board(QWidget):
    def __init__(self, state):
        super().__init__()
        self.board = state
        self.flipped = False


        self.setFixedSize(560, 560)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.load_board()

        self.highlighted_square = None
        self.valid_targets = set()

        
        Appbus.on("flip_board", self.flip_board)
        Appbus.on("highlight_piece", self.highlight_square)
        Appbus.on("hlt_legal_moves", self.highlight_squares)


    def load_board(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for r in range(8):
            for c in range(8):
                row = 7 - r if self.flipped else r
                col = 7 - c if self.flipped else c

                square = Square(self, row, col)

                piece_symbol = self.board[row * 8 + col]
                if piece_symbol != ".":
                    piece = Piece(Board.get_svg_name(piece_symbol), row, col, square)
                    square.set_piece(piece)

                self.layout.addWidget(square, r, c)
                self.squares[row][col] = square

    @staticmethod
    def get_svg_name(piece):
        piece_map = {
            "P": "wP.svg", "N": "wN.svg", "B": "wB.svg", "R": "wR.svg", "Q": "wQ.svg", "K": "wK.svg",
            "p": "bP.svg", "n": "bN.svg", "b": "bB.svg", "r": "bR.svg", "q": "bQ.svg", "k": "bK.svg"
        }
        return piece_map.get(piece, "")

    def highlight_squares(self, positions):
        self.valid_targets = set(positions)
        for r in range(8):
            for c in range(8):
                if self.squares[r][c].show_dot:
                    self.squares[r][c].show_dot = False
                    self.squares[r][c].update()

        for row, col in positions:
            self.squares[row][col].show_dot = True
            self.squares[row][col].update()


    def flip_board(self):
        self.flipped = not self.flipped
        self.load_board()
    
    def highlight_square(self, pos):
        if self.highlighted_square:
            r, c = self.highlighted_square
            self.squares[r][c].set_highlight(False)

        r, c = pos
        self.highlighted_square = (r, c)
        self.squares[r][c].set_highlight()

    def clear_highlights(self):
        for r in range(8):
            for c in range(8):
                if self.squares[r][c].show_dot:
                    self.squares[r][c].show_dot = False
                    self.squares[r][c].update()

        if self.highlighted_square:
            r, c = self.highlighted_square
            self.squares[r][c].set_highlight(False)
            self.highlighted_square = None

        self.valid_targets.clear()
