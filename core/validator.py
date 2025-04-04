class ChessValidator:
    def __init__(self, state_handler):
        self.state_handler = state_handler
        self.move_patterns = {
            'P': self.get_pawn_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'R': self.get_rook_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }
    
    def get_valid_moves(self, position):
        index = self.state_handler.position_to_index(position)
        piece = self.state_handler.board[index]
        if piece == '.':
            return []
        
        piece_type = piece.upper()
        is_white = piece.isupper()
        
        move_generator = self.move_patterns.get(piece_type)
        if not move_generator:
            return []
        
        return move_generator(position, is_white)
    
    def get_pawn_moves(self, position, is_white):
        moves = []
        file, rank = position[0], int(position[1])
        direction = 1 if is_white else -1
        
        # Standard move
        new_rank = rank + direction
        if 1 <= new_rank <= 8:
            new_pos = f"{file}{new_rank}"
            if self.state_handler.board[self.state_handler.position_to_index(new_pos)] == '.':
                moves.append(new_pos)
        
        return moves
    
    def get_knight_moves(self, position, is_white):
        moves = []
        file, rank = position[0], int(position[1])
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        for df, dr in knight_moves:
            new_file = chr(ord(file) + df)
            new_rank = rank + dr
            if 'a' <= new_file <= 'h' and 1 <= new_rank <= 8:
                new_pos = f"{new_file}{new_rank}"
                target_piece = self.state_handler.board[self.state_handler.position_to_index(new_pos)]
                if target_piece == '.' or (is_white and target_piece.islower()) or (not is_white and target_piece.isupper()):
                    moves.append(new_pos)
        
        return moves
    
    def get_bishop_moves(self, position, is_white):
        return self.get_sliding_moves(position, is_white, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
    
    def get_rook_moves(self, position, is_white):
        return self.get_sliding_moves(position, is_white, [(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    def get_queen_moves(self, position, is_white):
        return self.get_sliding_moves(position, is_white, [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)])
    
    def get_king_moves(self, position, is_white):
        moves = []
        file, rank = position[0], int(position[1])
        king_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for df, dr in king_moves:
            new_file = chr(ord(file) + df)
            new_rank = rank + dr
            if 'a' <= new_file <= 'h' and 1 <= new_rank <= 8:
                new_pos = f"{new_file}{new_rank}"
                target_piece = self.state_handler.board[self.state_handler.position_to_index(new_pos)]
                if target_piece == '.' or (is_white and target_piece.islower()) or (not is_white and target_piece.isupper()):
                    moves.append(new_pos)
        
        return moves
    
    def get_sliding_moves(self, position, is_white, directions):
        moves = []
        file, rank = position[0], int(position[1])
        
        for df, dr in directions:
            new_file, new_rank = file, rank
            while True:
                new_file = chr(ord(new_file) + df)
                new_rank += dr
                if 'a' <= new_file <= 'h' and 1 <= new_rank <= 8:
                    new_pos = f"{new_file}{new_rank}"
                    target_piece = self.state_handler.board[self.state_handler.position_to_index(new_pos)]
                    if target_piece == '.':
                        moves.append(new_pos)
                    elif (is_white and target_piece.islower()) or (not is_white and target_piece.isupper()):
                        moves.append(new_pos)
                        break
                    else:
                        break
                else:
                    break
        
        return moves
