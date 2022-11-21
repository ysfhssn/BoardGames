#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game

NUM_MAX_MOVES = 100

def init():
    """ void -> game_info
        move = (int, int)
        Initialise le game_info List[...] :
            0: board      	List[List[int]]
            1: player       int (1 ou 2)
            2: valid moves	List[(int, int)]
            3: played moves List[(int, int)]
            4: scores       List[int, int]
    """
    board = [[4,4,4,4,4,4],
               [4,4,4,4,4,4]]
    return [board, 1, None, [], [0, 0]]

def init_test(key=0):
    d = {
        0: [[0,1,0,0,0,0],
            [0,0,0,0,0,0]],
        1: [[1,0,0,0,0,0],
            [1,0,0,0,0,0]],
        2: [[6,0,0,0,0,0],
            [1,0,0,2,2,2]],
    }

    return [d[key], 1, None, [], [0, 0]]

def is_opponent_starving(game_info):
    opponent = game.get_player(game_info)%2 + 1
    return sum(game_info[0][opponent-1]) == 0

def is_opponent_fed(game_info, move):
    player = game.get_player(game_info)
    if player == 1:
        return game.get_position_value(game_info, move[0], move[1]) - move[1] > 0
    return game.get_position_value(game_info, move[0], move[1]) + move[1] > 5

def get_valid_moves(game_info):
    if game_info[2] is None:
        row = game.get_player(game_info) - 1
        b = is_opponent_starving(game_info)
        game_info[2] = [(row, col) for col in range(6) if game.get_position_value(game_info, row, col) > 0 and (not b or is_opponent_fed(game_info, (row, col)))]
    return game_info[2]

def is_game_over(game_info):
    if game_info[4][0] >= 25 or game_info[4][1] >= 25:
        return True
    if not game.get_valid_moves(game_info):
        game_info[4][0] += sum(game_info[0][0])
        game_info[4][1] += sum(game_info[0][1])
        return True
    if len(game.get_played_moves(game_info)) >= NUM_MAX_MOVES:
        return True

    return False

def next_pit(row, col):
    if row == 0 and col == 0:
        return (1, 0)
    if row == 1 and col == 5:
        return (0, 5)
    if row == 0:
        return (row, col-1)
    else:
        return (row, col+1)

def prev_pit(row, col):
    if row == 1 and col == 0:
        return (0, 0)
    if row == 0 and col == 5 :
        return (1, 5)
    if row == 0:
        return (row, col+1)
    else:
        return (row, col-1)

def move_seeds(game_info, move):
    """Retourne la pit finale"""
    row = move[0]
    col = move[1]
    seeds = game.get_position_value(game_info, row, col)
    pit = move
    game_info[0][row][col] = 0
    while seeds > 0:
        pit = next_pit(pit[0], pit[1])
        if pit != move:
            game_info[0][pit[0]][pit[1]] += 1
            seeds -= 1
    return pit

def play_move(game_info, move):
    row, col = move_seeds(game_info, move)
    game_copy = game.get_game_copy(game_info)

    player = game.get_player(game_info)
    opponent = player % 2
    seeds = game.get_position_value(game_info, row, col)

    while row == opponent and (seeds == 2 or seeds == 3):
        game_info[0][row][col] = 0
        game_info[4][player-1] += seeds
        row, col = prev_pit(row, col)
        seeds = game.get_position_value(game_info, row, col)

    if is_opponent_starving(game_info):
        game_info[0] = game_copy[0]
        game_info[4] = game_copy[4]

    game.change_player(game_info)
    game_info[2] = None
    game_info[3].append(move)



def print_board(game_info):
	board = game_info[0]

	for i in range(len(board[0])):
		if i == 0:
			print("%5s|" %(""), end="")
		print("%3s  |" %(i), end="")

	print("\n", "-"*6*7)

	for i in range(len(board)):
		print("%3s  |" %(i), end="")
		for j in range(len(board[i])):
			if board[i][j] == 0:
				print("%5s|" %(""), end="")
			else:
				print("%3s  |" %(board[i][j]), end="")

		print("\n", "-"*6*7)

def print_game(game_info):
	print("Last played move =", "None" if not game_info[3] else game_info[3][-1])
	print(f"Scores = {game_info[4]}")
	print("Board:")
	print_board(game_info)
	print(f"Player {game_info[1]}, it's your turn\n")
