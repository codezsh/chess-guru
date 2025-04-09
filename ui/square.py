from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from core.eventbus import Appbus
from core.legalmoves import ValidMoveGenerator
from ui.piece import Piece

class Square(QFrame):
    def __init__(self, parent, row, col):
        super().__init__(parent)
        self.row, self.col = row, col
        self.setAcceptDrops(True)
        self.piece = None
        self.show_dot = False
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

        if (start_row, start_col) == (self.row, self.col):
            event.ignore()
            return

        source_square = self.parent().squares[start_row][start_col]
        source_square.clear_piece()

        new_piece = Piece(svg_file, self.row, self.col, self)
        self.set_piece(new_piece)

        Appbus.emit("piece_moved", {
            "from": (start_row, start_col),
            "to": (self.row, self.col),
            "piece": svg_file
        })

        # Clear previous highlight
        validmoves = ValidMoveGenerator()
        parent = self.parent()
        if parent.highlighted_square:
            r, c = parent.highlighted_square
            parent.squares[r][c].set_highlight()
            parent.highlighted_square = None

        event.acceptProposedAction()


    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        if self.show_dot and not self.piece:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QColor(30, 30, 30, 150))  # Dark translucent dot
            painter.setPen(Qt.PenStyle.NoPen)
            radius = 10
            center = self.rect().center()
            painter.drawEllipse(center, radius, radius)
        
        painter.setPen(QColor(70, 70, 70))  # Dark text
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)


        if (not self.parent().flipped and self.row == 7) or (self.parent().flipped and self.row == 0):
            file_char = chr(ord('a') + self.col)
            painter.drawText(self.rect().adjusted(48, 48, -4, -4), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom, file_char)

        if (not self.parent().flipped and self.col == 0) or (self.parent().flipped and self.col == 7):
            rank_char = str(8 - self.row if not self.parent().flipped else self.row + 1)
            painter.drawText(self.rect().adjusted(4, 48, -48, -4), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom, rank_char)
        
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.piece:
                board = self.parent()
                if board.highlighted_square:
                    r, c = board.highlighted_square
                    board.squares[r][c].set_highlight(False)
                    board.highlighted_square = None
            else:
                Appbus.emit("highlight_piece", (self.row, self.col))
        return super().mousePressEvent(event)


    def set_highlight(self):
        self.update_background()
