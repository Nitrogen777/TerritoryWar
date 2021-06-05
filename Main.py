"""
The main file, used to run the game.
"""
import GraphicsHandler
from GameUtils import Player
import GameUtils

# Begin the game with 1 human player and 1 AI player
GameUtils.start(Player((98, 255, 98), False), Player((255, 45, 180), True))

