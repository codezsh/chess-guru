from core.eventbus import Appbus
from core.legalmoves import ValidMoveGenerator
from core.boardhistory import MoveTree

class StateHandler:
    def __init__(self):
        self.initial_board = [
            "r", "n", "b", "q", "k", "b", "n", "r",
            "p", "p", "p", "p", "p", "p", "p", "p",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            "P", "P", "P", "P", "P", "P", "P", "P",
            "R", "N", "B", "Q", "K", "B", "N", "R"
        ]

        self.board = list(self.initial_board)
        self.turn = "w"
        self.activepiece = None

        self.has_king_moved = {"w": False, "b": False}
        self.has_rook_moved = {"w": {"0": False, "7": False}, "b": {"0": False, "7": False}}

        self.move_tree = MoveTree()

        Appbus.on("piece_moved", self.handle_piece_move)
        Appbus.on("get_board", lambda: self.board)
        Appbus.on("print_board", self.print_board)
        Appbus.on("get_turn", lambda: self.turn)
        Appbus.on("set_active_piece", self.register_active_piece)
        Appbus.on("get_active_piece", lambda: self.activepiece)
        Appbus.on("get_piece_at", self.get_piece_at)

    def get_piece_at(self, row, col):
        return self.board[row * 8 + col]

    def set_piece_at(self, row, col, symbol):
        self.board[row * 8 + col] = symbol

    def register_active_piece(self, row, col):
        self.activepiece = (row, col)
        legal_move_handler = ValidMoveGenerator()
        Appbus.emit("hlt_legal_moves", legal_move_handler.get_moves(row, col))

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece_at(start_row, start_col)

        if piece.lower() == "p" and start_col != end_col and self.get_piece_at(end_row, end_col) == ".":
            last_node = self.move_tree.current
            if last_node.move:
                last_end = last_node.move["to"]
                last_start = last_node.move["from"]
                last_piece = last_node.move["piece"]
                if last_piece.lower() == "p" and abs(last_start[0] - last_end[0]) == 2 and last_end[1] == end_col:
                    self.set_piece_at(last_end[0], last_end[1], ".")

        self.set_piece_at(end_row, end_col, piece)
        self.set_piece_at(start_row, start_col, ".")

        move_dict = {
            "from": (start_row, start_col),
            "to": (end_row, end_col),
            "piece": piece,
            "capture": self.get_piece_at(end_row, end_col) != "."
        }

        self.move_tree.add_move(move_dict)
        self.turn = "b" if self.turn == "w" else "w"
        Appbus.emit("refresh")

    def handle_piece_move(self, move):
        start = move["from"]
        end = move["to"]
        piece = self.get_piece_at(start[0], start[1])

        if piece.lower() == "k" and abs(start[1] - end[1]) == 2:
            self.handle_castle_move(start, end)
        else:
            self.move_piece(start[0], start[1], end[0], end[1])

    def handle_castle_move(self, start, end):
        row = start[0]
        direction = 1 if end[1] > start[1] else -1

        self.set_piece_at(end[0], end[1], self.get_piece_at(start[0], start[1]))
        self.set_piece_at(start[0], start[1], ".")

        rook_col = 0 if direction == -1 else 7
        new_rook_col = start[1] + direction
        self.set_piece_at(row, new_rook_col, self.get_piece_at(row, rook_col))
        self.set_piece_at(row, rook_col, ".")

        self.has_king_moved[self.turn] = True
        self.has_rook_moved[self.turn][str(new_rook_col)] = True

        move_dict = {
            "from": start,
            "to": end,
            "piece": "K",
            "castle": True
        }

        self.move_tree.add_move(move_dict)
        self.turn = "b" if self.turn == "w" else "w"
        Appbus.emit("refresh")

    def print_board(self):
        print("\n  a b c d e f g h")
        print(" +-----------------+")
        for row in range(8):
            row_str = f"{8 - row}|"
            for col in range(8):
                piece = self.get_piece_at(row, col)
                row_str += f"{piece if piece != '.' else '.'} "
            print(row_str + f"|{8 - row}")
        print(" +-----------------+")
        print("  a b c d e f g h\n")

state_manager = StateHandler()
