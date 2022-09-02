#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
import awele
from Awele.Players import first_move

game.game = awele
game.player1 = first_move
game.player2 = first_move


game_info = game.init_test()
assert(game.get_position_value(game_info, 0, 1) == 1)
assert(game.get_valid_moves(game_info) == [])
assert(game.is_game_over(game_info) == True)
assert(game.get_winner(game_info) == 1)
assert(game.get_scores(game_info) == [1, 0])

game_info = game.init_test(1)
assert(len(game.get_valid_moves(game_info)) == 1)
move = game.get_move(game_info)
game.play_move(game_info, move)
assert(game.game.adversaireAffame(game_info) == True)
assert(game.is_game_over(game_info) == True)
assert(game.get_winner(game_info) == game.get_player(game_info))
assert(game.get_score(game_info, 2) == 2)

game_info = game.init_test(2)
move = game.get_move(game_info)
game.play_move(game_info, move)
assert(game.get_scores(game_info) == [9, 0])
assert(game.is_game_over(game_info) == True)
assert(game.get_scores(game_info) == [9, 4])
