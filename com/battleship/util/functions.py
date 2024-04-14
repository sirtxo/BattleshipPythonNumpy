import math
from turtle import distance

import pygame
import sys
import random
from com.battleship.exception.Exceptions import PositionException
import numpy as np

import com.battleship.config.variables as var

system_ships_steps = [["Place_Ship", 4, 1, 4], ["Place_Ship", 3, 2, 3], ["Place_Ship", 2, 3, 2],
                      ["Place_Ship", 1, 4, 1]]

debugger_enable = True


def show_window(text2, screen, player_table, system_table, game_position, ship_position,
                player_ships, player_game_steps, systems_ships=None):
    """
    Display the game window and handle user interactions.

    This function orchestrates the display of the game window and handles user interactions.
    It calls two sub-functions to perform specific actions on the window: `do_action_on_window`
    and `wait_message_window_action`.

    Parameters
    ----------
    text2 : str
        Text to be displayed on the game window.
    screen : pygame.Surface
        The game window surface.
    player_table : list
        List representing the player's game table.
    system_table : list
        List representing the system's game table.
    game_position : int
        Current position in the game state.
    ship_position : int
        Current position of the ship being placed.
    player_ships : list
        List containing information about the player's ships.
    player_game_steps : list
        List containing information about the game steps for the player.
    systems_ships : list, optional
        List containing information about the system's ships (default is None).

    Returns
    -------
    None

    Notes
    -----
    This function coordinates the display of the game window and user interactions.

    Examples
    --------
    >>> show_window("Player's turn", screen, player_table, system_table, 0, 0, player_ships, game_steps)
    """
    do_action_on_window(game_position, screen, text2, player_game_steps)
    wait_message_window_action(game_position, player_table, screen, system_table, ship_position, player_ships,
                               player_game_steps, systems_ships)


