# pieces.py
# Checkers piece classes

from config import BOARD_DIMENSION


class Piece:
    """Base class for all checkers pieces."""

    def __init__(self, name, is_player1):
        self.name = name
        self.is_player1 = is_player1
        self.color = 'red' if is_player1 else 'black'

    def get_moves(self, board, start_coords, move_history=None):
        """Base method to be overridden by subclasses."""
        return []

    def is_enemy(self, other_piece):
        """Check if another piece is an enemy."""
        return other_piece is not None and other_piece.is_player1 != self.is_player1

    def _get_diagonal_moves(self, board, start_coords, directions):
        """Helper method to get moves for diagonal movement."""
        moves = []
        row, col = start_coords
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check for a regular move
            if 0 <= new_row < BOARD_DIMENSION and 0 <= new_col < BOARD_DIMENSION:
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                # Check for a capture
                elif self.is_enemy(target):
                    jump_row, jump_col = new_row + dr, new_col + dc
                    if (0 <= jump_row < BOARD_DIMENSION and 0 <= jump_col < BOARD_DIMENSION 
                        and board[jump_row][jump_col] is None):
                        moves.append((jump_row, jump_col))
        return moves


class Man(Piece):
    """Regular checkers piece that moves diagonally forward only."""

    def __init__(self, is_player1):
        super().__init__('M', is_player1)

    def get_moves(self, board, start_coords, move_history=None):
        # Player1 (red) moves up the board (decreasing row numbers)
        # Player2 (black) moves down the board (increasing row numbers)
        if self.is_player1:
            directions = [(-1, -1), (-1, 1)]  # Forward diagonals for player1
        else:
            directions = [(1, -1), (1, 1)]   # Forward diagonals for player2
        
        return self._get_diagonal_moves(board, start_coords, directions)


class King(Piece):
    """King checkers piece that can move diagonally in all directions."""

    def __init__(self, is_player1):
        super().__init__('K', is_player1)

    def get_moves(self, board, start_coords, move_history=None):
        # Kings can move in all diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._get_diagonal_moves(board, start_coords, directions)