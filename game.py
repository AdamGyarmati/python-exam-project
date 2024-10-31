from board.game_board import GameBoard
from engine import Engine


gameboard = GameBoard("Mosquito splasher")
engine = Engine(gameboard)
engine.start_game()
