import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WINDOW_SIZE = (600, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)

# Set up the display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Basic 2-Player Chess")

# Chessboard setup
BOARD_SIZE = 8
square_size = WINDOW_SIZE[0] // BOARD_SIZE
font = pygame.font.SysFont(None, 72)

# Chess pieces
chess_pieces = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Keeps track of the turn: True for White, False for Black
white_turn = True


# Functions for drawing
def draw_chessboard():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_GRAY if (row + col) % 2 == 0 else DARK_GRAY
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

            # Draw pieces
            piece = chess_pieces[row][col]
            if piece:
                color = WHITE if piece.isupper() else BLACK
                text_surface = font.render(piece.upper(), True, color)
                text_rect = text_surface.get_rect(
                    center=(col * square_size + square_size // 2, row * square_size + square_size // 2))
                screen.blit(text_surface, text_rect)


# Helper function to get square coordinates
def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    return y // square_size, x // square_size


# Main game loop
dragging = False
start_pos = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_under_mouse()
            piece = chess_pieces[row][col]
            if (white_turn and piece.isupper()) or (not white_turn and piece.islower()):
                start_pos = (row, col)
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                end_row, end_col = get_square_under_mouse()
                start_row, start_col = start_pos
                piece = chess_pieces[start_row][start_col]

                # Move the piece if it's a different square
                if (start_row, start_col) != (end_row, end_col):
                    chess_pieces[end_row][end_col] = piece
                    chess_pieces[start_row][start_col] = ''
                    white_turn = not white_turn  # Switch turns

                # Reset dragging
                dragging = False

    # Draw everything
    screen.fill(WHITE)
    draw_chessboard()
    pygame.display.flip()
