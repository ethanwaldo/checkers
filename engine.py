# engine.py
# Checkers game logic and state management

import time
from config import BOARD_DIMENSION
from pieces import Man, King


class Player:
    """Represents a checkers player."""

    def __init__(self, name, is_player1):
        self.name = name
        self.is_player1 = is_player1
        self.color = 'red' if is_player1 else 'black'


class Move:
    """Represents a single checkers move, including its duration and capture info."""

    def __init__(self,
                 piece_moved,
                 start_coords,
                 end_coords,
                 piece_captured=None,
                 is_promotion=False,
                 promoted_piece=None,
                 turn_duration=0.0,
                 captured_coords=None):
        self.piece_moved = piece_moved
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.piece_captured = piece_captured
        self.is_promotion = is_promotion
        self.promoted_piece = promoted_piece
        self.turn_duration = turn_duration
        self.captured_coords = captured_coords or end_coords  # For regular captures
        
    def is_jump(self):
        """Check if this move is a jump (capture)."""
        return abs(self.start_coords[0] - self.end_coords[0]) == 2

    def to_notation(self):
        """Generates simple notation for the move."""
        start = f"{chr(ord('a') + self.start_coords[1])}{8 - self.start_coords[0]}"
        end = f"{chr(ord('a') + self.end_coords[1])}{8 - self.end_coords[0]}"
        symbol = 'x' if self.piece_captured else '-'
        notation = f"{start}{symbol}{end}"
        if self.is_promotion:
            notation += "=K"
        return notation


