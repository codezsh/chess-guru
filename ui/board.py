from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsRectItem
)
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QPainter

BOARD_SIZE = 8
SQUARE_SIZE = 64

PIECE_SVGS = {
    "P": "wP.svg",
    "N": "wN.svg",
    "B": "wB.svg",
    "R": "wR.svg",
    "Q": "wQ.svg",
    "K": "wK.svg",
    "p": "bP.svg",
    "n": "bN.svg",
    "b": "bB.svg",
    "r": "bR.svg",
    "q": "bQ.svg",
    "k": "bK.svg",
}

STARTING_FEN = (
    "rnbqkbnr"
    "pppppppp"
    "........"
    "........"
    "........"
    "........"
    "PPPPPPPP"
    "RNBQKBNR"
)

from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt, QRectF

class DraggableSvgPiece(QGraphicsSvgItem):
    def __init__(self, svg_file, row, col):
        super().__init__(svg_file)
        self.setFlags(self.GraphicsItemFlag.ItemIsMovable)
        self.row = row
        self.col = col
        self.setScale((SQUARE_SIZE / 45) * 0.85)
        scaled_size = 45 * (SQUARE_SIZE / 45) * 0.85
        offset = (SQUARE_SIZE - scaled_size) / 2
        self.setPos(col * SQUARE_SIZE + offset, row * SQUARE_SIZE + offset)


        self.drag_offset = None
        self.highlight_rect = QGraphicsRectItem(self)
        self.highlight_rect.setRect(QRectF(0, 0, 45, 45))  # matches original SVG size
        self.highlight_rect.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.DotLine))
        self.highlight_rect.setVisible(False)

    def mousePressEvent(self, event):
        self.drag_offset = self.pos() - event.scenePos()
        self.highlight_rect.setVisible(True)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_offset is not None:
            new_pos = event.scenePos() + self.drag_offset
            self.setPos(new_pos)
            self.highlight_rect.setVisible(False)  # Hide while dragging
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        scale = (SQUARE_SIZE / 45) * 0.85
        scaled_size = 45 * scale
        offset = (SQUARE_SIZE - scaled_size) / 2

        x = round((self.x() - offset) / SQUARE_SIZE) * SQUARE_SIZE + offset
        y = round((self.y() - offset) / SQUARE_SIZE) * SQUARE_SIZE + offset

        self.setPos(x, y)
        self.drag_offset = None
        super().mouseReleaseEvent(event)



class ChessBoardView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 ChessBoard with SVG Pieces")
        self.setFixedSize(BOARD_SIZE * SQUARE_SIZE + 2, BOARD_SIZE * SQUARE_SIZE + 2)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE)

        self.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.draw_board()
        self.place_pieces()

    def draw_board(self):
        colors = [QColor("#EEEED2"), QColor("#769656")]
        overlap = 1
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = QGraphicsRectItem(
                    col * SQUARE_SIZE - (overlap // 2),
                    row * SQUARE_SIZE - (overlap // 2),
                    SQUARE_SIZE + overlap,
                    SQUARE_SIZE + overlap,
                )
                rect.setBrush(colors[(row + col) % 2])
                rect.setPen(QPen(Qt.PenStyle.NoPen))
                self.scene.addItem(rect)

    def place_pieces(self):
        for i, piece_char in enumerate(STARTING_FEN):
            row = i // BOARD_SIZE
            col = i % BOARD_SIZE
            if piece_char != ".":
                svg_file = "pieces/" + PIECE_SVGS.get(piece_char)
                if svg_file:
                    piece_item = DraggableSvgPiece(svg_file, row, col)
                    self.scene.addItem(piece_item)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.viewport().update()

    def moveEvent(self, event):
        super().moveEvent(event)
        self.viewport().update()
