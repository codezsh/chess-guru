from PyQt6.QtWidgets import QWidget, QFrame, QGridLayout
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap, QPainter


class DraggableWidget(QWidget):
    def __init__(self, svg_file, row, col, parent=None):
        super().__init__(parent)
        self.setFixedSize(55, 55)
        self.row, self.col = row, col
        self.svg_file = svg_file
        self.svg_renderer = QSvgRenderer(f"pieces/{svg_file}")

    def paintEvent(self, event):
        """ Render the SVG inside the widget """
        painter = QPainter(self)
        self.svg_renderer.render(painter)

    def get_drag_pixmap(self):
        """ Convert SVG to QPixmap for drag image """
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        self.svg_renderer.render(painter)
        painter.end()
        return pixmap

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(f"{self.row},{self.col},{self.svg_file}")

            drag.setPixmap(self.get_drag_pixmap())
            drag.setHotSpot(event.position().toPoint())
            drag.setMimeData(mime_data)

            drag.exec(Qt.DropAction.MoveAction)


class DroppableSquare(QFrame):
    def __init__(self, parent, row, col):
        super().__init__(parent)
        self.row, self.col = row, col
        self.setAcceptDrops(True)
        self.piece = None
        self.setFixedSize(65, 65)
        self.update_background()

    def update_background(self):
        if (self.row + self.col) % 2 == 0:
            self.setStyleSheet("background-color: #EEEED2;")  # Light square
        else:
            self.setStyleSheet("background-color: #769656;")  # Dark square

    def set_piece(self, piece):
        if self.piece:
            self.piece.deleteLater()
        self.piece = piece
        self.piece.setParent(self)
        self.piece.move(5, 5)
        self.piece.show()

    def clear_piece(self):
        if self.piece:
            self.piece.deleteLater()
            self.piece = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData().text().split(",")
        start_row, start_col, svg_file = int(data[0]), int(data[1]), data[2]

        source_square = self.parent().squares[start_row][start_col]
        source_square.clear_piece()

        new_piece = DraggableWidget(svg_file, self.row, self.col, self)
        self.set_piece(new_piece)
        event.acceptProposedAction()


class ChessBoard(QWidget):
    """ Manages the chessboard layout and piece placement """
    def __init__(self, state):
        super().__init__()
        self.board = state
        self.setFixedSize(560, 560)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.load_board()

    def load_board(self):
        for row in range(8):
            for col in range(8):
                square = DroppableSquare(self, row, col)

                piece_symbol = self.board[row * 8 + col]
                if piece_symbol != ".":
                    piece = DraggableWidget(self.get_svg_name(piece_symbol), row, col, square)
                    square.set_piece(piece)

                self.layout.addWidget(square, row, col)
                self.squares[row][col] = square

    def get_svg_name(self, piece):
        piece_map = {
            "P": "wP.svg", "N": "wN.svg", "B": "wB.svg", "R": "wR.svg", "Q": "wQ.svg", "K": "wK.svg",
            "p": "bP.svg", "n": "bN.svg", "b": "bB.svg", "r": "bR.svg", "q": "bQ.svg", "k": "bK.svg"
        }
        return piece_map.get(piece, "")
