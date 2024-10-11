import pygame
import sys
import os

pygame.init()

# Colors
WINDOW_SIZE = (600, 700)
BOARD_SIZE = 8
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
BUTTON_AREA_COLOR = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
FONT_COLOR = (255, 255, 255)

# Chess pieces layout
chess_pieces = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Create Window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Chess Board')

# Create font for chess pieces and button text
font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 48)

# Board flipping flag
flip_board = False
dragging = False
dragging_piece = None
dragging_pos = None

# Button definitions
def draw_button(screen, button_rect, text, hover):
    button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = button_font.render(text, True, FONT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def draw_buttons(screen):
    button_flip = pygame.Rect(50, WINDOW_SIZE[1] - 80, 150, 50)
    button_restart = pygame.Rect(225, WINDOW_SIZE[1] - 80, 150, 50)
    button_bot = pygame.Rect(400, WINDOW_SIZE[1] - 80, 150, 50)

    mouse_pos = pygame.mouse.get_pos()

    hover = button_flip.collidepoint(mouse_pos)
    draw_button(screen, button_flip, "FLIP", hover)

    hover = button_restart.collidepoint(mouse_pos)
    draw_button(screen, button_restart, "NEW", hover)

    hover = button_bot.collidepoint(mouse_pos)
    draw_button(screen, button_bot, "BOT", hover)

    return button_flip, button_restart, button_bot

def restart_program():
    """Restarts the current program."""
    pygame.quit()
    os.execl(sys.executable, sys.executable, *sys.argv)

def get_square_under_mouse(pos, square_size):
    """Calculate the row and column of the square under the mouse pointer."""
    x, y = pos
    col = x // square_size
    row = y // square_size
    return row, col

def draw_chessboard(screen, board_size, flip):
    width, height = screen.get_size()
    board_height = height - 100
    square_size = min(width, board_height) // board_size

    for row in range(board_size):
        for col in range(board_size):
            is_light_square = (row + col) % 2 == 0
            color = LIGHT_GRAY if is_light_square else DARK_GRAY
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, rect)

            display_row = row if not flip else board_size - 1 - row
            display_col = col if not flip else board_size - 1 - col

            piece = chess_pieces[display_row][display_col]
            if piece and not (dragging and dragging_piece == (display_row, display_col)):
                font_color = BLACK if display_row < 2 else WHITE
                text_surface = font.render(piece, True, font_color)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    return square_size

def draw_dragging_piece(screen, piece, mouse_pos):
    """Draw the piece being dragged under the mouse cursor."""
    if piece:
        font_color = BLACK if piece.isupper() else WHITE
        text_surface = font.render(piece, True, font_color)
        text_rect = text_surface.get_rect(center=mouse_pos)
        screen.blit(text_surface, text_rect)

# Main loop
while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                button_flip, button_restart, button_bot = draw_buttons(screen)
                if button_flip.collidepoint(mouse_pos):
                    flip_board = not flip_board
                elif button_restart.collidepoint(mouse_pos):
                    restart_program()
                elif button_bot.collidepoint(mouse_pos):
                    print("Bot button pressed (no functionality yet)")

                else:
                    width, height = screen.get_size()
                    square_size = min(width, height - 100) // BOARD_SIZE
                    row, col = get_square_under_mouse(mouse_pos, square_size)
                    if row < BOARD_SIZE and col < BOARD_SIZE:
                        row = row if not flip_board else BOARD_SIZE - 1 - row
                        col = col if not flip_board else BOARD_SIZE - 1 - col
                        piece = chess_pieces[row][col]
                        if piece:
                            dragging = True
                            dragging_piece = (row, col)
                            dragging_pos = mouse_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging:  # Release left mouse button
                width, height = screen.get_size()
                square_size = min(width, height - 100) // BOARD_SIZE
                row, col = get_square_under_mouse(mouse_pos, square_size)
                if row < BOARD_SIZE and col < BOARD_SIZE:
                    row = row if not flip_board else BOARD_SIZE - 1 - row
                    col = col if not flip_board else BOARD_SIZE - 1 - col

                    # Move the piece to the new square
                    old_row, old_col = dragging_piece
                    chess_pieces[row][col] = chess_pieces[old_row][old_col]
                    chess_pieces[old_row][old_col] = ''
                dragging = False
                dragging_piece = None
                dragging_pos = None

    # Draw Chessboard
    screen.fill(WHITE)
    square_size = draw_chessboard(screen, BOARD_SIZE, flip_board)

    # Draw button area
    pygame.draw.rect(screen, BUTTON_AREA_COLOR, (0, WINDOW_SIZE[1] - 100, WINDOW_SIZE[0], 100))

    # Draw Buttons
    draw_buttons(screen)

    # Draw the piece being dragged (if any)
    if dragging and dragging_piece:
        piece = chess_pieces[dragging_piece[0]][dragging_piece[1]]
        draw_dragging_piece(screen, piece, mouse_pos)

    pygame.display.flip()