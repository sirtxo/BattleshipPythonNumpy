import numpy as np
import pygame
import sys

from pygame import font

WATER_SYMBOL = "%"

BOARD_HEIGHT = 600
MAX_CELLS = 10
BOARD_WIDTH = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


def alert(text2, screen, table):
    pygame.display.set_caption("Alert Window")
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render(text2, True, (255, 0, 0))  # Texto de la alerta
    text_rect = text.get_rect(center=(150, 100))  # Posición del texto en el centro de la ventana

    screen.blit(text, text_rect)  # Dibuja el texto en la ventana

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                initialize_window(table)


def draw_board(screen, table):
    # Define board dimensions
    cell_size = BOARD_WIDTH // MAX_CELLS

    # Draw grid lines
    for i in range(MAX_CELLS + 1):
        pygame.draw.line(screen, GRAY, (i * cell_size, 0), (i * cell_size, BOARD_HEIGHT))
        pygame.draw.line(screen, GRAY, (0, i * cell_size), (BOARD_HEIGHT, i * cell_size))

    # Display board contents
    font = pygame.font.Font(None, 12)
    for i in range(MAX_CELLS):
        for j in range(MAX_CELLS):
            text = font.render(table[i, j], True, BLACK)
            text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
            screen.blit(text, text_rect)


def main():
    pygame.init()
    table = np.full((MAX_CELLS, MAX_CELLS), WATER_SYMBOL)
    initialize_window(table)


def initialize_window(table):
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    screen.fill(WHITE)
    draw_board(screen, table)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    alert("Clic izquierdo en ({}, {})".format(event.pos[0] // (BOARD_WIDTH / MAX_CELLS),
                                                              event.pos[1] // (BOARD_HEIGHT / MAX_CELLS)),
                          screen, table)


if __name__ == "__main__":
    main()
