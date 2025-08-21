# gui.py
# Graphical user interface using Pygame

import pygame
import sys
import time
import threading
from config import *
from engine import Game, King
from ai import AIPlayer

class CheckersGUI:
    """Manages the graphical user interface using Pygame."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + UI_HEIGHT))
        pygame.display.set_caption("Checkers Game")
        self.font = pygame.font.Font(None, 64)
        self.ui_font = pygame.font.Font(None, UI_FONT_SIZE)
        self.game = Game()
        
        self.selected_square = None
        self.legal_moves = []
        self.hovered_button = None
        
        # --- Player Configuration ---
        self.white_player_type = "human"
        self.black_player_type = "human"

        # --- Create player objects based on the types selected ---
        self.white_player = self._create_player(self.white_player_type)
        self.black_player = self._create_player(self.black_player_type)
        
        self.ai_is_thinking = False
        self.ai_move_result = None
        self.ai_lock = threading.Lock()

    def _create_player(self, player_type):
        """Helper function to create and return an AI player object."""
        if player_type == "gemini":
            return AIPlayer()
        return None # Player is human

    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        while True:
            self._handle_ai_turn_start()
            self._process_ai_result()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                is_human_turn = (self.game.get_current_player().color == 'red' and self.white_player is None) or \
                                (self.game.get_current_player().color == 'black' and self.black_player is None)

                if not self.ai_is_thinking and is_human_turn:
                    self.handle_input(event)

            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def _handle_ai_turn_start(self):
        """Checks if the current player is an AI and starts its thinking process."""
        current_player_object = self.white_player if self.game.get_current_player().color == 'red' else self.black_player
        
        is_ai_turn = (current_player_object is not None and 
                      not self.ai_is_thinking and 
                      self.game.game_state == 'active')

        if is_ai_turn:
            self.ai_is_thinking = True
            thread = threading.Thread(target=self._get_ai_move_threaded, args=(current_player_object,))
            thread.start()

    def _get_ai_move_threaded(self, ai_player):
        """This function runs in a separate thread to get the AI's move."""
        pdn = self.game.to_pdn()
        move = ai_player.get_best_move(pdn)
        with self.ai_lock:
            self.ai_move_result = move

    def _process_ai_result(self):
        """Checks if the AI thread has finished and, if so, processes the resulting move."""
        move_to_make = None
        with self.ai_lock:
            if self.ai_move_result is not None:
                move_to_make = self.ai_move_result
                self.ai_move_result = None
        
        if move_to_make:
            start_coords, end_coords = self._parse_ai_move(move_to_make)
            if start_coords and end_coords:
                if end_coords in self.game.get_legal_moves_for_piece(start_coords):
                    self.game.make_move(start_coords, end_coords)
                else:
                    print(f"ERROR: AI suggested an illegal move: {move_to_make}")
            else:
                print(f"ERROR: AI response '{move_to_make}' could not be parsed.")
            
            self.ai_is_thinking = False

    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION: self.hovered_button = self._get_button_at(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            button = self._get_button_at(pos)
            if button: self.handle_button_click(button['name'])
            else: self.handle_square_click(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u: self._undo_move()
            if event.key == pygame.K_r: self._reset_game_state()

    def handle_square_click(self, pos):
        coords = (pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE)
        if coords[0] >= BOARD_DIMENSION: return
        if self.selected_square:
            if coords in self.legal_moves:
                self.game.make_move(self.selected_square, coords)
            self._reset_ui_state()
        else:
            piece = self.game.get_piece_at(coords)
            if piece and piece.is_player1 == self.game.get_current_player().is_player1:
                self.selected_square = coords
                self.legal_moves = self.game.get_legal_moves_for_piece(coords)
            else:
                self._reset_ui_state()

    def handle_button_click(self, button_name):
        if button_name == 'New Game': self._reset_game_state()
        elif button_name == 'Resign': self.game.resign()
        elif button_name == 'Offer Draw': self.game.offer_draw()
        elif button_name == 'Undo': self._undo_move()

    def draw(self):
        self.screen.fill(COLOR_WHITE)
        self.draw_board(); self.draw_highlights(); self.draw_pieces(); self.draw_ui()

    def draw_board(self):
        for r in range(BOARD_DIMENSION):
            for c in range(BOARD_DIMENSION):
                color = COLOR_LIGHT_SQUARE if (r + c) % 2 == 0 else COLOR_DARK_SQUARE
                pygame.draw.rect(self.screen, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_highlights(self):
        if not self.selected_square: return
        r, c = self.selected_square
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(COLOR_HIGHLIGHT); self.screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
        s.fill(COLOR_LEGAL_MOVE)
        for r_m, c_m in self.legal_moves: self.screen.blit(s, (c_m * SQUARE_SIZE, r_m * SQUARE_SIZE))

    def draw_pieces(self):
        for r in range(BOARD_DIMENSION):
            for c in range(BOARD_DIMENSION):
                piece = self.game.board[r][c]
                if piece:
                    # Draw the piece as a circle
                    color = COLOR_RED if piece.is_player1 else COLOR_BLACK
                    pygame.draw.circle(self.screen, color, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2), PIECE_RADIUS)
                    # Draw a crown for kings
                    if isinstance(piece, King):
                        crown_surf = self.ui_font.render('K', True, COLOR_WHITE)
                        crown_rect = crown_surf.get_rect(center=(c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2))
                        self.screen.blit(crown_surf, crown_rect)

    def draw_ui(self):
        red_cap_str = f"Red captured: {len(self.game.black_captured)}"
        black_cap_str = f"Black captured: {len(self.game.red_captured)}"
        self.screen.blit(self.ui_font.render(red_cap_str, True, COLOR_BLACK), (10, CAPTURED_ROW_Y))
        self.screen.blit(self.ui_font.render(black_cap_str, True, COLOR_BLACK), (10, CAPTURED_ROW_Y + UI_LINE_HEIGHT))
        last_move_str = f"Last Move: {self.game.move_history[-1].to_notation()}" if self.game.move_history else "Last Move: None"
        self.screen.blit(self.ui_font.render(last_move_str, True, COLOR_BLACK), (10, LAST_MOVE_ROW_Y))
        red_time, black_time = self._get_display_times()
        self.screen.blit(self.ui_font.render(f"Red: {red_time}", True, COLOR_BLACK), (10, TIMER_ROW_Y))
        self.screen.blit(self.ui_font.render(f"Black: {black_time}", True, COLOR_BLACK), (200, TIMER_ROW_Y))
        player_color = self.game.get_current_player().color.title()
        status_text = f"{player_color}'s Turn | {self.game.game_state.title()}"
        if self.ai_is_thinking: 
            current_ai_type = self.white_player_type if self.game.get_current_player().color == 'red' else self.black_player_type
            status_text = f"{current_ai_type.title()} is thinking..."
        self.screen.blit(self.ui_font.render(status_text, True, COLOR_BLACK), (10, STATUS_ROW_Y))
        for button in BUTTONS:
            rect = pygame.Rect(button['x'], BUTTON_ROW_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
            color = COLOR_BUTTON_HOVER if self.hovered_button == button['name'] else COLOR_BUTTON
            pygame.draw.rect(self.screen, color, rect)
            text_surf = self.ui_font.render(button['name'], True, COLOR_BLACK)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _parse_ai_move(self, move_str):
        try:
            start_sq, end_sq = map(int, move_str.split('-'))
            start_coords = self._square_to_coords(start_sq)
            end_coords = self._square_to_coords(end_sq)
            return (start_coords, end_coords)
        except (ValueError, IndexError): pass
        print(f"ERROR: Could not parse AI move string: '{move_str}'")
        return None, None

    def _square_to_coords(self, square):
        row = (square - 1) // 4
        col = ((square - 1) % 4) * 2 + (1 - row % 2)
        return row, col

    def _get_button_at(self, pos):
        for button in BUTTONS:
            rect = pygame.Rect(button['x'], BUTTON_ROW_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
            if rect.collidepoint(pos): return button
        return None

    def _get_display_times(self):
        r_time = self.game.red_turn_time; b_time = self.game.black_turn_time
        elapsed = time.time() - self.game.turn_start_time
        if self.game.get_current_player().is_player1: r_time += elapsed
        else: b_time += elapsed
        format_time = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"
        return format_time(r_time), format_time(b_time)

    def _reset_ui_state(self): self.selected_square = None; self.legal_moves = []
    def _reset_game_state(self): self.game = Game(); self._reset_ui_state()
    def _undo_move(self):
        is_h_vs_ai = (self.white_player is None and self.black_player is not None) or \
                     (self.white_player is not None and self.black_player is None)
        
        self.game.undo_last_move()
        if is_h_vs_ai:
            self.game.undo_last_move()
        self._reset_ui_state()
