from core.eventbus import Appbus
from core.legalmoves import ValidMoveGenerator

class StateHandler:
    def __init__(self):

        self.board = [
            "r", "n", "b", "q", "k", "b", "n", "r",
            "p", "p", "p", "p", "p", "p", "p", "p",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            "P", "P", "P", "P", "P", "P", "P", "P",
            "R", "N", "B", "Q", "K", "B", "N", "R"
        ]

        self.turn = "w"
        self.activepiece = None
        Appbus.on("piece_moved", self.handle_piece_move)
        Appbus.on("get_board", lambda : self.board)
        Appbus.on("print_board", self.print_board)
        Appbus.on("get_turn", lambda : self.turn)
        Appbus.on("set_active_piece", self.register_active_piece)
        Appbus.on("get_active_piece", lambda : self.activepiece)
    
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
        self.set_piece_at(end_row, end_col, piece)
        self.set_piece_at(start_row, start_col, ".")
        self.turn = "b" if self.turn == "w" else "w"
    
    def handle_piece_move(self, move):
        start = move["from"]
        end = move["to"]
        self.move_piece(start[0], start[1], end[0], end[1])    

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
