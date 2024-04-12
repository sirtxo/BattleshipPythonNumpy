import numpy as np
import pygame
import sys
import random

PLAYER_SHIP_SYMBOL = "x"


class Ship:
    def __init__(self, ship_type=None, size=None, positions=[],  is_sunk=None):
        self.ship_type = ship_type
        self.size = size
        self.positions = positions
        self.is_sunk = is_sunk

    def __str__(self):
        return f"Ship(ship_type={self.ship_type}, size={self.size}, positions={self.positions}, orientation={self.orientation}, is_sunk={self.is_sunk})"

TITLE_OF_GAME = "Battleship"
START_IMG = 'battleship/img/hundir-la-flota-juego-de-mesa.jpg'
SYSTEM_WATER_SYMBOL = "+"
PLAYER_WATER_SYMBOL = "-"

BOARD_HEIGHT = 600
MAX_CELLS = 10
BOARD_WIDTH = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (25, 25, 25)

player_ships = [Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship()]
games_ships = []
#0:name - 1 :: 1:construction_position :: 2:number_of_ships :: 4 default_number_positions :: 5 : position,  :: 6 : orientation
player_game_status = [["Start"], ["Place_Ship", 4, 1, 4, []], ["Place_Ship", 3, 2, 3, []],
                      ["Place_Ship", 2, 3, 2, []], ["Place_Ship", 1, 4, 1, []],
                      ["System_ships", 1, 4],
                      ["Game"], ["End_Game"]]
#status = [["Start", 0, 0, 0], ["Place_Ship", 1, 1, 1], ["System_ships", 1, 4], ["Game"], ["End_Game"]]
game_position = 0
ship_position = 0

def show_message_window(text2, screen, player_table, system_table, game_position=None):
    do_action_on_window(game_position, screen, text2)
    wait_message_window_action(game_position, player_table, screen, system_table, ship_position,player_ships)

def wait_message_window_action(game_position, player_table, screen, system_table,ship_position,player_ships):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player_game_status[game_position][0] == "Start":
                        game_position += 1
                        screen.fill(WHITE)
                        show_game_window(player_table, system_table, screen, game_position,ship_position,player_ships)

def do_action_on_window(game_position, screen, text2):
    if player_game_status[game_position][0] == "Start":
        pygame.display.set_caption(TITLE_OF_GAME)
        image1 = pygame.image.load(START_IMG).convert_alpha()
        image1 = pygame.transform.scale(image1, (BOARD_WIDTH * 2, BOARD_HEIGHT))
        screen.fill(WHITE)
        screen.blit(image1, (0, 0))
    else:
        font = pygame.font.Font(None, 36)
        text = font.render(text2, True, (255, 0, 0))  # Texto de la alerta
        text_rect = text.get_rect(center=(150, 100))
        screen.blit(text, text_rect)

    pygame.display.flip()

def draw_board(screen, player_table, system_table):
    cell_size = BOARD_WIDTH // MAX_CELLS
    font = pygame.font.Font(None, 36)
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
    player_table = np.full((MAX_CELLS, MAX_CELLS), PLAYER_WATER_SYMBOL)
    system_table = np.full((MAX_CELLS, MAX_CELLS), SYSTEM_WATER_SYMBOL)
    if player_game_status[game_position][0] == "Start":
        show_message_window("Iniciando juego", screen, player_table, system_table, game_position)

def check_position_on_table(pos, table, tuplo):
    if table[pos] == SYSTEM_WATER_SYMBOL or table[pos] == PLAYER_WATER_SYMBOL:
        table[pos] = tuplo[0]
    else:
        table[pos] = tuplo[1]

def generate_random_position(board_size):
    return random.randint(0, board_size - 1), random.randint(0, board_size-1)

