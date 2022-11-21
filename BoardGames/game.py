#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""
    NOMENCLATURE A RESPECTER (exceptions in chess)
    move = (int, int)
    game_info = List[...] :
        0: board      	    List[List[int]]
        1: player           int (1 ou 2)
        2: valid moves	    List[(int, int)]
        3: played moves     List[(int, int)]
        4: score            List[int, int]
"""

game	= None
player1	= None
player2	= None
GUI     = True


# Generic Functions
def get_board(game_info):
    return game_info[0]

def get_player(game_info):
    return game_info[1]

def change_player(game_info):
    game_info[1] = 2 if game_info[1] == 1 else 1

def get_winner(game_info):
    score = game_info[4][-1] if isinstance(game_info[4][-1], tuple) else game_info[4]
    if score[0] == score[1]:
        return 0
    return 1 if score[0] > score[1] else 2

def get_valid_moves(game_info):
    return game.get_valid_moves(game_info)

def get_played_moves(game_info):
    return game_info[3]

def get_score(game_info):
    score = game_info[4][-1] if isinstance(game_info[4][-1], tuple) else game_info[4]
    return score

def get_score_player(game_info, player):
    score = game_info[4][-1] if isinstance(game_info[4][-1], tuple) else game_info[4]
    return score[0] if player == 1 else score[1]

def get_position_value(game_info, row, col):
    return game_info[0][row][col]

def get_game_copy(game_info):
    game_copy = []
    for i in game_info:
        if isinstance(i, list):
            if i != [] and isinstance(i[0], list): game_copy.append([ii[:] for ii in i])
            else: game_copy.append(i[:])
        else: game_copy.append(i)
    return game_copy


# Specific functions
def init():
    return game.init()

def init_test(key=0):
    return game.init_test(key)

def is_game_over(game_info):
    return game.is_game_over(game_info)

def get_move(game_info):
    player = get_player(game_info)
    return player1.get_move(game_info) if player == 1 else player2.get_move(game_info)

def play_move(game_info, move):
    game.play_move(game_info, move)

def print_game(game_info):
    game.print_game(game_info)


if __name__ == "__main__":
    if GUI:
        import games_selection
        games_selection.selection()
    else:
        print("GUI mode is off")
