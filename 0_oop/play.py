# implements the card game Silver: Amulet by Teo Alspach
import easygui
import random

# import classes

import classes.silveramulet as c


if __name__ == "__main__":
    # start the game
    game = c.SilverAmulet()
    game.run_game()
