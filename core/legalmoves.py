from core.eventbus import Appbus

class ValidMoveGenerator:
    def __init__(self):
        self.board = Appbus.emit_with_return("get_board")
        print(self.board)
        self.moves = []

    def generate_legal_moves(self, piece):
        pass