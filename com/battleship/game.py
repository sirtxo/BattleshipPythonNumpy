import numpy as np
import pygame
import com.battleship.config.variables as var
from com.battleship.model.Objects import *
from com.battleship.util.functions import show_window

player_ships = [Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(),
                Ship()]
games_ships = [Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(), Ship(),
               Ship()]
player_game_steps = [["Start"],
                     ["Place_Ship", 4, 1, 4],
                     ["Place_Ship", 3, 2, 3],
                     ["Place_Ship", 2, 3, 2],
                     ["Place_Ship", 1, 4, 1],
                     ["System_ships"],
                     ["Game"],
                     ["End_Game"]]
game_position = 0
ship_position = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((var.BOARD_WIDTH * 2, var.BOARD_HEIGHT))
    screen.fill(var.WHITE)

    player_ships = [Ship() for _ in range(14)]
    systems_ships = [Ship() for _ in range(14)]

    player_table = np.full((var.MAX_CELLS, var.MAX_CELLS), var.PLAYER_WATER_SYMBOL)
    system_table = np.full((var.MAX_CELLS, var.MAX_CELLS), var.SYSTEM_WATER_SYMBOL)
    if player_game_steps[game_position][0] == var.STATUS_START:
        show_window(var.START_MESSAGE,
                    screen,
                    player_table,
                    system_table,
                    game_position,
                    ship_position,
                    player_ships,
                    player_game_steps,
                    systems_ships)


if __name__ == "__main__":
    main()