class Game:
    """The main game engine that manages checkers logic and state."""

    def __init__(self):
        self.board = [[None for _ in range(BOARD_DIMENSION)]
                      for _ in range(BOARD_DIMENSION)]
        self.players = [Player("Red", True), Player("Black", False)]
        self.current_player_index = 0
        self.game_state = 'active'
        self.move_history = []
        self.red_captured = []
        self.black_captured = []
        self.turn_start_time = time.time()
        self.red_turn_time = 0
        self.black_turn_time = 0
        self.position_history = {}
        self._place_pieces()
        self._update_position_history()

    def make_move(self, start_coords, end_coords):
        """Executes a move, assuming it has been pre-validated by the GUI."""
        piece_to_move = self.get_piece_at(start_coords)

        if not piece_to_move or piece_to_move.is_player1 != self.get_current_player().is_player1:
            return False

        elapsed_time = time.time() - self.turn_start_time
        move_details = self._execute_board_move(start_coords, end_coords, elapsed_time)
        self._update_game_after_move(move_details)
        return True

    def undo_last_move(self):
        """Undo the last move made."""
        if not self.move_history: 
            return
        move = self.move_history.pop()

        # Restore the piece to its original position
        self.set_piece_at(move.start_coords, move.piece_moved)
        
        # If it was a promotion, demote back to Man
        if move.is_promotion:
            self.set_piece_at(move.start_coords, Man(move.piece_moved.is_player1))
            self.set_piece_at(move.end_coords, None)
        else:
            self.set_piece_at(move.end_coords, None)

        # If there was a capture, restore the captured piece
        if move.piece_captured:
            # For jumps, the captured piece was in the middle
            if move.is_jump():
                captured_row = (move.start_coords[0] + move.end_coords[0]) // 2
                captured_col = (move.start_coords[1] + move.end_coords[1]) // 2
                self.set_piece_at((captured_row, captured_col), move.piece_captured)
            
            # Remove from captured pieces list
            if move.piece_moved.is_player1: 
                self.black_captured.pop()
            else: 
                self.red_captured.pop()

        # Restore time
        if move.piece_moved.is_player1:
            self.red_turn_time -= move.turn_duration
        else:
            self.black_turn_time -= move.turn_duration

        self.current_player_index = 1 - self.current_player_index
        self.turn_start_time = time.time()
        self._update_game_status()

    def get_legal_moves_for_piece(self, coords):
        """Get all legal moves for a piece at the given coordinates."""
        piece = self.get_piece_at(coords)
        if not piece or piece.is_player1 != self.get_current_player().is_player1:
            return []

        # In checkers, if a jump is available, it must be taken
        all_jumps = self._get_all_jumps_for_player(self.get_current_player())
        
        if all_jumps:
            piece_jumps = [move for move in all_jumps if move[0] == coords]
            return [move[1] for move in piece_jumps]  # Return only jump destinations
        else:
            # No jumps available, return regular moves
            return piece.get_moves(self.board, coords, self.move_history)

    def get_piece_at(self, coords):
        """Get the piece at the given coordinates."""
        return self.board[coords[0]][coords[1]]

    def set_piece_at(self, coords, piece):
        """Set a piece at the given coordinates."""
        self.board[coords[0]][coords[1]] = piece

    def get_current_player(self):
        """Get the current player."""
        return self.players[self.current_player_index]

    def resign(self):
        """Current player resigns."""
        winner = "Black" if self.current_player_index == 0 else "Red"
        self.game_state = f'resignation - {winner} wins'

    def offer_draw(self):
        """Offer a draw."""
        self.game_state = 'draw by agreement'

    def to_pdn(self):
        """Generates a FEN string for the current board state using PDN standard."""
        turn = 'R' if self.get_current_player().is_player1 else 'B'
        
        red_pieces = []
        black_pieces = []

        for r in range(BOARD_DIMENSION):
            for c in range(BOARD_DIMENSION):
                if (r + c) % 2 == 1: # Only playable squares
                    square_num = (r * 4) + (c // 2) + 1
                    piece = self.get_piece_at((r, c))
                    if piece:
                        piece_str = str(square_num)
                        if isinstance(piece, King):
                            piece_str = "K" + piece_str
                        
                        if piece.is_player1:
                            red_pieces.append(piece_str)
                        else:
                            black_pieces.append(piece_str)

        return f"[{turn}:{','.join(red_pieces)}:{','.join(black_pieces)}]"

    # --- Helper Methods (reused and adapted from chess) ---
    def _place_pieces(self):
        """Place initial checkers pieces on the board."""
        # Place black pieces (top of board)
        for row in range(3):
            for col in range(BOARD_DIMENSION):
                if (row + col) % 2 == 1:  # Only on dark squares
                    self.board[row][col] = Man(False)
        
        # Place red pieces (bottom of board)  
        for row in range(5, 8):
            for col in range(BOARD_DIMENSION):
                if (row + col) % 2 == 1:  # Only on dark squares
                    self.board[row][col] = Man(True)

    def _execute_board_move(self, start_coords, end_coords, elapsed_time):
        """Execute the actual board move and return move details."""
        piece = self.get_piece_at(start_coords)
        captured_piece = None
        captured_coords = None
        
        # Check if this is a jump (capture)
        if abs(start_coords[0] - end_coords[0]) == 2:
            # This is a jump - capture the piece in between
            captured_row = (start_coords[0] + end_coords[0]) // 2
            captured_col = (start_coords[1] + end_coords[1]) // 2
            captured_coords = (captured_row, captured_col)
            captured_piece = self.get_piece_at(captured_coords)
            self.set_piece_at(captured_coords, None)

        # Handle captured pieces
        if captured_piece:
            if piece.is_player1: 
                self.black_captured.append(captured_piece)
            else: 
                self.red_captured.append(captured_piece)

        # Check for promotion
        promoted_piece = None
        is_promotion = False
        if isinstance(piece, Man):
            # Red pieces promote when reaching row 0, black pieces when reaching row 7
            if (piece.is_player1 and end_coords[0] == 0) or (not piece.is_player1 and end_coords[0] == 7):
                is_promotion = True
                promoted_piece = King(piece.is_player1)
                self.set_piece_at(end_coords, promoted_piece)
            else:
                self.set_piece_at(end_coords, piece)
        else:
            self.set_piece_at(end_coords, piece)

        self.set_piece_at(start_coords, None)
        
        return Move(piece, start_coords, end_coords, captured_piece,
                   is_promotion, promoted_piece, elapsed_time, captured_coords)

    def _update_game_after_move(self, move):
        """Update game state after a move (reused from chess)."""
        self.move_history.append(move)
        if self.current_player_index == 0:
            self.red_turn_time += move.turn_duration
        else:
            self.black_turn_time += move.turn_duration
        self.turn_start_time = time.time()
        self.current_player_index = 1 - self.current_player_index
        self._update_position_history()
        self._update_game_status()

    def _update_game_status(self):
        """Update the current game status."""
        # Check for threefold repetition (reused logic)
        if self.position_history.get(self._get_position_hash(), 0) >= 3:
            self.game_state = 'draw by threefold repetition'
            return

        player = self.get_current_player()
        
        # Check if opponent has any pieces left
        opponent_pieces = 0
        for r, c in self._iterate_squares():
            piece = self.get_piece_at((r, c))
            if piece and piece.is_player1 != player.is_player1:
                opponent_pieces += 1
        
        if opponent_pieces == 0:
            self.game_state = f'{player.color.title()} wins - All opponent pieces captured'
            return

        # Check if player has any legal moves
        has_legal_move = False
        for r, c in self._iterate_squares():
            piece = self.get_piece_at((r, c))
            if piece and piece.is_player1 == player.is_player1:
                if self.get_legal_moves_for_piece((r, c)):
                    has_legal_move = True
                    break

        if not has_legal_move:
            winner = "Black" if player.is_player1 else "Red"
            self.game_state = f'{winner} wins - no legal moves'
        else:
            self.game_state = 'active'

    def _get_all_jumps_for_player(self, player):
        """Get all possible jumps for a player."""
        jumps = []
        for r, c in self._iterate_squares():
            piece = self.get_piece_at((r, c))
            if piece and piece.is_player1 == player.is_player1:
                piece_moves = piece.get_moves(self.board, (r, c), self.move_history)
                for move_coords in piece_moves:
                    if abs(r - move_coords[0]) == 2:  # This is a jump
                        jumps.append(((r, c), move_coords))
        return jumps

    def _get_position_hash(self):
        """Generate a hash for the current position (reused from chess)."""
        board_str = "".join(p.name + p.color[0] if p else ' ' 
                           for r in self.board for p in r)
        return board_str + str(self.current_player_index)

    def _update_position_history(self):
        """Update position history for repetition detection (reused from chess)."""
        pos_hash = self._get_position_hash()
        self.position_history[pos_hash] = self.position_history.get(pos_hash, 0) + 1

    def _iterate_squares(self):
        """Iterator for all board squares (reused from chess)."""
        for r in range(BOARD_DIMENSION):
            for c in range(BOARD_DIMENSION):
                yield r, c