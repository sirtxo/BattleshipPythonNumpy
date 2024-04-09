import numpy as np
import pygame
import sys

BOARD_HEIGHT = 600
MAX_CELLS = 10
BOARD_WIDTH = 800

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


def draw_board(screen, tablero):
    # Define board dimensions
    cell_size = BOARD_WIDTH // MAX_CELLS

    # Draw grid lines
    for i in range(MAX_CELLS + 1):
        pygame.draw.line(screen, GRAY, (i * cell_size, 0), (i * cell_size, BOARD_HEIGHT))
        pygame.draw.line(screen, GRAY, (0, i * cell_size), (BOARD_HEIGHT, i * cell_size))

    # Display board contents
    font = pygame.font.Font(None, 36)
    for i in range(MAX_CELLS):
        for j in range(MAX_CELLS):
            text = font.render(tablero[i, j], True, BLACK)
            text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
            screen.blit(text, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, 600))
    pygame.display.set_caption("PSA Battleship")
    tablero = np.full((10, 10), "%")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_board(screen, tablero)
        pygame.display.flip()


if __name__ == "__main__":
    main()