def show_game_window(player_table, system_table, screen, game_position, ship_position,player_ships):
    screen.fill(WHITE)
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
                        int(event.pos[1] // (BOARD_HEIGHT / MAX_CELLS)), int(event.pos[0] // (BOARD_WIDTH / MAX_CELLS))
                    )
                    if player_game_status[game_position][0] == "Place_Ship":
                        game_position,ship_position = place_player_ships(game_position, ship_position, player_table, pos, system_table,player_ships)

                    if player_game_status[game_position][0] == "System_ships":
                        do_system_ships(game_position, player_table, system_table)
                        game_position = game_position + 1
                        if player_game_status[game_position][0] == "Game":
                            show_game_window(player_table, system_table, screen, game_position, ship_position,player_ships)
                    if player_game_status[game_position][0] == "Game":
                        check_position_on_table(pos, system_table, ("W", "B"))
                        check_position_on_table(generate_random_position(MAX_CELLS), player_table, ("w", "b"))

                        show_game_window(player_table, system_table, screen, game_position, ship_position,player_ships)
                        pygame.display.flip()


# player_game_status -> 0:name - 1 :: 1:construction_position :: 2:number_of_ships :: 4 default_number_positions :: 5 : position, :: 6 : orientation

class PositionException(BaseException):
    pass


#pos vector
#positions list vector

def check_position(positions, pos):
    check_orientation(pos, positions)
    adjacent_found = False
    for position in positions:
        if is_adjacent(position, pos):
            adjacent_found = True

    if not adjacent_found:
        print("not is adjacent")
        raise PositionException("Orientation is bad...")
    return False

# Función auxiliar para verificar si dos posiciones están adyacentes
def is_adjacent(position1, position2):
    x1, y1 = position1
    x2, y2 = position2
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1 != x2 or y1 != y2)


def check_orientation(pos, positions):
    orientation = "H"
    pos_orientation = "H"
    if positions[0][0] != positions[1][0]:
        orientation = "V"
    if positions[0][0] != pos[0]:
        pos_orientation = "V"
    if orientation != pos_orientation:
        raise PositionException("Orientation is bad...")


def place_player_ships(game_position,ship_position, player_table, pos, system_table,player_ships):
    # Comprueba si hay más posiciones de construcción disponibles para el jugador
    if player_game_status[game_position][1] >= 0:
        # Marca la posición del jugador en el tablero
        if player_table[pos] != PLAYER_SHIP_SYMBOL:
            try:
                if len(player_ships[ship_position].positions) > 1:
                    check_position(player_ships[ship_position].positions, pos)
                player_table[pos] = PLAYER_SHIP_SYMBOL
                # Agrega la posición a las posiciones del barco del jugador
                ship = player_ships[ship_position]
                ship.positions.append(pos)
                player_ships[ship_position] = ship
                # Dibuja la ventana del juego actualizada
                draw_window(game_position, player_table, system_table)
                # Reduce el número de posiciones de construcción disponibles
                player_game_status[game_position][1] = player_game_status[game_position][1] - 1
                # Si se han utilizado todas las posiciones de construcción para este tipo de barco
                if player_game_status[game_position][1] == 0:
                    # Reduce el número total de barcos para este tipo
                    player_game_status[game_position][2] = player_game_status[game_position][2] - 1
                    ship_position = ship_position+1
                    # Si quedan más barcos por colocar
                    if player_game_status[game_position][2] > 0:
                        # Restablece las posiciones de construcción para el siguiente barco
                        player_game_status[game_position][1] = player_game_status[game_position][3]
                    else:
                        # Mueve el juego al siguiente estado
                        game_position = game_position + 1
            except PositionException as exc:
                print(f"Error on positionate ship try again {exc}")

    # Devuelve el estado actual del juego
    return game_position, ship_position


def go_to_next_status(game_position, player_table, system_table):
    draw_window(game_position + 1, player_table, system_table)


def do_system_ships(game_position, player_table, system_table):
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
                        table[r - 1][c] == '0'\
                        or table[r - 1][c - 1] == '0'):
                    valid_position = False
            except:
                print("Error continue")
    return valid_position


def draw_window(game_position, player_table, system_table):
    screen = pygame.display.set_mode((BOARD_WIDTH * 2, BOARD_HEIGHT))
    screen.fill(WHITE)
    draw_board(screen, player_table, system_table)


if __name__ == "__main__":
    main()
