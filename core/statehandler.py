# handles the state of the board

class StateHandler:
    def __init__(self):
        """ Initializes the board with pieces in starting position """
        # black pieces - small case
        # white pieces - upper case

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

        self.turn = "w"  # White starts
        self.castling = {"white": "KQ", "black": "kq"}
        self.en_passant = "-"
        self.halfmove_clock = 0
        self.fullmove_number = 1
    
    def update_board(self,moveinfo):
        pass

state_manager = StateHandler()
