import numpy as np
import pygame
import com.battleship.config.variables as var
from com.battleship.model.Objects import *
from com.battleship.util.functions import paint_game_window

# List of ships owned by the player
player_ships = [Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(),
                Ship()]

# List of ships in various systems
systems_ships = [Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(),
                 Ship()]

# List of steps in the game, including ship placement and game progression
player_game_steps = [["Start"],
                     ["Place_Ship", 4, 1, 4],  # Action: Place ship of length 4, Quantity: 1, Priority: 4
                     ["Place_Ship", 3, 2, 3],  # Action: Place ship of length 3, Quantity: 2, Priority: 3
                     ["Place_Ship", 2, 3, 2],  # Action: Place ship of length 2, Quantity: 3, Priority: 2
                     ["Place_Ship", 1, 4, 1],  # Action: Place ship of length 1, Quantity: 4, Priority: 1
                     ["System_ships"],  # Action: Assign ships to systems
                     ["Game"],  # Action: Start game
                     ["End_Game"]]  # Action: End game

# Position in the game
game_position = 0

# Position of ship
ship_position = 0


def main():
    """
    Initialize the game window and paint the initial game state.

    Initializes Pygame and retrieves the game window screen.
    Then, initializes game variables such as player ships, player table,
    system table, and system ships.
    Finally, paints the initial game window with the required information.

    Returns
    -------
    None

    Notes
    -----
    This function serves as the entry point for the game.

    Examples
    --------
    >>> main()
    """
    # Initialize Pygame and get the game window screen
    screen = pygame_init()

    # Initialize game variables including player ships, player table, system table, and system ships
    player_ships, player_table, system_table, systems_ships = init_game_vars()

    # Paint the initial game window with necessary information
    paint_game_window(var.START_MESSAGE,
                      screen,
                      player_table,
                      system_table,
                      game_position,
                      ship_position,
                      player_ships,
                      player_game_steps,
                      systems_ships)


def init_game_vars():
    player_ships = [Ship() for _ in range(14)]
    systems_ships = [Ship() for _ in range(14)]
    player_table = np.full((var.MAX_CELLS, var.MAX_CELLS), var.PLAYER_WATER_SYMBOL)
    system_table = np.full((var.MAX_CELLS, var.MAX_CELLS), var.SYSTEM_WATER_SYMBOL)
    return player_ships, player_table, system_table, systems_ships


def pygame_init():
    pygame.init()
    screen = pygame.display.set_mode((var.BOARD_WIDTH * 2, var.BOARD_HEIGHT))
    screen.fill(var.WHITE)
    return screen


if __name__ == "__main__":
    main()
