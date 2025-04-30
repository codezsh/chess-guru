from PyQt6.QtWidgets import QWidget, QFrame
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap, QPainter, QColor
from core.eventbus import Appbus

class Piece(QWidget):
    def __init__(self, svg_file, row, col, parent=None):
        super().__init__(parent)
        self.setFixedSize(55, 55)
        self.row, self.col = row, col
        self.svg_file = svg_file
        self.svg_renderer = QSvgRenderer(f"pieces/{svg_file}")
        self.setMouseTracking(True)

        self.hovered = False
        self.active = False
    
    def isValid(self):
        if self.parent() is None:
            return False
        return True

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            parent = self.parent()
            current_turn = Appbus.emit_with_return("get_turn")[0]

            if not self.svg_file or len(self.svg_file) < 1:
                return

            piece_color = self.svg_file[0].lower()

            if self.hovered and piece_color == current_turn and not (
                isinstance(parent, QFrame) and parent.styleSheet().startswith("background-color: #7faec7")
            ):
                painter.fillRect(self.rect(), QColor(255, 255, 0, 80))
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

            if self.active:
                painter.fillRect(self.rect(), QColor(0, 255, 0, 80))

            self.svg_renderer.render(painter)

            if isinstance(parent, QFrame) and getattr(parent, "show_dot", False):
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setBrush(QColor(0, 153, 0, 130))
                painter.setPen(Qt.PenStyle.NoPen)
                center = self.rect().center()
                painter.drawEllipse(center, 8, 8)
        except RuntimeError:
            pass
    
    def get_drag_pixmap(self):
        try:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            self.svg_renderer.render(painter)
            painter.end()
            return pixmap
        except RuntimeError:
            return QPixmap()

    def mousePressEvent(self, event):
        try:
            if event.button() != Qt.MouseButton.LeftButton:
                return

            current_turn = Appbus.emit_with_return("get_turn")[0]
            piece_color = self.svg_file[0].lower()

            if piece_color != current_turn:
                return

            Appbus.emit("set_active_piece", self.row, self.col)
            self.active = True

            if not self.isValid():
                return

            self.update()

            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(f"{self.row},{self.col},{self.svg_file}")
            drag.setPixmap(self.get_drag_pixmap())
            drag.setHotSpot(event.position().toPoint())
            drag.setMimeData(mime_data)
            result = drag.exec(Qt.DropAction.MoveAction)

            if not self.isValid():
                return

            new_pos = Appbus.emit_with_return("get_active_piece")[0]

            if new_pos == (self.row, self.col) or (not new_pos or len(new_pos) != 2):
                self.active = False
                if self.isValid():
                    self.update()
                return

            Appbus.emit("piece_moved", {
                "from": (self.row, self.col),
                "to": new_pos,
                "piece": self.svg_file
            })

            self.active = False
            if self.isValid():
                self.update()
        except RuntimeError:
            pass
            self.active = False

    def enterEvent(self, event):
        try:
            self.hovered = True
            self.update()
            return super().enterEvent(event)
        except RuntimeError:
            pass
    
    def leaveEvent(self, event):
        try:
            self.hovered = False
            self.update()
            return super().leaveEvent(event)
        except RuntimeError:
            pass
