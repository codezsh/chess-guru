from core.eventbus import Appbus

class PieceMoveGenerator:
    def __init__(self, board):
        self.board = board

    def get_piece(self, row, col):
        return self.board[row * 8 + col]

    def is_opponent(self, piece, color):
        return (piece.isupper() and color == "black") or (piece.islower() and color == "white")

    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty(self, row, col):
        return self.in_bounds(row, col) and self.get_piece(row, col) == "."

    def simulate_move(self, board, start, end):
        new_board = board[:]
        start_idx = start[0]*8 + start[1]
        end_idx = end[0]*8 + end[1]
        new_board[end_idx] = new_board[start_idx]
        new_board[start_idx] = "."
        return new_board

    def king_in_check(self, board, color):
        king = "K" if color == "white" else "k"
        king_pos = next(((r, c) for r in range(8) for c in range(8) if board[r * 8 + c] == king), None)
        if not king_pos:
            return True

        for r in range(8):
            for c in range(8):
                piece = board[r * 8 + c]
                if piece == ".":
                    continue
                if (piece.isupper() and color == "white") or (piece.islower() and color == "black"):
                    continue
                vm = ValidMoveGenerator(board)
                if king_pos in vm.get_raw_moves(r, c):
                    return True
        return False

class SlidingPieceMixin:
    def sliding_moves(self, row, col, color, directions):
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.in_bounds(r, c):
                target = self.get_piece(r, c)
                if target == ".":
                    moves.append((r, c))
                elif self.is_opponent(target, color):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class PawnMoveGenerator(PieceMoveGenerator):
    def get_legal_moves(self, row, col, color):
        moves = []
        direction = -1 if color == "white" else 1
        start_row = 6 if color == "white" else 1
        enemy_pawn = "p" if color == "white" else "P"
        own_pawn = "P" if color == "white" else "p"

        # Forward one square
        if self.is_empty(row + direction, col):
            moves.append((row + direction, col))
            # Two squares
            if row == start_row and self.is_empty(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))

        # Captures
        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if self.in_bounds(r, c):
                target = self.get_piece(r, c)
                if target != "." and self.is_opponent(target, color):
                    moves.append((r, c))

        # En passant
        enpassant_row = 3 if color == "white" else 4
        if row == enpassant_row:
            for dc in [-1, 1]:
                adj_col = col + dc
                if self.in_bounds(row, adj_col):
                    side_piece = self.get_piece(row, adj_col)
                    if side_piece == enemy_pawn:
                        behind = row + direction
                        if self.is_empty(behind, adj_col):
                            # Check if pawn just advanced (by checking starting position empty)
                            two_behind = row - direction * 2
                            if self.in_bounds(two_behind, adj_col) and self.get_piece(two_behind, adj_col) == ".":
                                moves.append((row + direction, adj_col))

        return moves

class KnightMoveGenerator(PieceMoveGenerator):
    def get_legal_moves(self, row, col, color):
        moves = []
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            r, c = row + dr, col + dc
            if self.in_bounds(r, c):
                target = self.get_piece(r, c)
                if target == "." or self.is_opponent(target, color):
                    moves.append((r, c))
        return moves

class BishopMoveGenerator(PieceMoveGenerator, SlidingPieceMixin):
    def get_legal_moves(self, row, col, color):
        return self.sliding_moves(row, col, color, [(-1,-1),(-1,1),(1,-1),(1,1)])

class RookMoveGenerator(PieceMoveGenerator, SlidingPieceMixin):
    def get_legal_moves(self, row, col, color):
        return self.sliding_moves(row, col, color, [(-1,0),(1,0),(0,-1),(0,1)])

class QueenMoveGenerator(PieceMoveGenerator, SlidingPieceMixin):
    def get_legal_moves(self, row, col, color):
        return self.sliding_moves(row, col, color, [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)])

class KingMoveGenerator(PieceMoveGenerator):
    def get_legal_moves(self, row, col, color):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    target = self.get_piece(r, c)
                    if target == "." or self.is_opponent(target, color):
                        moves.append((r, c))

        # Castling
        if color == "white" and row == 7 and col == 4:
            if self.get_piece(7, 7) == "R" and self.board[7 * 8 + 5] == "." and self.board[7 * 8 + 6] == ".":
                moves.append((7, 6))  # Kingside
            if self.get_piece(7, 0) == "R" and self.board[7 * 8 + 1] == "." and self.board[7 * 8 + 2] == "." and self.board[7 * 8 + 3] == ".":
                moves.append((7, 2))  # Queenside

        if color == "black" and row == 0 and col == 4:
            if self.get_piece(0, 7) == "r" and self.board[0 * 8 + 5] == "." and self.board[0 * 8 + 6] == ".":
                moves.append((0, 6))  # Kingside
            if self.get_piece(0, 0) == "r" and self.board[0 * 8 + 1] == "." and self.board[0 * 8 + 2] == "." and self.board[0 * 8 + 3] == ".":
                moves.append((0, 2))  # Queenside

        return moves

class ValidMoveGenerator:
    def __init__(self, board=None):
        self.board = board or Appbus.emit_with_return("get_board")[0]

    def get_raw_moves(self, row, col):
        piece = self.board[row * 8 + col]
        if piece == ".":
            return []
        color = "white" if piece.isupper() else "black"
        piece_type = piece.lower()

        generators = {
            "p": PawnMoveGenerator,
            "n": KnightMoveGenerator,
            "b": BishopMoveGenerator,
            "r": RookMoveGenerator,
            "q": QueenMoveGenerator,
            "k": KingMoveGenerator,
        }

        generator_class = generators.get(piece_type)
        if generator_class:
            return generator_class(self.board).get_legal_moves(row, col, color)
        return []

    def get_moves(self, row, col):
        raw_moves = self.get_raw_moves(row, col)
        piece = self.board[row * 8 + col]
        color = "white" if piece.isupper() else "black"
        legal_moves = []

        for move in raw_moves:
            new_board = PieceMoveGenerator(self.board).simulate_move(self.board, (row, col), move)
            if not PieceMoveGenerator(new_board).king_in_check(new_board, color):
                legal_moves.append(move)

        return legal_moves
