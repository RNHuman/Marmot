import pygame
import sys

pygame.init()

WINDOW_SIZE = (600, 600)
BOARD_SIZE = 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Chess pieces layout
chess_pieces = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],  # Rooks, Knights, Bishops, Queen, King
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Pawns
    ['', '', '', '', '', '', '', ''],           # Empty rows
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Pawns (black side)
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # Rooks, Knights, Bishops, Queen, King (black side)
]

# Create Window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Chess Board')

# Create font for chess pieces
font = pygame.font.SysFont(None, 72)

def draw_chessboard(screen, board_size):
    width, height = screen.get_size()
    square_size = min(width, height) // board_size

    for row in range(board_size):
        for col in range(board_size):
            # Determine square color
            is_white_square = (row + col) % 2 == 0
            color = WHITE if is_white_square else BLACK
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, rect)

            # Draw chess piece if present
            piece = chess_pieces[row][col]
            if piece:
                # Set font color based on square color
                font_color = BLACK if is_white_square else WHITE
                text_surface = font.render(piece, True, font_color)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw Chessboard
    screen.fill(WHITE)
    draw_chessboard(screen, BOARD_SIZE)

    pygame.display.flip()
