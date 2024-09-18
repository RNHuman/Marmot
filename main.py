import pygame
import sys

pygame.init()

WINDOW_SIZE = (600, 700)  # Make the window larger to accommodate the button
BOARD_SIZE = 8
LIGHT_BROWN = (205, 133, 63)
DARK_BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
FONT_COLOR = (255, 255, 255)

# Chess pieces layout
chess_pieces = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],  # Rooks, Knights, Bishops, Queen, King
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Pawns
    ['', '', '', '', '', '', '', ''],           # Empty rows
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Pawns (white side)
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # Rooks, Knights, Bishops, Queen, King (white side)
]

# Create Window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Chess Board')

# Create font for chess pieces and button text
font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 48)

# Board flipping flag
flip_board = False

def draw_chessboard(screen, board_size, flip):
    width, height = screen.get_size()
    board_height = height - 100  # Leave space for the button at the bottom
    square_size = min(width, board_height) // board_size

    for row in range(board_size):
        for col in range(board_size):
            # Determine if square is light or dark brown
            is_light_brown = (row + col) % 2 == 0
            color = LIGHT_BROWN if is_light_brown else DARK_BROWN
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

def draw_button(screen, button_rect, hover):
    # Change color when hovering over the button
    button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = button_font.render("Flip Board", True, FONT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

# Main loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(200, WINDOW_SIZE[1] - 80, 200, 50)  # Button dimensions

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos):
                # Flip the board when the button is clicked
                flip_board = not flip_board

    # Draw Chessboard
    screen.fill(WHITE)
    draw_chessboard(screen, BOARD_SIZE, flip_board)

    # Draw Button
    hover = button_rect.collidepoint(mouse_pos)
    draw_button(screen, button_rect, hover)

    pygame.display.flip()
