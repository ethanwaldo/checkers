# config.py
# Constants and Configuration

SQUARE_SIZE = 80
BOARD_DIMENSION = 8
WINDOW_SIZE = SQUARE_SIZE * BOARD_DIMENSION
UI_HEIGHT = 180
PIECE_RADIUS = SQUARE_SIZE // 2 - 5

# --- Colors ---
COLOR_LIGHT_SQUARE = (240, 217, 181)
COLOR_DARK_SQUARE = (181, 136, 99)
COLOR_HIGHLIGHT = (255, 255, 0, 128)
COLOR_LEGAL_MOVE = (0, 255, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BUTTON = (200, 200, 200)
COLOR_BUTTON_HOVER = (150, 150, 150)

# --- UI Layout ---
# All UI elements are positioned relative to a starting point and a line height.
UI_FONT_SIZE = 24
UI_START_Y = WINDOW_SIZE + 15
UI_LINE_HEIGHT = 20

# Calculated Y-positions for each UI row
CAPTURED_ROW_Y = UI_START_Y
LAST_MOVE_ROW_Y = CAPTURED_ROW_Y + UI_LINE_HEIGHT * 2
TIMER_ROW_Y = LAST_MOVE_ROW_Y + UI_LINE_HEIGHT
STATUS_ROW_Y = TIMER_ROW_Y + UI_LINE_HEIGHT
BUTTON_ROW_Y = STATUS_ROW_Y + UI_LINE_HEIGHT + 5

# Button dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTONS = [{
    'name': 'New Game',
    'x': 10
}, {
    'name': 'Resign',
    'x': 120
}, {
    'name': 'Offer Draw',
    'x': 230
}, {
    'name': 'Undo',
    'x': 340
}]