def wait_message_window_action(game_position, player_table, screen, system_table, ship_position, player_ships,
                               player_game_steps, systems_ships):
    """
    Wait for user input and handle mouse button clicks.

    This function waits for user input events and specifically handles mouse button clicks.
    If the left mouse button is clicked during the start game status, it advances the game state
    and updates the game window accordingly.

    Parameters
    ----------
    game_position : int
        Current position in the game state.
    player_table : list
        List representing the player's game table.
    screen : pygame.Surface
        The game window surface.
    system_table : list
        List representing the system's game table.
    ship_position : int
        Current position of the ship being placed.
    player_ships : list
        List containing information about the player's ships.
    player_game_steps : list
        List containing information about the game steps for the player.
    systems_ships : list
        List containing information about the system's ships.

    Returns
    -------
    None

    Notes
    -----
    This function listens for user input events and handles left mouse button clicks during the start game status.

    Examples
    --------
    >>> wait_message_window_action(0, player_table, screen, system_table, 0, player_ships, game_steps, systems_ships)
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player_game_steps[game_position][0] == var.STATUS_START:
                        game_position += 1
                        screen.fill(var.WHITE)
                        show_game_window(player_table, system_table, screen, game_position, ship_position, player_ships,
                                         player_game_steps, systems_ships)


def do_action_on_window(game_position, screen, text2, player_game_steps):
    if player_game_steps[game_position][0] == var.STATUS_START or player_game_steps[game_position][0] == var.STATUS_END:
        draw_window_img(game_position, player_game_steps, screen)
    else:
        draw_window_text(screen, text2)

    pygame.display.flip()


def draw_window_text(screen, text2):
    font = pygame.font.Font(None, 36)
    text = font.render(text2, True, (255, 0, 0))  # Texto de la alerta
    text_rect = text.get_rect(center=(150, 100))
    screen.blit(text, text_rect)


def draw_window_img(game_position, player_game_steps, screen):
    pygame.display.set_caption(var.TITLE_OF_GAME)
    if player_game_steps[game_position][0] == var.STATUS_END:
        image1 = pygame.image.load(var.END_IMG).convert_alpha()
    else:
        image1 = pygame.image.load(var.START_IMG).convert_alpha()
    image1 = pygame.transform.scale(image1, (var.BOARD_WIDTH * 2, var.BOARD_HEIGHT))
    screen.fill(var.WHITE)
    screen.blit(image1, (0, 0))


def draw_board(screen, player_table, system_table):
    """
    Draw the game board with player and system tables.

    This function draws the game board on the provided screen surface,
    including the player's table, player's grids, system's table, and system's grids.

    Parameters
    ----------
    screen : pygame.Surface
        The game window surface.
    player_table : list
        List representing the player's game table.
    system_table : list
        List representing the system's game table.

    Returns
    -------
    None

    Examples
    --------
    >>> draw_board(screen, player_table, system_table)
    """
    cell_size = var.BOARD_WIDTH // var.MAX_CELLS
    font = pygame.font.Font(None, 36)

    # Draw the player's table
    draw_player_table(cell_size, font, player_table, screen)

    # Draw the player's grids
    draw_pllayer_grids(cell_size, screen)

    # Draw the system's table
    draw_system_table(cell_size, font, screen, system_table)

    # Draw the system's grids
    draw_system_table_grids(cell_size, screen)

    pygame.display.flip()


def draw_system_table_grids(cell_size, screen):
    # Draw grid lines for system's board
    for i in range(var.MAX_CELLS + 1):
        pygame.draw.line(screen, var.GRAY, (i * cell_size + var.BOARD_WIDTH, 0),
                         (i * cell_size + var.BOARD_WIDTH, var.BOARD_HEIGHT))
        pygame.draw.line(screen, var.GRAY, (0, i * cell_size + var.BOARD_WIDTH),
                         (var.BOARD_HEIGHT, i * cell_size + var.BOARD_WIDTH))


def draw_system_table(cell_size, font, screen, system_table):
    # Display system's board contents
    for i in range(var.MAX_CELLS):
        for j in range(var.MAX_CELLS):
            if debugger_enable:
                text = font.render(system_table[i, j], True, var.GREEN)
            elif system_table[i, j] == "0":
                text = font.render(var.SYSTEM_WATER_SYMBOL, True, var.GREEN)
            else:
                text = font.render(system_table[i, j], True, var.GREEN)
            text_rect = text.get_rect(center=(j * cell_size + cell_size // 2 + var.BOARD_WIDTH,
                                              i * cell_size + cell_size // 2))
            screen.blit(text, text_rect)


def draw_pllayer_grids(cell_size, screen):
    # Draw grid lines for player's board
    for i in range(var.MAX_CELLS + 1):
        pygame.draw.line(screen, var.GRAY, (i * cell_size, 0), (i * cell_size, var.BOARD_HEIGHT))
        pygame.draw.line(screen, var.GRAY, (0, i * cell_size), (var.BOARD_HEIGHT, i * cell_size))


def draw_player_table(cell_size, font, player_table, screen):
    for i in range(var.MAX_CELLS):
        for j in range(var.MAX_CELLS):
            text = font.render(player_table[i, j], True, var.BLACK)
            text_rect = text.get_rect(center=(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
            screen.blit(text, text_rect)


def check_position_on_table(pos, table, tuplo):
    if table[pos] == var.SYSTEM_WATER_SYMBOL or table[pos] == var.PLAYER_WATER_SYMBOL or table[pos] == var.PLAYER_SYSTEM_WATER or table[pos] == var.SYSTEM_PLAYER_WATER:
        table[pos] = tuplo[0]
    else:
        table[pos] = tuplo[1]


def generate_random_position(board_size):
    return random.randint(0, board_size - 1), random.randint(0, board_size - 1)


def show_game_window(player_table, system_table, screen, game_position, ship_position, player_ships, player_game_steps,
                     systems_ships):
    screen.fill(var.WHITE)
    draw_board(screen, player_table, system_table)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = (
                        int(event.pos[1] // (var.BOARD_HEIGHT / var.MAX_CELLS)),
                        int(event.pos[0] // (var.BOARD_WIDTH / var.MAX_CELLS))
                    )
                    ##Step place Ship
                    if player_game_steps[game_position][0] == var.STEP_PLACE_SHIP:
                        game_position, ship_position = place_player_ships(game_position, ship_position, player_table,
                                                                          pos, system_table, player_ships,
                                                                          player_game_steps)

                    ##Step place System Ships
                    if player_game_steps[game_position][0] == var.STEP_SYSTEM_SHIPS:

                        do_system_ships(game_position, player_table, system_table, systems_ships)
                        game_position = game_position + 1
                        if player_game_steps[game_position][0] == var.STATUS_GAME:
                            show_game_window(player_table, system_table, screen, game_position, ship_position,
                                             player_ships, player_game_steps, systems_ships)

                    ##Step play game
                    if player_game_steps[game_position][0] == var.STATUS_GAME:
                        check_position_on_table(pos, system_table, (var.PLAYER_SYSTEM_WATER, var.PLAYER_SYSTEM_BOOM))
                        if not (check_element(system_table, "0")):
                            game_position = game_position + 1
                            print("Has ganado")
                            show_window("Has Ganado!", screen, player_table, system_table, game_position, ship_position,
                                        player_ships, player_game_steps, systems_ships)
                        else:
                            check_position_on_table(generate_random_position(var.MAX_CELLS), player_table,
                                                    (var.SYSTEM_PLAYER_WATER, var.SYSTEM_PLAYER_BOOM))
                            if not (check_element(system_table, "0")):
                                game_position = game_position + 1
                                print("Ha ganado la máquina")
                                show_window("Ha ganado la máquina!", screen, player_table, system_table,
                                            game_position)
                            else:
                                show_game_window(player_table, system_table, screen, game_position, ship_position,
                                                 player_ships, player_game_steps, systems_ships)
                                pygame.display.flip()


def end_game():
    pygame.quit()
    sys.exit()


def check_element(table, element):
    return np.any(table == element)


def check_position(positions, pos):
    check_orientation(pos, positions)
    adjacent_found = False
    for position in positions:
        if is_adjacent_and_not_diagonal(position, pos):
            adjacent_found = True

    if not adjacent_found:
        print("not is adjacent")
        raise PositionException("Orientation is bad...")
    return False


def checkAdjacent(pos, positions):
    adjacent_found = False
    for position in positions:
        if is_adjacent_and_not_diagonal(position, pos):
            adjacent_found = True
    if adjacent_found:
        print("not is adjacent")
        raise PositionException("Orientation is bad...")


def check_all_adjacent_and_distance(all_positions, check_positions):
    adjacent_found_and_distance = False
    for pos in check_positions:
        for position in all_positions:
            if is_adjacent_and_distance(position, pos):
                adjacent_found_and_distance = True

    return adjacent_found_and_distance


def check_no_adjacent(pos, positions):
    adjacent_no_found = True
    for position in positions:
        if is_adjacent_and_not_diagonal(position, pos):
            adjacent_no_found = False
    if adjacent_no_found:
        print("not is adjacent")
        raise PositionException("Orientation is bad...")


# Función auxiliar para verificar si dos posiciones están adyacentes y en diagonal
# Method to check if two positions are adjacent on a 2D grid
def is_adjacent_and_not_diagonal(position1, position2):
    # Extract x and y coordinates of both positions
    x1, y1 = position1
    x2, y2 = position2

    # Check if absolute difference between x and y coordinates is <= 1
    # and ensure positions are not the same
    adjacent_condition = (abs(int(x1) - int(x2)) <= 1 and abs(int(y1) - int(y2)) <= 1 and abs(int(x2) - int(x1)) <= 1
                          and abs(int(y2) - int(y1)) <= 1 and (int(x1) != int(x2) or int(y1) != int(y2)))

    # Return True if positions are adjacent but not diagonal
    # Return False otherwise
    return adjacent_condition and distance(position1, position2) >= 1


def check_diagonal(position1, position2):
    x1, y1 = position1
    x2, y2 = position2
    # Check if the difference between x and y coordinates is equal
    # This indicates diagonal movement
    if abs(int(x1) - int(x2)) == abs(int(y1) - int(y2)):
        raise PositionException("Orientation is bad...")


# Method to check if two positions are adjacent and have a minimum distance
def is_adjacent_and_distance(position1, position2):
    x1, y1 = position1
    x2, y2 = position2

    if int(position1[0]) == int(position2[0]) and int(position1[1]) == int(position2[1]):
        return True
    else:

        # Check if absolute difference between x and y coordinates is <= 1
        adjacent_condition = abs(int(x1) - int(x2)) <= 1 and abs(int(y1) - int(y2)) <= 1

        # Check if positions are adjacent and distance is >= 1
        if adjacent_condition and distance(position1, position2) >= 1:
            return True
        else:
            return False


# Method to calculate Euclidean distance between two positions in a 2D grid
def distance(position1, position2):
    # Extract x and y coordinates of both positions
    x1, y1 = position1
    x2, y2 = position2

    # Calculate square of difference in x coordinates
    # Calculate square of difference in y coordinates
    # Sum them up and take square root to get distance
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def check_orientation(pos, positions):
    orientation = "H"
    pos_orientation = "H"
    if positions[0][0] != positions[1][0]:
        orientation = "V"
    if positions[0][0] != pos[0]:
        pos_orientation = "V"
    if orientation != pos_orientation:
        raise PositionException("Orientation is bad...")


def place_player_ships(game_position, ship_position, player_table,
                       pos, system_table, player_ships, player_game_steps):
    # Comprueba si hay más posiciones de construcción disponibles para el jugador
    if player_game_steps[game_position][1] >= 0:
        # Marca la posición del jugador en el tablero
        if player_table[pos] != var.PLAYER_SHIP_SYMBOL:
            try:
                positions = np.empty((0, 2))

                check_position_is_correct(player_ships, pos, positions, ship_position)

                if len(player_ships[ship_position].positions) > 0:
                    check_diagonal(pos, player_ships[ship_position].positions[
                        len(player_ships[ship_position].positions) - 1])
                player_table[pos] = var.PLAYER_SHIP_SYMBOL

                player_ships[ship_position].positions.append(pos)

                # Dibuja la ventana del juego actualizada
                draw_window(game_position, player_table, system_table)
                # Reduce el número de posiciones de construcción disponibles
                player_game_steps[game_position][1] = player_game_steps[game_position][1] - 1
                # Si se han utilizado todas las posiciones de construcción para este tipo de barco
                if player_game_steps[game_position][1] == 0:
                    # Reduce el número total de barcos para este tipo
                    player_game_steps[game_position][2] = player_game_steps[game_position][2] - 1
                    ship_position = ship_position + 1
                    # Si quedan más barcos por colocar
                    if player_game_steps[game_position][2] > 0:
                        # Restablece las posiciones de construcción para el siguiente barco
                        player_game_steps[game_position][1] = player_game_steps[game_position][3]
                    else:
                        # Mueve el juego al siguiente estado
                        game_position = game_position + 1
            except PositionException as exc:
                print(f"Error on positionate ship try again {exc}")

    # Devuelve el estado actual del juego
    return game_position, ship_position


def check_position_is_correct(player_ships, pos, positions, ship_position):
    if ship_position - 1 >= 0:
        for ship in player_ships[:ship_position]:
            ship_positions = np.array(ship.positions)
            positions = np.concatenate((positions, ship_positions))
        checkAdjacent(pos, positions)
    if len(player_ships[ship_position].positions) > 0:
        check_no_adjacent(pos, player_ships[ship_position].positions)
        if len(player_ships[ship_position].positions) > 1:
            check_position(player_ships[ship_position].positions, pos)


def go_to_next_status(game_position, player_table, system_table):
    draw_window(game_position + 1, player_table, system_table)


def do_system_ships(game_position, player_table, system_table, systems_ships):
    cont = 0
    for sublist in system_ships_steps:
        num_ships = sublist[2]
        for i in range(num_ships):
            num_positions = sublist[1]
            positions = []
            tuple_sys_list, cont = generate_ship_positions(var.MAX_CELLS, num_positions, system_table, systems_ships,
                                                           cont)
            for tuple_sys in tuple_sys_list:
                paint_ship_position(positions, system_table, tuple_sys)

            systems_ships[cont].positions = positions
            cont += 1
            draw_window(game_position, player_table, system_table)


def paint_ship_position(positions, system_table, tuple_sys):
    positions.append(tuple_sys)
    system_table[tuple_sys] = "0"


def generate_ship_positions(board_size, ship_size, system_table, systems_ships, cont):
    valid_position = False
    if ship_size == 1:
        print()

    while not valid_position:
        random_positions = create_random_position(board_size, ship_size)

        system_positions = get_all_systems_ships_positions(systems_ships)

        if check_all_adjacent_and_distance(system_positions, np.array(random_positions)):
            valid_position = False
        elif not (check_elements(random_positions, system_table)):
            return random_positions, cont
        else:
            valid_position = False


def get_all_systems_ships_positions(systems_ships):
    system_positions = np.empty((0, 2))
    for ship in systems_ships:
        ship_positions = np.array(ship.positions)
        if ship_positions.size > 0:
            ship_positions = np.atleast_2d(ship_positions)
            system_positions = np.concatenate((system_positions, ship_positions))
    return system_positions


def create_random_position(board_size, ship_size):
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

    return positions


def check_valid_position(positions, table, ):
    valid_position = True
    for r, c in positions:
        if table[r][c] == '0':
            try:
                if (table[r][c + 1] == '0' or table[r + 1][c] == '0'
                        or table[r + 1][c + 1] != '0' or table[r][c - 1] != '0' or
                        table[r - 1][c] == '0'
                        or table[r - 1][c - 1] == '0'):
                    valid_position = False
            except:
                print("Error continue")
    return valid_position


def check_elements(positions, table):
    is_element = False
    for pos in positions:
        if table[pos] == '0':
            is_element = True
    return is_element


def draw_window(game_position, player_table, system_table):
    screen = pygame.display.set_mode((var.BOARD_WIDTH * 2, var.BOARD_HEIGHT))
    screen.fill(var.WHITE)
    draw_board(screen, player_table, system_table)
