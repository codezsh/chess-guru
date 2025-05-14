class BoardRepresentor:
    def __init__(self):
        self.board_1d = [
            'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',  # Black pieces
            'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',  # Black pawns
            '.', '.', '.', '.', '.', '.', '.', '.',  # Empty squares
            '.', '.', '.', '.', '.', '.', '.', '.',  # Empty squares
            '.', '.', '.', '.', '.', '.', '.', '.',  # Empty squares
            '.', '.', '.', '.', '.', '.', '.', '.',  # Empty squares
            'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',  # White pawns
            'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'   # White pieces
        ]
        
        # Initialize the bitboard representation
        self.bitboards = {
            'w_pawns': 0x000000000000FF00,  # White pawns (on ranks 2-3)
            'b_pawns': 0x00FF000000000000,  # Black pawns (on ranks 7-8)
            'w_knights': 0x0000000000000042, # White knights
            'b_knights': 0x4200000000000000, # Black knights
            'w_bishops': 0x0000000000000024, # White bishops
            'b_bishops': 0x2400000000000000, # Black bishops
            'w_rooks': 0x0000000000000081,   # White rooks
            'b_rooks': 0x8100000000000000,   # Black rooks
            'w_queens': 0x0000000000000008,  # White queens
            'b_queens': 0x0800000000000000,  # Black queens
            'w_king': 0x0000000000000010,    # White king
            'b_king': 0x1000000000000000     # Black king
        }

    def update_bitboards_from_1d(self):
        """Convert the 1D array representation to bitboards."""
        self.bitboards = { 
            'w_pawns': 0,
            'b_pawns': 0,
            'w_knights': 0,
            'b_knights': 0,
            'w_bishops': 0,
            'b_bishops': 0,
            'w_rooks': 0,
            'b_rooks': 0,
            'w_queens': 0,
            'b_queens': 0,
            'w_king': 0,
            'b_king': 0
        }
        
        for idx, piece in enumerate(self.board_1d):
            bit_index = 63 - idx  # 63 -> 0 (bitboard from left to right, starting from the top)
            if piece == 'p':  # Black pawn
                self.bitboards['b_pawns'] |= (1 << bit_index)
            elif piece == 'P':  # White pawn
                self.bitboards['w_pawns'] |= (1 << bit_index)
            elif piece == 'n':  # Black knight
                self.bitboards['b_knights'] |= (1 << bit_index)
            elif piece == 'N':  # White knight
                self.bitboards['w_knights'] |= (1 << bit_index)
            elif piece == 'b':  # Black bishop
                self.bitboards['b_bishops'] |= (1 << bit_index)
            elif piece == 'B':  # White bishop
                self.bitboards['w_bishops'] |= (1 << bit_index)
            elif piece == 'r':  # Black rook
                self.bitboards['b_rooks'] |= (1 << bit_index)
            elif piece == 'R':  # White rook
                self.bitboards['w_rooks'] |= (1 << bit_index)
            elif piece == 'q':  # Black queen
                self.bitboards['b_queens'] |= (1 << bit_index)
            elif piece == 'Q':  # White queen
                self.bitboards['w_queens'] |= (1 << bit_index)
            elif piece == 'k':  # Black king
                self.bitboards['b_king'] |= (1 << bit_index)
            elif piece == 'K':  # White king
                self.bitboards['w_king'] |= (1 << bit_index)

    def update_1d_from_bitboards(self):
        """Convert bitboards to the 1D array representation."""
        self.board_1d = ['.' for _ in range(64)]  # Initialize empty board
        
        for piece, bitboard in self.bitboards.items():
            for i in range(64):
                if (bitboard >> (63 - i)) & 1:
                    # Determine the piece and set the board array
                    if piece == 'w_pawns':
                        self.board_1d[i] = 'P'
                    elif piece == 'b_pawns':
                        self.board_1d[i] = 'p'
                    elif piece == 'w_knights':
                        self.board_1d[i] = 'N'
                    elif piece == 'b_knights':
                        self.board_1d[i] = 'n'
                    elif piece == 'w_bishops':
                        self.board_1d[i] = 'B'
                    elif piece == 'b_bishops':
                        self.board_1d[i] = 'b'
                    elif piece == 'w_rooks':
                        self.board_1d[i] = 'R'
                    elif piece == 'b_rooks':
                        self.board_1d[i] = 'r'
                    elif piece == 'w_queens':
                        self.board_1d[i] = 'Q'
                    elif piece == 'b_queens':
                        self.board_1d[i] = 'q'
                    elif piece == 'w_king':
                        self.board_1d[i] = 'K'
                    elif piece == 'b_king':
                        self.board_1d[i] = 'k'

    def display_1d(self):
        """Display the 1D array as an 8x8 board for the UI."""
        for i in range(8):
            print(" ".join(self.board_1d[i*8:(i+1)*8]))
        print()

    def display_bitboards(self):
        """Display the bitboards for debugging or AI evaluation."""
        for piece, bitboard in self.bitboards.items():
            print(f"{piece}: {bin(bitboard)}")
