from core.eventbus import Appbus

class PawnMoveGenerator:
    def __init__(self, board):
        self.board = board

    def get_legal_moves(self, row, col, color):
        moves = []
        direction = -1 if color == "white" else 1

        if self.is_empty(row + direction, col):
            moves.append((row + direction, col))

            start_row = 6 if color == "white" else 1
            if row == start_row and self.is_empty(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))

        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
            if self.in_bounds(new_row, new_col):
                target = self.get_piece(new_row, new_col)
                if target != "." and self.is_opponent(target, color):
                    moves.append((new_row, new_col))

        return moves

    def get_piece(self, row, col):
        return self.board[row * 8 + col]

    def is_empty(self, row, col):
        return self.in_bounds(row, col) and self.get_piece(row, col) == "."

    def is_opponent(self, piece, color):
        return (piece.isupper() and color == "black") or (piece.islower() and color == "white")

    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8


class KnightMoveGenerator:
    def __init__(self, board):
        self.board = board

    def get_legal_moves(self, row, col, color):
        moves = []
        directions = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            if self.in_bounds(new_row, new_col):
                target = self.get_piece(new_row, new_col)
                if target == "." or self.is_opponent(target, color):
                    moves.append((new_row, new_col))

        return moves

    def get_piece(self, row, col):
        return self.board[row * 8 + col]

    def is_opponent(self, piece, color):
        return (piece.isupper() and color == "black") or (piece.islower() and color == "white")

    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8


class ValidMoveGenerator:
    def __init__(self):
        self.board = Appbus.emit_with_return("get_board")[0]

    def get_moves(self, row, col):
        piece = self.board[row * 8 + col]
        if piece == ".":
            return []

        color = "white" if piece.isupper() else "black"
        piece_type = piece.lower()

        if piece_type == "p":
            return PawnMoveGenerator(self.board).get_legal_moves(row, col, color)
        elif piece_type == "n":
            return KnightMoveGenerator(self.board).get_legal_moves(row, col, color)

        return []
