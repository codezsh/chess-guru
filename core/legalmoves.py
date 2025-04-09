from core.eventbus import Appbus


class PawnMoveGenerator:
    pass


class ValidMoveGenerator:
    def __init__(self):
        self.board = Appbus.emit_with_return("get_board")
        self.moves = []

    def get_moves(self, piece: str):
        pawn = PawnMoveGenerator()
        
        if piece.lower() == "P":
            return pawn.getLegalMoves()

        pass
