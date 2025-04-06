"""Handles the state of the board"""

from core.eventbus import AppBus

class StateHandler:
    def __init__(self):
        """
        Initializes the board with pieces in starting position
        # black pieces - small case
        # white pieces - upper case
        """

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
        self.castling = {"white": "KQ", "black": "kq"}
        self.en_passant = "-"
        self.halfmove_clock = 0
        self.fullmove_number = 1

        AppBus.on("piece_moved", self.handle_piece_move)

    
    def get_piece_at(self, row, col):
        return self.board[row * 8 + col]

    def set_piece_at(self, row, col, symbol):
        self.board[row * 8 + col] = symbol

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
        '''for debugging purposes'''
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
