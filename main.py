import pygame
import sys

pygame.init()

WINDOW_SIZE = (600, 600)
BOARD_SIZE = 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create Window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Chess Board')


def draw_chessboard(screen, board_size):
    width, height = screen.get_size()
    square_size = min(width, height) // board_size

    for row in range(board_size):
        for col in range(board_size):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, rect)


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
