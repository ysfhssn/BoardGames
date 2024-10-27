import game
import random

def get_move(game_info):
    return random.choice(game.get_valid_moves(game_info))
