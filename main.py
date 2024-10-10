import pygame
import sys
import os  # Used for restarting the program

pygame.init()

# Colors
WINDOW_SIZE = (600, 700)  # Make the window larger to accommodate the buttons
BOARD_SIZE = 8
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
BUTTON_AREA_COLOR = (200, 200, 200)  # Light grey button area
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
FONT_COLOR = (255, 255, 255)

# Chess pieces layout
chess_pieces = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],  # Rooks, Knights, Bishops, Queen, King
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Pawns
    ['', '', '', '', '', '', '', ''],  # Empty rows
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Pawns (white side)
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']  # Rooks, Knights, Bishops, Queen, King (white side)
]

# Create Window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Chess Board')

# Create font for chess pieces and button text
font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 48)

# Board flipping flag
flip_board = False


# Button definitions
def draw_button(screen, button_rect, text, hover):
    # Change color when hovering over the button
    button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = button_font.render(text, True, FONT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)


def draw_buttons(screen):
    # Draw 3 buttons (Flip, Restart, Bot)
    button_flip = pygame.Rect(20, WINDOW_SIZE[1] - 80, 150, 50)
    button_restart = pygame.Rect(210, WINDOW_SIZE[1] - 80, 180, 50)
    button_bot = pygame.Rect(430, WINDOW_SIZE[1] - 80, 150, 50)

    mouse_pos = pygame.mouse.get_pos()

    # Flip Button
    hover = button_flip.collidepoint(mouse_pos)
    draw_button(screen, button_flip, "FLIP", hover)

    # Restart Button
    hover = button_restart.collidepoint(mouse_pos)
    draw_button(screen, button_restart, "RESTART", hover)

    # Bot Button
    hover = button_bot.collidepoint(mouse_pos)
    draw_button(screen, button_bot, "BOT", hover)

    return button_flip, button_restart, button_bot


def restart_program():
    """Restarts the current program."""
    pygame.quit()
    os.execl(sys.executable, sys.executable, *sys.argv)


def draw_chessboard(screen, board_size, flip):
    width, height = screen.get_size()
    board_height = height - 100  # Leave space for the buttons at the bottom
    square_size = min(width, board_height) // board_size

    for row in range(board_size):
        for col in range(board_size):
            # Determine if square is light or dark gray
            is_light_square = (row + col) % 2 == 0
            color = LIGHT_GRAY if is_light_square else DARK_GRAY
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, rect)

            # Flip board if necessary
            display_row = row if not flip else board_size - 1 - row
            display_col = col if not flip else board_size - 1 - col

            # Draw chess piece if present
            piece = chess_pieces[display_row][display_col]
            if piece:
                # Set piece color: black pieces for top two rows, white pieces for bottom two rows
                if display_row < 2:  # Black pieces at the top
                    font_color = BLACK
                else:  # White pieces at the bottom
                    font_color = WHITE
                text_surface = font.render(piece, True, font_color)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)


# Main loop
while True:
    mouse_pos = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_flip, button_restart, button_bot = draw_buttons(screen)
            if button_flip.collidepoint(mouse_pos):
                flip_board = not flip_board
            elif button_restart.collidepoint(mouse_pos):
                restart_program()
            elif button_bot.collidepoint(mouse_pos):
                print("Bot button pressed (no functionality yet)")

    # Draw Chessboard
    screen.fill(WHITE)
    draw_chessboard(screen, BOARD_SIZE, flip_board)

    # Draw button area
    pygame.draw.rect(screen, BUTTON_AREA_COLOR, (0, WINDOW_SIZE[1] - 100, WINDOW_SIZE[0], 100))

    # Draw Buttons
    draw_buttons(screen)

    pygame.display.flip()
