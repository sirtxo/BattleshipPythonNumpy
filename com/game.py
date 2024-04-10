import numpy as np
import pygame
import sys
import random

from pygame import font

WATER_SYMBOL = " "

BOARD_HEIGHT = 600
MAX_CELLS = 10
BOARD_WIDTH = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (25, 25, 25)

# status = [["Start", 0, 0, 0], ["Place_Ship", 4, 1, 4], ["Place_Ship", 3, 2, 3], ["Place_Ship", 2, 3, 2], ["Place_Ship", 1, 4, 1], ["System_ships", 1, 4], ["End_Game"]]
status = [["Start", 0, 0, 0], ["Place_Ship", 1, 1, 1], ["System_ships", 1, 4], ["End_Game"]]
game_position = 0


def alert(text2, screen, player_table, system_table, game_position=None):
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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if status[game_position][0] == "Start":
                        game_position += 1
                        screen.fill(WHITE)
                        show_window(player_table, system_table, screen, game_position)


def draw_board(screen, player_table, system_table):
    cell_size = BOARD_WIDTH // MAX_CELLS
    font = pygame.font.Font(None, 12)
    for i in range(MAX_CELLS):
        for j in range(MAX_CELLS):
            text = font.render(player_table[i, j], True, BLACK)
            text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
            screen.blit(text, text_rect)

    # Draw grid lines for player's board
    for i in range(MAX_CELLS + 1):
        pygame.draw.line(screen, GRAY, (i * cell_size, 0), (i * cell_size, BOARD_HEIGHT))
        pygame.draw.line(screen, GRAY, (0, i * cell_size), (BOARD_HEIGHT, i * cell_size))

    # Display system's board contents
    for i in range(MAX_CELLS):
        for j in range(MAX_CELLS):
            text = font.render(system_table[i, j], True, GREEN)
            text_rect = text.get_rect(center=(j * cell_size + cell_size // 2 + BOARD_WIDTH,
                                              i * cell_size + cell_size // 2))
            screen.blit(text, text_rect)

    # Draw grid lines for system's board
    for i in range(MAX_CELLS + 1):
        pygame.draw.line(screen, GRAY, (i * cell_size + BOARD_WIDTH, 0),
                         (i * cell_size + BOARD_WIDTH, BOARD_HEIGHT))
        pygame.draw.line(screen, GRAY, (0, i * cell_size + BOARD_WIDTH),
                         (BOARD_HEIGHT, i * cell_size + BOARD_WIDTH))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH * 2, BOARD_HEIGHT))
    screen.fill(WHITE)
    player_table = np.full((MAX_CELLS, MAX_CELLS), WATER_SYMBOL)
    system_table = np.full((MAX_CELLS, MAX_CELLS), "-")
    if status[game_position][0] == "Start":
        alert("Iniciando juego", screen, player_table, system_table, game_position)


def show_window(player_table, system_table, screen, game_position):
    draw_board(screen, player_table, system_table)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = (
                    int(event.pos[1] // (BOARD_HEIGHT / MAX_CELLS)), int(event.pos[0] // (BOARD_WIDTH / MAX_CELLS)))
                    if status[game_position][0] == "Place_Ship":
                        if status[game_position][1] >= 0:
                            player_table[pos] = "x"
                            draw_window(game_position, player_table, system_table)
                            status[game_position][1] = status[game_position][1] - 1
                            if status[game_position][1] == 0:
                                status[game_position][2] = status[game_position][2] - 1
                                if status[game_position][2] > 0:
                                    status[game_position][1] = status[game_position][3]
                                else:
                                    game_position = game_position + 1
                    if status[game_position][0] == "System_ships":
                        system_ships = [["Place_Ship", 4, 1, 4], ["Place_Ship", 3, 2, 3], ["Place_Ship", 2, 3, 2],
                                        ["Place_Ship", 1, 4, 1]]
                        for sublist in system_ships:
                            for i in range(sublist[2]):
                                for tuple_sys in generate_ship_positions(10, sublist[1], system_table):
                                    system_table[tuple_sys] = "0"

                            draw_window(game_position, player_table, system_table)


def generate_ship_positions(board_size, ship_size, system_table):
    valid_position = False
    while not valid_position:
        # Decide si el barco estará horizontal o vertical
        horizontal = random.choice([True, False])
        if horizontal:
            row = random.randint(0, board_size - 1)
            col = random.randint(0, board_size - ship_size)
            positions = [(row, col + i) for i in range(ship_size)]
        else:
            row = random.randint(0, board_size - ship_size)
            col = random.randint(0, board_size - 1)
            positions = [(row + i, col) for i in range(ship_size)]

        if check_balid_position(positions, system_table):
            return positions
        else:
            return generate_ship_positions(board_size, ship_size, system_table)



def check_balid_position(positions, table):
    valid_position = True
    for r, c in positions:
        if table[r][c] == '0':
            try:
                if (table[r][c + 1] == '0' or table[r + 1][c] == '0' \
                        or table[r + 1][c + 1] != '0' or table[r][c - 1] != '0' or
                        table[r - 1][c] == '0' \
                        or table[r - 1][c - 1] == '0'):
                    valid_position = False
            except:
                print("hidasdjhisa")
    return valid_position


def draw_window(game_position, player_table, system_table):
    screen = pygame.display.set_mode((BOARD_WIDTH * 2, BOARD_HEIGHT))
    screen.fill(WHITE)
    draw_board(screen, player_table, system_table)


if __name__ == "__main__":
    main()
